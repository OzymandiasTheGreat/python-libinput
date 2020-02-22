#!/usr/bin/env python3

from __future__ import absolute_import, print_function
from ctypes import CDLL, POINTER, byref, CFUNCTYPE, create_string_buffer
from ctypes import c_int, c_char_p, c_void_p
# ~ try:
	# ~ from time import monotonic
# ~ except ImportError:
	# ~ from monotonic import monotonic
try:
	from selectors import DefaultSelector, EVENT_READ
except ImportError:
	from selectors34 import DefaultSelector, EVENT_READ
from .version import __version__
from .define import Interface
from .device import Device
from .constant import LogPriority, ContextType, EventType, DeviceCapability
from .constant import KeyState, Led, ButtonState, PointerAxis
from .constant import PointerAxisSource, TabletPadRingAxisSource
from .constant import TabletPadStripAxisSource, TabletToolType
from .constant import TabletToolProximityState, TabletToolTipState, SwitchState
from .constant import Switch, ConfigStatus, TapState, TapButtonMap, DragState
from .constant import DragLockState, SendEventsMode, AccelProfile, ClickMethod
from .constant import MiddleEmulationState, ScrollMethod, DwtState
from .event import PointerEvent, KeyboardEvent, TouchEvent, GestureEvent
from .event import TabletToolEvent, TabletPadEvent, SwitchEvent
from .event import DeviceNotifyEvent


__all__ = ('LibInput', 'LogPriority', 'ContextType', 'EventType',
	'DeviceCapability', 'KeyState', 'Led', 'ButtonState', 'PointerAxis',
	'PointerAxisSource', 'TabletPadRingAxisSource', 'TabletPadStripAxisSource',
	'TabletToolType', 'TabletToolProximityState', 'TabletToolTipState',
	'SwitchState', 'Switch', 'ConfigStatus', 'TapState', 'TapButtonMap',
	'DragState', 'DragLockState', 'SendEventsMode', 'AccelProfile',
	'ClickMethod', 'MiddleEmulationState', 'ScrollMethod', 'DwtState')


