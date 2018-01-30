#!/usr/bin/env python3

import os
from fcntl import ioctl
from ctypes import Structure, CFUNCTYPE, string_at, POINTER, byref
from ctypes import c_int, c_char_p, c_void_p, c_uint, c_bool, c_double
from ctypes import c_uint32, c_uint64, c_float
from ctypes import sizeof
from .constant import Led, DeviceCapability, TabletToolType
from .constant import ConfigStatus, TapState, TapButtonMap, DragState
from .constant import DragLockState, SendEventsMode, AccelProfile, ClickMethod
from .constant import MiddleEmulationState, ScrollMethod, DwtState
from .event_codes import Key, Button

_IOCPARM_MASK = 0x1FFF
_IOC_IN = 0x40000000


def _IOW(magic, command, type_):

	return (
		(magic << 8)
		| command
		| ((sizeof(type_) & _IOCPARM_MASK) << 16)
		| _IOC_IN)


EVIOCGRAB = _IOW(ord('E'), 0x90, c_int)


class Interface(object):

	class Interface(Structure):

		_fields_ = (
			('open_restricted', CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)),
			('close_restricted', CFUNCTYPE(None, c_int, c_void_p)))

	def __new__(self):

		return self.Interface(self.open_restricted(), self.close_restricted())

	@classmethod
	def open_restricted(cls):

		def open_restricted(path, flags, user_data):

			fd = os.open(path, flags)
			if user_data:
				ioctl(fd, EVIOCGRAB, 1)
			return fd

		CMPFUNC = CFUNCTYPE(c_int, c_char_p, c_int, c_void_p)
		return CMPFUNC(open_restricted)

	@classmethod
	def close_restricted(cls):

		def close_restricted(fd, user_data):

			os.close(fd)

		CMPFUNC = CFUNCTYPE(None, c_int, c_void_p)
		return CMPFUNC(close_restricted)


