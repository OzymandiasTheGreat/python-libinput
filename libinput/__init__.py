#!/usr/bin/env python3

import time
from selectors import DefaultSelector, EVENT_READ
from ctypes import CDLL, POINTER, byref, CFUNCTYPE, create_string_buffer
from ctypes import c_int, c_char_p, c_void_p
from .define import Interface, Device
from .constant import LogPriority
from .event import Event


class LibInput(object):

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
	# ~ _libinput.libinput_set_user_data.argtypes = (c_void_p, POINTER(c_int))
	# ~ _libinput.libinput_set_user_data.restype = None
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

	def __init__(self, *, udev=False, grab=False, debug=False):

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
		# ~ print(c_int(grab))
		# ~ self._libinput.libinput_set_user_data(self._li, byref(c_int(grab)))
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

		return self._log_handler

	@log_handler.setter
	def log_handler(self, handler):

		self._log_handler = handler

	def suspend(self):

		self._libinput.libinput_suspend(self._li)

	def resume(self):

		rc = self._libinput.libinput_resume(self._li)
		assert rc == 0, 'Failed to resume current context'

	def udev_assign_seat(self, seat):

		rc = self._libinput.libinput_udev_assign_seat(self._li, seat.encode())
		assert rc == 0, 'Failed to assign {}'.format(seat)

	def path_add_device(self, path):

		hdevice = self._libinput.libinput_path_add_device(
			self._li, path.encode())
		return Device(hdevice, self._libinput)

	def path_remove_device(self, device):

		self._libinput.libinput_path_remove_device(device._handle)

	def get_event(self, timeout=None):

		if timeout:
			start = time.monotonic()
		while True:
			events = self._selector.select(timeout=timeout)
			for nevent in range(len(events) + 1):
				self._libinput.libinput_dispatch(self._li)
				hevent = self._libinput.libinput_get_event(self._li)
				if hevent:
					event = Event(hevent, self._libinput)
					self._libinput.libinput_dispatch(self._li)
					if timeout:
						start = time.monotonic()
					yield event
			if not events and timeout:
				delta = time.monotonic() - start
				if start >= timeout:
					raise StopIteration(
						'No events for {} seconds'.format(timeout))