class LibInput(object):
	"""A base/factory class for libinput context.

	Context is used to manage devices and get events.
	"""

	_libc = CDLL('libc.so.6')
	_libc.vsprintf.argtypes = (c_char_p, c_char_p, c_void_p)
	_libc.vsprintf.restype = c_int
	_libudev = CDLL('libudev.so.1')
	_libudev.udev_new.argtypes = None
	_libudev.udev_new.restype = c_void_p
	_libudev.udev_unref.argtypes = (c_void_p,)
	_libudev.udev_unref.restype = None
	# libinput is not available on RTD so we prevent failing immediately
	# when it's not available. Trying to instantiate the class will still
	# throw an exception.
	try:
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
		_libinput.libinput_event_get_type.argtypes = (c_void_p,)
		_libinput.libinput_event_get_type.restype = EventType

		_libinput.libinput_next_event_type.argtypes = (c_void_p,)
		_libinput.libinput_next_event_type.restype = c_int
	except OSError:
		pass

	def __new__(cls, context_type=ContextType.PATH, debug=False):

		if context_type == ContextType.PATH:
			return LibInputPath()
		elif context_type == ContextType.UDEV:
			return LibInputUdev()
		else:
			raise TypeError('Unsupported context type')

	def __init__(self, context_type=ContextType.PATH, debug=False):
		"""Initialize context.

		Args:
			context_type (~libinput.constant.ContextType): If
				:attr:`~libinput.constant.ContextType.UDEV` devices are
				added/removed from udev seat. If
				:attr:`~libinput.constant.ContextType.PATH` devices have to be
				added/removed manually.
			debug (bool): If false, only errors are printed.
		"""

		self._selector = DefaultSelector()
		self._interface = Interface()
		if context_type == ContextType.UDEV:
			self._udev = self._libudev.udev_new()
			self._li = self._libinput.libinput_udev_create_context(
				byref(self._interface), None, self._udev)
		elif context_type == ContextType.PATH:
			self._li = self._libinput.libinput_path_create_context(
				byref(self._interface), None)
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
		"""

		rc = self._libinput.libinput_resume(self._li)
		assert rc == 0, 'Failed to resume current context'

	@property
	def events(self):
		"""Yield events from the internal libinput's queue.

		Yields device events that are subclasses of
		:class:`~libinput.event.Event`.

		Yields:
			:class:`~libinput.event.Event`: Device event.
		"""

		while True:
			self._selector.select()
			self._libinput.libinput_dispatch(self._li)
			while True:
				hevent = self._libinput.libinput_get_event(self._li)
				if not hevent:
					break
				type_ = self._libinput.libinput_event_get_type(hevent)
				self._libinput.libinput_dispatch(self._li)
				if type_.is_pointer():
					yield PointerEvent(hevent, self._libinput)
				elif type_.is_keyboard():
					yield KeyboardEvent(hevent, self._libinput)
				elif type_.is_touch():
					yield TouchEvent(hevent, self._libinput)
				elif type_.is_gesture():
					yield GestureEvent(hevent, self._libinput)
				elif type_.is_tablet_tool():
					yield TabletToolEvent(hevent, self._libinput)
				elif type_.is_tablet_pad():
					yield TabletPadEvent(hevent, self._libinput)
				elif type_.is_switch():
					yield SwitchEvent(hevent, self._libinput)
				elif type_.is_device():
					yield DeviceNotifyEvent(hevent, self._libinput)

	def next_event_type(self):
		"""Return the type of the next event in the internal queue.

		This method does not pop the event off the queue and the next call
		to :attr:`events` returns that event.

		Returns:
			~libinput.constant.EventType: The event type of the next available
			event or :obj:`None` if no event is available.
		"""

		type_ = self._libinput.libinput_next_event_type(self._li)
		if type_ == 0:
			return None
		else:
			return EventType(type_)


class LibInputPath(LibInput):
	"""libinput path context.

	For a context of this type, devices have to be added/removed manually with
	:meth:`add_device` and :meth:`remove_device` respectively.

	Note:
		Do not instanciate this class directly, instead call :class:`.LibInput`
		with ``context_type`` :attr:`~libinput.constant.ContextType.PATH`.
	"""

	def __new__(cls, *args, **kwargs):

		return object.__new__(cls)

	def __init__(self, *args, **kwargs):

		LibInput.__init__(self, *args, **kwargs)

	def add_device(self, path):
		"""Add a device to a libinput context.

		If successful, the device will be added to the internal list and
		re-opened on :meth:`~libinput.LibInput.resume`. The device can be
		removed with :meth:`remove_device`.
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

	def remove_device(self, device):
		"""Remove a device from a libinput context.

		Events already processed from this input device are kept in the queue,
		the :attr:`~libinput.constant.EventType.DEVICE_REMOVED` event marks
		the end of events for this device.

		If no matching device exists, this method does nothing.

		Args:
			Device (~libinput.define.Device): A previously added device.
		"""

		self._libinput.libinput_path_remove_device(device._handle)


class LibInputUdev(LibInput):
	"""libinput udev context.

	For a context of this type, devices are added/removed automatically from
	the assigned seat.

	Note:
		Do not instanciate this class directly, instead call :class:`.LibInput`
		with ``context_type`` :attr:`~libinput.constant.ContextType.UDEV`.
	"""

	def __new__(cls, *args, **kwargs):

		return object.__new__(cls)

	def __init__(self, *args, **kwargs):

		LibInput.__init__(self, *args, **kwargs)

	def __del__(self):

		self._libudev.udev_unref(self._udev)

	def assign_seat(self, seat):
		"""Assign a seat to this libinput context.

		New devices or the removal of existing devices will appear as events
		when iterating over :meth:`~libinput.LibInput.get_event`.

		:meth:`assign_seat` succeeds even if no input devices are
		currently available on this seat, or if devices are available but fail
		to open. Devices that do not have the minimum capabilities to be
		recognized as pointer, keyboard or touch device are ignored. Such
		devices and those that failed to open are ignored until the next call
		to :meth:`~libinput.LibInput.resume`.

		Warning:
			This method may only be called once per context.
		Args:
			seat (str): A seat identifier.
		"""

		rc = self._libinput.libinput_udev_assign_seat(self._li, seat.encode())
		assert rc == 0, 'Failed to assign {}'.format(seat)