class DeviceConfig(object):

	def __init__(self, hdevice, libinput):

		self._handle = hdevice
		self._libinput = libinput

		self._libinput.libinput_config_status_to_str.argtypes = (ConfigStatus,)
		self._libinput.libinput_config_status_to_str.restype = c_char_p
		self._libinput.libinput_device_config_tap_get_finger_count.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_tap_get_finger_count.restype = (
			c_int)
		self._libinput.libinput_device_config_tap_set_enabled.argtypes = (
			c_void_p, TapState)
		self._libinput.libinput_device_config_tap_set_enabled.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_tap_get_enabled.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_tap_get_enabled.restype = (
			TapState)
		self._libinput \
			.libinput_device_config_tap_get_default_enabled.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_tap_get_default_enabled.restype = TapState
		self._libinput.libinput_device_config_tap_set_button_map.argtypes = (
			c_void_p, TapButtonMap)
		self._libinput.libinput_device_config_tap_set_button_map.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_tap_get_button_map.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_tap_get_button_map.restype = (
			TapButtonMap)
		self._libinput \
			.libinput_device_config_tap_get_default_button_map.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_tap_get_default_button_map.restype = (
				TapButtonMap)
		self._libinput.libinput_device_config_tap_set_drag_enabled.argtypes = (
			c_void_p, DragState)
		self._libinput.libinput_device_config_tap_set_drag_enabled.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_tap_get_drag_enabled.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_tap_get_drag_enabled.restype = (
			DragState)
		self._libinput \
			.libinput_device_config_tap_get_default_drag_enabled.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_tap_get_default_drag_enabled.restype = (
				DragState)
		self._libinput \
			.libinput_device_config_tap_set_drag_lock_enabled.argtypes = (
				c_void_p, DragLockState)
		self._libinput \
			.libinput_device_config_tap_set_drag_lock_enabled.restype = (
				ConfigStatus)
		self._libinput \
			.libinput_device_config_tap_get_drag_lock_enabled.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_tap_get_drag_lock_enabled.restype = (
				DragLockState)
		self._libinput \
			.libinput_device_config_tap_get_default_drag_lock_enabled.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_tap_get_default_drag_lock_enabled.restype = (
				DragLockState)
		self._libinput.libinput_device_config_calibration_has_matrix.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_calibration_has_matrix.restype = (
			c_bool)
		self._libinput.libinput_device_config_calibration_set_matrix.argtypes = (
			c_void_p, c_float * 6)
		self._libinput.libinput_device_config_calibration_set_matrix.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_calibration_get_matrix.argtypes = (
			c_void_p, c_float * 6)
		self._libinput.libinput_device_config_calibration_get_matrix.restype = (
			c_bool)
		self._libinput \
			.libinput_device_config_calibration_get_default_matrix.argtypes = (
				c_void_p, c_float * 6)
		self._libinput \
			.libinput_device_config_calibration_get_default_matrix.restype = (
				c_bool)
		self._libinput.libinput_device_config_send_events_get_modes.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_send_events_get_modes.restype = (
			SendEventsMode)
		self._libinput.libinput_device_config_send_events_set_mode.argtypes = (
			c_void_p, SendEventsMode)
		self._libinput.libinput_device_config_send_events_set_mode.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_send_events_get_mode.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_send_events_get_mode.restype = (
			SendEventsMode)
		self._libinput \
			.libinput_device_config_send_events_get_default_mode.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_send_events_get_default_mode.restype = (
				SendEventsMode)
		self._libinput.libinput_device_config_accel_is_available.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_accel_is_available.restype = (
			c_bool)
		self._libinput.libinput_device_config_accel_set_speed.argtypes = (
			c_void_p, c_double)
		self._libinput.libinput_device_config_accel_set_speed.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_accel_get_speed.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_accel_get_speed.restype = (
			c_double)
		self._libinput.libinput_device_config_accel_get_default_speed.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_accel_get_default_speed.restype = (
			c_double)
		self._libinput.libinput_device_config_accel_get_profiles.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_accel_get_profiles.restype = (
			AccelProfile)
		self._libinput.libinput_device_config_accel_set_profile.argtypes = (
			c_void_p, AccelProfile)
		self._libinput.libinput_device_config_accel_set_profile.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_accel_get_profile.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_accel_get_profile.restype = (
			AccelProfile)
		self._libinput \
			.libinput_device_config_accel_get_default_profile.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_accel_get_default_profile.restype = (
				AccelProfile)
		self._libinput \
			.libinput_device_config_scroll_has_natural_scroll.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_scroll_has_natural_scroll.restype = c_bool
		self._libinput \
			.libinput_device_config_scroll_set_natural_scroll_enabled.argtypes = (
				c_void_p, c_bool)
		self._libinput \
			.libinput_device_config_scroll_set_natural_scroll_enabled.restype = (
				ConfigStatus)
		self._libinput \
			.libinput_device_config_scroll_get_natural_scroll_enabled.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_scroll_get_natural_scroll_enabled.restype = (
				c_bool)
		self._libinput \
			.libinput_device_config_scroll_get_default_natural_scroll_enabled \
			.argtypes = (c_void_p,)
		self._libinput \
			.libinput_device_config_scroll_get_default_natural_scroll_enabled \
			.restype = c_bool
		self._libinput.libinput_device_config_left_handed_is_available.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_left_handed_is_available.restype = (
			c_bool)
		self._libinput.libinput_device_config_left_handed_set.argtypes = (
			c_void_p, c_bool)
		self._libinput.libinput_device_config_left_handed_set.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_left_handed_get.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_left_handed_get.restype = c_bool
		self._libinput.libinput_device_config_left_handed_get_default.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_left_handed_get_default.restype = (
			c_bool)
		self._libinput.libinput_device_config_click_get_methods.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_click_get_methods.restype = (
			ClickMethod)
		self._libinput.libinput_device_config_click_set_method.argtypes = (
			c_void_p, ClickMethod)
		self._libinput.libinput_device_config_click_set_method.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_click_get_method.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_click_get_method.restype = (
			ClickMethod)
		self._libinput.libinput_device_config_click_get_default_method.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_click_get_default_method.restype = (
			ClickMethod)
		self._libinput \
			.libinput_device_config_middle_emulation_is_available.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_middle_emulation_is_available.restype = (
				c_bool)
		self._libinput \
			.libinput_device_config_middle_emulation_set_enabled.argtypes = (
				c_void_p, MiddleEmulationState)
		self._libinput \
			.libinput_device_config_middle_emulation_set_enabled.restype = (
				ConfigStatus)
		self._libinput \
			.libinput_device_config_middle_emulation_get_enabled.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_middle_emulation_get_enabled.restype = (
				MiddleEmulationState)
		self._libinput \
			.libinput_device_config_middle_emulation_get_default_enabled \
			.argtypes = (c_void_p,)
		self._libinput \
			.libinput_device_config_middle_emulation_get_default_enabled \
			.restype = MiddleEmulationState
		self._libinput.libinput_device_config_scroll_get_methods.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_scroll_get_methods.restype = (
			ScrollMethod)
		self._libinput.libinput_device_config_scroll_set_method.argtypes = (
			c_void_p, ScrollMethod)
		self._libinput.libinput_device_config_scroll_set_method.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_scroll_get_method.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_scroll_get_method.restype = (
			ScrollMethod)
		self._libinput \
			.libinput_device_config_scroll_get_default_method.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_scroll_get_default_method.restype = (
				ScrollMethod)
		self._libinput.libinput_device_config_scroll_set_button.argtypes = (
			c_void_p, Button)
		self._libinput.libinput_device_config_scroll_set_button.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_scroll_get_button.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_scroll_get_button.restype = (
			Button)
		self._libinput \
			.libinput_device_config_scroll_get_default_button.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_scroll_get_default_button.restype = Button
		self._libinput.libinput_device_config_dwt_is_available.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_dwt_is_available.restype = c_bool
		self._libinput.libinput_device_config_dwt_set_enabled.argtypes = (
			c_void_p, DwtState)
		self._libinput.libinput_device_config_dwt_set_enabled.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_dwt_get_enabled.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_dwt_get_enabled.restype = (
			DwtState)
		self._libinput.libinput_device_config_dwt_get_default_enabled.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_dwt_get_default_enabled.restype = (
			DwtState)
		self._libinput.libinput_device_config_rotation_is_available.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_rotation_is_available.restype = (
			c_bool)
		self._libinput.libinput_device_config_rotation_set_angle.argtypes = (
			c_void_p, c_uint)
		self._libinput.libinput_device_config_rotation_set_angle.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_rotation_get_angle.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_rotation_get_angle.restype = (
			c_uint)
		self._libinput \
			.libinput_device_config_rotation_get_default_angle.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_rotation_get_default_angle.restype = c_uint

	def config_status_to_str(self, status):

		pchar = self._libinput.libinput_config_status_to_str(status)
		return string_at(pchar)

	def config_tap_get_finger_count(self):

		return self._libinput.libinput_device_config_tap_get_finger_count(
			self._handle)

	def config_tap_set_enabled(self, state):

		return self._libinput.libinput_device_config_tap_set_enabled(
			self._handle, state)

	def config_tap_get_enabled(self):

		return self._libinput.libinput_device_config_tap_get_enabled(
			self._handle)

	def config_tap_get_default_enabled(self):

		return self._libinput.libinput_device_config_tap_get_default_enabled(
			self._handle)

	def config_tap_set_button_map(self, button_map):

		return self._libinput.libinput_device_config_tap_set_button_map(
			self._handle, button_map)

	def config_tap_get_button_map(self):

		return self._libinput.libinput_device_config_tap_get_button_map(
			self._handle)

	def config_tap_get_default_button_map(self):

		return self._libinput.libinput_device_config_tap_get_default_button_map(
			self._handle)

	def config_tap_set_drag_enabled(self, state):

		return self._libinput.libinput_device_config_tap_set_drag_enabled(
			self._handle, state)

	def config_tap_get_drag_enabled(self):

		return self._libinput.libinput_device_config_tap_get_drag_enabled(
			self._handle)

	def config_tap_get_default_drag_enabled(self):

		return self._libinput \
			.libinput_device_config_tap_get_default_drag_enabled(self._handle)

	def config_tap_set_drag_lock_enabled(self, state):

		return self._libinput.libinput_device_config_tap_set_drag_lock_enabled(
			self._handle, state)

	def config_tap_get_drag_lock_enabled(self):

		return self._libinput.libinput_device_config_tap_get_drag_lock_enabled(
			self._handle)

	def config_tap_get_default_drag_lock_enabled(self):

		return self._libinput \
			.libinput_device_config_tap_get_default_drag_lock_enabled(
				self._handle)

	def config_calibration_has_matrix(self):

		return self._libinput.libinput_device_config_calibration_has_matrix(
			self._handle)

	def config_calibration_set_matrix(self, matrix):

		matrix = (c_float * 6)(*matrix)
		return self._libinput.libinput_device_config_calibration_set_matrix(
			self._handle, matrix)

	def config_calibration_get_matrix(self):

		matrix = (c_float * 6)()
		rc = self._libinput.libinput_device_config_calibration_get_matrix(
			self._handle, matrix)
		return rc, matrix

	def config_calibration_get_default_matrix(self):

		matrix = (c_float * 6)()
		rc = self._libinput \
			.libinput_device_config_calibration_get_default_matrix(
				self._handle, matrix)
		return rc, matrix

	def config_send_events_get_modes(self):

		return self._libinput.libinput_device_config_send_events_get_modes(
			self._handle)

	def config_send_events_set_mode(self, mode):

		return self._libinput.libinput_device_config_send_events_set_mode(
			self._handle, mode)

	def config_send_events_get_mode(self):

		return self._libinput.libinput_device_config_send_events_get_mode(
			self._handle)

	def config_send_events_get_default_mode(self):

		return self._libinput \
			.libinput_device_config_send_events_get_default_mode(self._handle)

	def config_accel_is_available(self):

		return self._libinput.libinput_device_config_accel_is_available(
			self._handle)

	def config_accel_set_speed(self, speed):

		return self._libinput.libinput_device_config_accel_set_speed(
			self._handle, speed)

	def config_accel_get_speed(self):

		return self._libinput.libinput_device_config_accel_get_speed(
			self._handle)

	def config_accel_get_default_speed(self):

		return self._libinput.libinput_device_config_accel_get_default_speed(
			self._handle)

	def config_accel_get_profiles(self):

		return self._libinput.libinput_device_config_accel_get_profiles(
			self._handle)

	def config_accel_set_profile(self, profile):

		return self._libinput.libinput_device_config_accel_set_profile(
			self._handle, profile)

	def config_accel_get_profile(self):

		return self._libinput.libinput_device_config_accel_get_profile(
			self._handle)

	def config_accel_get_default_profile(self):

		return self._libinput.libinput_device_config_accel_get_default_profile(
			self._handle)

	def config_scroll_has_natural_scroll(self):

		return self._libinput.libinput_device_config_scroll_has_natural_scroll(
			self._handle)

	def config_scroll_set_natural_scroll_enabled(self, enable):

		return self._libinput \
			.libinput_device_config_scroll_set_natural_scroll_enabled(
				self._handle, enable)

	def config_scroll_get_natural_scroll_enabled(self):

		return self._libinput \
			.libinput_device_config_scroll_get_natural_scroll_enabled(
				self._handle)

	def config_scroll_get_default_natural_scroll_enabled(self):

		return self._libinput \
			.libinput_device_config_scroll_get_default_natural_scroll_enabled(
				self._handle)

	def config_left_handed_is_available(self):

		return self._libinput.libinput_device_config_left_handed_is_available(
			self._handle)

	def config_left_handed_set(self, enable):

		return self._libinput.libinput_device_config_left_handed_set(
			self._handle, enable)

	def config_left_handed_get(self):

		return self._libinput.libinput_device_config_left_handed_get(
			self._handle)

	def config_left_handed_get_default(self):

		return self._libinput.libinput_device_config_left_handed_get_default(
			self._handle)

	def config_click_get_methods(self):

		return self._libinput.libinput_device_config_click_get_methods(
			self._handle)

	def config_click_set_method(self, method):

		return self._libinput.libinput_device_config_click_set_method(
			self._handle, method)

	def config_click_get_method(self):

		return self._libinput.libinput_device_config_click_get_method(
			self._handle)

	def config_click_get_default_method(self):

		return self._libinput.libinput_device_config_click_get_default_method(
			self._handle)

	def config_middle_emulation_is_available(self):

		return self._libinput \
			.libinput_device_config_middle_emulation_is_available(self._handle)

	def config_middle_emulation_set_enabled(self, state):

		return self._libinput \
			.libinput_device_config_middle_emulation_set_enabled(
				self._handle, state)

	def config_middle_emulation_get_enabled(self):

		return self._libinput \
			.libinput_device_config_middle_emulation_get_enabled(self._handle)

	def config_middle_emulation_get_default_enabled(self):

		return self._libinput \
			.libinput_device_config_middle_emulation_get_default_enabled(
				self._handle)

	def config_scroll_get_methods(self):

		return self._libinput.libinput_device_config_scroll_get_methods(
			self._handle)

	def config_scroll_set_method(self, method):

		return self._libinput.libinput_device_config_scroll_set_method(
			self._handle, method)

	def config_scroll_get_method(self):

		return self._libinput.libinput_device_config_scroll_get_method(
			self._handle)

	def config_scroll_get_default_method(self):

		return self._libinput.libinput_device_config_scroll_get_default_method(
			self._handle)

	def config_scroll_set_button(self, button):

		return self._libinput.libinput_device_config_scroll_set_button(
			self._handle, button)

	def config_scroll_get_button(self):

		return self._libinput.libinput_device_config_scroll_get_button(
			self._handle)

	def config_scroll_get_default_button(self):

		return self._libinput.libinput_device_config_scroll_get_default_button(
			self._handle)

	def config_dwt_is_available(self):

		return self._libinput.libinput_device_config_dwt_is_available(
			self._handle)

	def config_dwt_set_enabled(self, state):

		return self._libinput.libinput_device_config_dwt_set_enabled(
			self._handle, state)

	def config_dwt_get_enabled(self):

		return self._libinput.libinput_device_config_dwt_get_enabled(
			self._handle)

	def config_dwt_get_default_enabled(self):

		return self._libinput.libinput_device_config_dwt_get_default_enabled(
			self._handle)

	def config_rotation_is_available(self):

		return self._libinput.libinput_device_config_rotation_is_available(
			self._handle)

	def config_rotation_set_angle(self, degrees_cw):

		return self._libinput.libinput_device_config_rotation_set_angle(
			self._handle, degrees_cw)

	def config_rotation_get_angle(self):

		return self._libinput.libinput_device_config_rotation_get_angle(
			self._handle)

	def config_rotation_get_default_angle(self):

		return self._libinput.libinput_device_config_rotation_get_default_angle(
			self._handle)


