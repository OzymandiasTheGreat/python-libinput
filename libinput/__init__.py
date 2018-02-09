#!/usr/bin/env python3

from __future__ import absolute_import, print_function
from ctypes import CDLL, POINTER, byref, CFUNCTYPE, create_string_buffer
from ctypes import c_int, c_char_p, c_void_p
try:
	from time import monotonic
except ImportError:
	from monotonic import monotonic
try:
	from selectors import DefaultSelector, EVENT_READ
except ImportError:
	from selectors34 import DefaultSelector, EVENT_READ
from .version import __version__
from .define import Interface, Device
from .constant import LogPriority
from .event import Event


__all__ = ('LibInput', 'constant', 'evcodes')


class LibInput(object):
	"""Main class representing libinput context.

	Context is used to manage devices and get events.

	Attributes:
		udev (bool): A boolean indicating weather this context uses udev.
	"""

	_libc = CDLL('libc.so.6')
	_libc.vsprintf.argtypes = (c_char_p, c_char_p, c_void_p)
	_libc.vsprintf.restype = c_int
	_libudev = CDLL('libudev.so.1')
	_libudev.udev_new.argtypes = None
	_libudev.udev_new.restype = c_void_p
	_libudev.udev_unref.argtypes = (c_void_p,)
	_libudev.udev_unref.restype = None
	_libinput = CDLL('libinput.so.10')
	_libinput.libinput_udev_create_context.argtypes = (
		POINTER(Interface.Interface), c_void_p, c_void_p)
	_libinput.libinput_udev_create_context.restype = c_void_p
	_libinput.libinput_udev_assign_seat.argtypes = (c_void_p, c_char_p)
	_libinput.libinput_udev_assign_seat.restype = c_int
	_libinput.libinput_path_create_context.argtypes = (
		POINTER(Interface.Interface), c_void_p)
	_libinput.libinput_path_create_context.restype = c_void_p
	_libinput.libinput_unref.argtypes = (c_void_p,)
	_libinput.libinput_unref.restype = c_void_p
	_libinput.libinput_log_set_handler.argtypes = (c_void_p, c_void_p)
	_libinput.libinput_log_set_handler.restype = None
	_libinput.libinput_log_set_priority.argtypes = (c_void_p, LogPriority)
	_libinput.libinput_log_set_priority.restype = None
	_libinput.libinput_get_fd.argtypes = (c_void_p,)
	_libinput.libinput_get_fd.restype = c_int
	_libinput.libinput_suspend.argtypes = (c_void_p,)
	_libinput.libinput_suspend.restype = None
	_libinput.libinput_resume.argtypes = (c_void_p,)
	_libinput.libinput_resume.restype = c_int
	_libinput.libinput_path_add_device.argtypes = (c_void_p, c_char_p)
	_libinput.libinput_path_add_device.restype = c_void_p
	_libinput.libinput_path_remove_device.argtypes = (c_void_p,)
	_libinput.libinput_path_remove_device.restype = None
	_libinput.libinput_dispatch.argtypes = (c_void_p,)
	_libinput.libinput_dispatch.restype = c_int
	_libinput.libinput_get_event.argtypes = (c_void_p,)
	_libinput.libinput_get_event.restype = c_void_p

	def __init__(self, udev=False, grab=False, debug=False):
		"""Initialize context.

		Args:
			udev (bool): If true devices are added/removed from udev seat. If
				false devices have to be added/removed manually.
			grab (bool): If true get exclusive access to device(s).
				Note:
					Grabbing an already grabbed device raises :exc:`OSError`
			debug (bool): If false, only errors are printed.
		"""

		self._selector = DefaultSelector()
		self._interface = Interface()
		if udev:
			self.udev = True
			self._udev = self._libudev.udev_new()
			self._li = self._libinput.libinput_udev_create_context(
				byref(self._interface), grab, self._udev)
		else:
			self.udev = False
			self._li = self._libinput.libinput_path_create_context(
				byref(self._interface), grab)
		self._log_handler = lambda pr, strn: print(pr.name, ': ', strn)
		self._set_default_log_handler()
		if debug:
			self._libinput.libinput_log_set_priority(
				self._li, LogPriority.DEBUG)
		self._selector.register(
			self._libinput.libinput_get_fd(self._li), EVENT_READ)

	def __del__(self):

		while self._libinput.libinput_unref(self._li):
			pass
		if self.udev:
			self._libudev.udev_unref(self._udev)

	def _set_default_log_handler(self):

		def default_log_handler(li, priority, fmt, args):

			string = create_string_buffer(2048)
			self._libc.vsprintf(string, fmt, args)
			self._log_handler(LogPriority(priority), string.value.decode())

		CMPFUNC = CFUNCTYPE(None, c_void_p, c_int, c_char_p, c_void_p)
		self._default_log_handler = CMPFUNC(default_log_handler)
		self._libinput.libinput_log_set_handler(
			self._li, self._default_log_handler)

	@property
	def log_handler(self):
		"""Callable that handles error/info/debug messages.

		Args:
			priority (~libinput.constant.LogPriority): Message priority.
			message (str): The message.
		Default handler prints messages to stdout.
		"""

		return self._log_handler

	@log_handler.setter
	def log_handler(self, handler):

		self._log_handler = handler

	def suspend(self):
		"""Suspend monitoring for new devices and close existing devices.

		This all but terminates libinput but does keep the context valid to be
		resumed with :meth:`resume`.
		"""

		self._libinput.libinput_suspend(self._li)

	def resume(self):
		"""Resume a suspended libinput context.

		This re-enables device monitoring and adds existing devices.

		Warning:
			Resuming udev context before assigning seat causes segfault.
		"""

		rc = self._libinput.libinput_resume(self._li)
		assert rc == 0, 'Failed to resume current context'

	def udev_assign_seat(self, seat):
		"""Assign a seat to this libinput context.

		New devices or the removal of existing devices will appear as events
		when iterating over :meth:`get_event`.

		:meth:`udev_assign_seat` succeeds even if no input devices are
		currently available on this seat, or if devices are available but fail
		to open. Devices that do not have the minimum capabilities to be
		recognized as pointer, keyboard or touch device are ignored. Such
		devices and those that failed to open are ignored until the next call
		to :meth:`resume`.

		Warning:
			This method may only be called once per context.
		Args:
			seat (str): A seat identifier.
		"""

		rc = self._libinput.libinput_udev_assign_seat(self._li, seat.encode())
		assert rc == 0, 'Failed to assign {}'.format(seat)

	def path_add_device(self, path):
		"""Add a device to a libinput context initialized with udev=False.

		If successful, the device will be added to the internal list and
		re-opened on :meth:`resume`. The device can be removed with
		:meth:`path_remove_device`.
		If the device was successfully initialized, it is returned.

		Args:
			path (str): Path to an input device.
		Returns:
			~libinput.define.Device: A device object or :obj:`None`.
		"""

		hdevice = self._libinput.libinput_path_add_device(
			self._li, path.encode())
		if hdevice:
			return Device(hdevice, self._libinput)
		return None

	def path_remove_device(self, device):
		"""Remove a device from a libinput context initialized udev=False.

		Events already processed from this input device are kept in the queue,
		the :attr:`~libinput.constant.Event.DEVICE_REMOVED` event marks the end
		of events for this device.

		If no matching device exists, this method does nothing.

		Args:
			Device (~libinput.define.Device): A previously added device.
		"""

		self._libinput.libinput_path_remove_device(device._handle)

	def get_event(self, timeout=None):
		"""Yield events from the internal libinput's queue.

		Yields generic :class:`~libinput.event.Event`, to get get device
		specific event objects call
		:meth:`~libinput.event.Event.get_pointer_event` or similar.

		If *timeout* is positive integer, the generator will only block for
		*timeout* seconds when there are no events. If *timeout* is
		:obj:`None` (default) the generator will block indefinitely.

		Args:
			timeout (int): Seconds to block when there are no events.
		Yields:
			:class:`~libinput.event.Event`: A generic event.
		"""

		if timeout:
			start = monotonic()
		while True:
			events = self._selector.select(timeout=timeout)
			for nevent in range(len(events) + 1):
				self._libinput.libinput_dispatch(self._li)
				hevent = self._libinput.libinput_get_event(self._li)
				if hevent:
					event = Event(hevent, self._libinput)
					self._libinput.libinput_dispatch(self._li)
					if timeout:
						start = monotonic()
					yield event
			if not events and timeout:
				delta = monotonic() - start
				if start >= timeout:
					raise StopIteration(
						'No events for {} seconds'.format(timeout))