class Device(DeviceConfig):

	def __init__(self, hdevice, libinput):

		DeviceConfig.__init__(self, hdevice, libinput)

		self._libinput.libinput_device_ref.argtypes = (c_void_p,)
		self._libinput.libinput_device_ref.restype = c_void_p
		self._libinput.libinput_device_unref.argtypes = (c_void_p,)
		self._libinput.libinput_device_unref.restype = c_void_p
		self._libinput.libinput_device_get_sysname.argtypes = (c_void_p,)
		self._libinput.libinput_device_get_sysname.restype = c_char_p
		self._libinput.libinput_device_get_name.argtypes = (c_void_p,)
		self._libinput.libinput_device_get_name.restype = c_char_p
		self._libinput.libinput_device_get_id_product.argtypes = (c_void_p,)
		self._libinput.libinput_device_get_id_product.restype = c_uint
		self._libinput.libinput_device_get_id_vendor.argtypes = (c_void_p,)
		self._libinput.libinput_device_get_id_vendor.restype = c_uint
		self._libinput.libinput_device_get_seat.argtypes = (c_void_p,)
		self._libinput.libinput_device_get_seat.restype = c_void_p
		self._libinput.libinput_device_set_seat_logical_name.argtypes = (
			c_void_p, c_char_p)
		self._libinput.libinput_device_set_seat_logical_name = c_int
		self._libinput.libinput_device_get_udev_device.argtypes = (c_void_p,)
		self._libinput.libinput_device_get_udev_device.restype = c_void_p
		self._libinput.libinput_device_led_update.argtypes = (c_void_p, Led)
		self._libinput.libinput_device_led_update.restype = None
		self._libinput.libinput_device_has_capability.argtypes = (
			c_void_p, DeviceCapability)
		self._libinput.libinput_device_has_capability.restype = c_bool
		self._libinput.libinput_device_get_size.argtypes = (
			c_void_p, POINTER(c_double), POINTER(c_double))
		self._libinput.libinput_device_get_size.restype = c_int
		self._libinput.libinput_device_pointer_has_button.argtypes = (
			c_void_p, Button)
		self._libinput.libinput_device_pointer_has_button.restype = c_int
		self._libinput.libinput_device_keyboard_has_key.argtypes = (
			c_void_p, Key)
		self._libinput.libinput_device_keyboard_has_key.restype = c_int
		self._libinput.libinput_device_tablet_pad_get_num_buttons.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_tablet_pad_get_num_buttons.restype = (
			c_int)
		self._libinput.libinput_device_tablet_pad_get_num_rings.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_tablet_pad_get_num_rings.restype = c_int
		self._libinput.libinput_device_tablet_pad_get_num_strips.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_tablet_pad_get_num_strips.restype = (
			c_int)
		self._libinput \
			.libinput_device_tablet_pad_get_num_mode_groups.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_tablet_pad_get_num_mode_groups.restype = c_int
		self._libinput.libinput_device_tablet_pad_get_mode_group.argtypes = (
			c_void_p, c_uint)
		self._libinput.libinput_device_tablet_pad_get_mode_group.restype = (
			c_void_p)

		self._libinput.libinput_device_ref(self._handle)

	def __del__(self):

		self._libinput.libinput_device_unref(self._handle)

	def __eq__(self, other):

		if isinstance(other, type(self)):
			return self._handle == other._handle
		else:
			return NotImplemented

	def get_sysname(self):

		pchar = self._libinput.libinput_device_get_sysname(self._handle)
		return string_at(pchar).decode()

	def get_name(self):

		pchar = self._libinput.libinput_device_get_name(self._handle)
		return string_at(pchar).decode()

	def get_id_product(self):

		return self._libinput.libinput_device_get_id_product(self._handle)

	def get_id_vendor(self):

		return self._libinput.libinput_device_get_id_vendor(self._handle)

	def get_seat(self):

		hseat = self._libinput.libinput_device_get_seat(self._handle)
		return Seat(hseat, self._libinput)

	def set_seat_logical_name(self, seat):

		rc = self._libinput.libinput_device_set_seat_logical_name(
			self._handle, seat.encode())
		assert rc == 0, 'Cannot assign device to {}'.format(seat)

	def get_udev_device(self):

		return self._libinput.libinput_device_get_udev_device(self._handle)

	def led_update(self, leds):

		self._libinput.libinput_device_led_update(self._handle, leds)

	def has_capability(self, capability):

		return self._libinput.libinput_device_has_capability(
			self._handle, capability)

	def get_size(self):

		width = c_double(0)
		height = c_double(0)
		rc = self._libinput.libinput_device_get_size(
			self._handle, byref(width), byref(height))
		if not rc:
			return True, width.value, height.value
		else:
			return False, 0.0, 0.0

	def pointer_has_button(self, button):

		rc = self._libinput.libinput_device_pointer_has_button(
			self._handle, button)
		assert rc >= 0, 'Device is not a pointer device'
		return bool(rc)

	def keyboard_has_key(self, key):

		rc = self._libinput.libinput_device_keyboard_has_key(
			self._handle, key)
		assert rc >= 0, 'Device is not a keyboard device'
		return bool(rc)

	def tablet_pad_get_num_buttons(self):

		num = self._libinput.libinput_device_tablet_pad_get_num_buttons(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'
		return num

	def tablet_pad_get_num_rings(self):

		num = self._libinput.libinput_device_tablet_pad_get_num_rings(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'
		return num

	def tablet_pad_get_num_strips(self):

		num = self._libinput.libinput_device_tablet_pad_get_num_strips(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'
		return num

	def tablet_pad_get_num_mode_groups(self):

		num = self._libinput.libinput_device_tablet_pad_get_num_mode_groups(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'

	def tablet_pad_get_mode_group(self, group):

		hmodegroup = self._libinput.libinput_device_tablet_pad_get_mode_group(
			self._handle, group)
		return TabletPadModeGroup(hmodegroup, self._libinput)


class Seat(object):

	def __init__(self, hseat, libinput):

		self._handle = hseat
		self._libinput = libinput

		self._libinput.libinput_seat_ref.argtypes = (c_void_p,)
		self._libinput.libinput_seat_ref.restype = c_void_p
		self._libinput.libinput_seat_unref.argtypes = (c_void_p,)
		self._libinput.libinput_seat_unref.restype = c_void_p
		self._libinput.libinput_seat_get_physical_name.argtypes = (c_void_p,)
		self._libinput.libinput_seat_get_physical_name.restype = c_char_p
		self._libinput.libinput_seat_get_logical_name.argtypes = (c_void_p,)
		self._libinput.libinput_seat_get_logical_name.restype = c_char_p

		self._libinput.libinput_seat_ref(self._handle)

	def __del__(self):

		self._libinput.libinput_seat_unref(self._handle)

	def __eq__(self, other):

		if isinstance(other, type(self)):
			return self._handle == other._handle
		else:
			return NotImplemented

	def get_physical_name(self):

		pchar = self._libinput.libinput_seat_get_physical_name(self._handle)
		return string_at(pchar).decode()

	def get_logical_name(self):

		pchar = self._libinput.libinput_seat_get_logical_name(self._handle)
		return string_at(pchar).decode()


class TabletTool(object):

	def __init__(self, htablettool, libinput):

		self._handle = htablettool
		self._libinput = libinput

		self._libinput.libinput_tablet_tool_ref.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_ref.restype = c_void_p
		self._libinput.libinput_tablet_tool_unref.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_unref.restype = c_void_p
		self._libinput.libinput_tablet_tool_get_type.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_get_type.restype = TabletToolType
		self._libinput.libinput_tablet_tool_get_tool_id.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_get_tool_id.restype = c_uint64
		self._libinput.libinput_tablet_tool_has_pressure.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_has_pressure.restype = c_bool
		self._libinput.libinput_tablet_tool_has_distance.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_has_distance.restype = c_bool
		self._libinput.libinput_tablet_tool_has_tilt.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_has_tilt.restype = c_bool
		self._libinput.libinput_tablet_tool_has_rotation.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_has_rotation.restype = c_bool
		self._libinput.libinput_tablet_tool_has_slider.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_has_slider.restype = c_bool
		self._libinput.libinput_tablet_tool_has_wheel.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_has_wheel.restype = c_bool
		self._libinput.libinput_tablet_tool_has_button.argtypes = (
			c_void_p, Button)
		self._libinput.libinput_tablet_tool_has_button.restype = c_bool
		self._libinput.libinput_tablet_tool_is_unique.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_is_unique.restype = c_bool
		self._libinput.libinput_tablet_tool_get_serial.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_tool_get_serial.restype = c_uint64

		self._libinput.libinput_tablet_tool_ref(self._handle)

	def __del__(self):

		self._libinput.libinput_tablet_tool_unref(self._handle)

	def __eq__(self, other):

		if isinstance(other, type(self)):
			return self._handle == other._handle
		else:
			return NotImplemented

	def get_type(self):

		return self._libinput.libinput_tablet_tool_get_type(self._handle)

	def get_tool_id(self):

		return self._libinput.libinput_tablet_tool_get_tool_id(self._handle)

	def has_pressure(self):

		return self._libinput.libinput_tablet_tool_has_pressure(self._handle)

	def has_distance(self):

		return self._libinput.libinput_tablet_tool_has_distance(self._handle)

	def has_tilt(self):

		return self._libinput.libinput_tablet_tool_has_tilt(self._handle)

	def has_rotation(self):

		return self._libinput.libinput_tablet_tool_has_rotation(self._handle)

	def has_slider(self):

		return self._libinput.libinput_tablet_tool_has_slider(self._handle)

	def has_wheel(self):

		return self._libinput.libinput_tablet_tool_has_wheel(self._handle)

	def has_button(self, button):

		return self._libinput.libinput_tablet_tool_has_button(
			self._handle, button)

	def is_unique(self):

		return self._libinput.libinput_tablet_tool_is_unique(self._handle)

	def get_serial(self):

		return self._libinput.libinput_tablet_tool_get_serial(self._handle)


class TabletPadModeGroup(object):

	def __init__(self, hmodegroup, libinput):

		self._handle = hmodegroup
		self._libinput = libinput

		self._libinput.libinput_tablet_pad_mode_group_ref.argtypes = (c_void_p,)
		self._libinput.libinput_tablet_pad_mode_group_ref.restype = c_void_p
		self._libinput.libinput_tablet_pad_mode_group_unref.argtypes = (
			c_void_p,)
		self._libinput.libinput_tablet_pad_mode_group_unref.restype = c_void_p
		self._libinput.libinput_tablet_pad_mode_group_get_index.argtypes = (
			c_void_p,)
		self._libinput.libinput_tablet_pad_mode_group_get_index.restype = (
			c_uint)
		self._libinput.libinput_tablet_pad_mode_group_get_num_modes.argtypes = (
			c_void_p,)
		self._libinput.libinput_tablet_pad_mode_group_get_num_modes.restype = (
			c_uint)
		self._libinput.libinput_tablet_pad_mode_group_get_mode.argtypes = (
			c_void_p,)
		self._libinput.libinput_tablet_pad_mode_group_get_mode.restype = c_uint
		self._libinput.libinput_tablet_pad_mode_group_has_button.argtypes = (
			c_void_p, c_uint32)
		self._libinput.libinput_tablet_pad_mode_group_has_button.restype = (
			c_bool)
		self._libinput.libinput_tablet_pad_mode_group_has_ring.argtypes = (
			c_void_p, c_uint)
		self._libinput.libinput_tablet_pad_mode_group_has_ring.restype = c_bool
		self._libinput.libinput_tablet_pad_mode_group_has_strip.argtypes = (
			c_void_p, c_uint)
		self._libinput.libinput_tablet_pad_mode_group_has_strip.restype = (
			c_bool)
		self._libinput \
			.libinput_tablet_pad_mode_group_button_is_toggle.argtypes = (
				c_void_p, c_uint)
		self._libinput \
			.libinput_tablet_pad_mode_group_button_is_toggle.restype = c_bool

		self._libinput.libinput_tablet_pad_mode_group_ref(self._handle)

	def __del__(self):

		self._libinput.libinput_tablet_pad_mode_group_unref(self._handle)

	def __eq__(self, other):

		if isinstance(other, type(self)):
			return self._handle == other._handle
		else:
			return NotImplemented

	def get_index(self):

		return self._libinput.libinput_tablet_pad_mode_group_get_index(
			self._handle)

	def get_num_modes(self):

		return self._libinput.libinput_tablet_pad_mode_group_get_num_modes(
			self._handle)

	def get_mode(self):

		return self._libinput.libinput_tablet_pad_mode_group_get_mode(
			self._handle)

	def has_button(self, button):

		return self._libinput.libinput_tablet_pad_mode_group_has_button(
			self._handle, button)

	def has_ring(self, ring):

		return self._libinput.libinput_tablet_pad_mode_group_has_ring(
			self._handle, ring)

	def has_strip(self, strip):

		return self._libinput.libinput_tablet_pad_mode_group_has_strip(
			self._handle, strip)

	def button_is_toggle(self, button):

		return self._libinput.libinput_tablet_pad_mode_group_button_is_toggle(
			self._handle, button)
