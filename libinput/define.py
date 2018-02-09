#!/usr/bin/env python3

from __future__ import absolute_import
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
from .evcodes import Key, Button

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
	"""A base class for :class:`.Device` providing configuration methods.
	"""

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
		"""Return a string describing the error.

		Args:
			status (~libinput.constant.ConfigStatus): The status to translate
				to a string.
		Returns:
			str: A human-readable string representing the error.
		"""

		pchar = self._libinput.libinput_config_status_to_str(status)
		return string_at(pchar)

	def config_tap_get_finger_count(self):
		"""Check if the device supports tap-to-click and how many fingers can
		be used for tapping.

		See :meth:`config_tap_set_enabled` for more information.

		Returns:
			int: The number of fingers that can generate a tap event, or 0 if
			the device does not support tapping.
		"""

		return self._libinput.libinput_device_config_tap_get_finger_count(
			self._handle)

	def config_tap_set_enabled(self, state):
		"""Enable or disable tap-to-click on this device, with
		a default mapping of 1, 2, 3 finger tap mapping to left, right, middle
		click, respectively.

		Tapping is limited by the number of simultaneous touches supported by the device, see libinput_device_config_tap_get_finger_count().

		Args:
			state (~libinput.constant.TapState):
				:attr:`~libinput.constant.TapState.ENABLED` to enable tapping
				or :attr:`~libinput.constant.TapState.DISABLED` to disable
				tapping.
		Returns:
			~libinput.constant.ConfigStatus: A config status code. Disabling
			tapping on a device that does not support tapping always succeeds.
		"""

		return self._libinput.libinput_device_config_tap_set_enabled(
			self._handle, state)

	def config_tap_get_enabled(self):
		"""Check if tap-to-click is enabled on this device.

		If the device does not support tapping, this method always returns
		:attr:`~libinput.constant.TapState.DISABLED`.

		Returns:
			~libinput.constant.TapState: Whether tapping is enabled or disabled.
		"""

		return self._libinput.libinput_device_config_tap_get_enabled(
			self._handle)

	def config_tap_get_default_enabled(self):
		"""Return the default setting for whether tap-to-click is enabled
		on this device.

		Returns:
			~libinput.constant.TapState: Whether tapping is enabled or disabled.
		"""

		return self._libinput.libinput_device_config_tap_get_default_enabled(
			self._handle)

	def config_tap_set_button_map(self, button_map):
		"""Set the finger number to button number mapping for tap-to-click.

		The default mapping on most devices is to have a 1, 2 and 3 finger tap
		to map to the left, right and middle button, respectively. A device may
		permit changing the button mapping but disallow specific maps. In this
		case :attr:`~libinput.constant.ConfigStatus.UNSUPPORTED` is returned,
		the caller is expected to handle this case correctly.

		Changing the button mapping may not take effect immediately, the device
		may wait until it is in a neutral state before applying any changes.

		The mapping may be changed when tap-to-click is disabled. The new
		mapping takes effect when tap-to-click is enabled in the future.

		Note:
			It is an application bug to call this method for devices where
			:meth:`config_tap_get_finger_count` returns 0.
		Args:
			button_map (~libinput.constant.TapButtonMap): The new
				finger-to-button number mapping.
		Returns:
			~libinput.constant.ConfigStatus: A config status code. Changing
			the order on a device that does not support tapping always fails
			with :attr:`~libinput.constant.ConfigStatus.UNSUPPORTED`.
		"""

		return self._libinput.libinput_device_config_tap_set_button_map(
			self._handle, button_map)

	def config_tap_get_button_map(self):
		"""Get the finger number to button number mapping for tap-to-click.

		The return value for a device that does not support tapping is always
		:attr:`~libinput.constant.TapButtonMap.LRM`.

		Note:
			It is an application bug to call this method for devices where
			:meth:`config_tap_get_finger_count` returns 0.
		Returns:
			~libinput.constant.TapButtonMap: The current finger-to-button
			number mapping.
		"""

		return self._libinput.libinput_device_config_tap_get_button_map(
			self._handle)

	def config_tap_get_default_button_map(self):
		"""Get the default finger number to button number mapping
		for tap-to-click.

		The return value for a device that does not support tapping is always
		:attr:`~libinput.constant.TapButtonMap.LRM`.

		Note:
			It is an application bug to call this method for devices where
			:meth:`config_tap_get_finger_count` returns 0.
		Returns:
			~libinput.constant.TapButtonMap: The current finger-to-button
			number mapping.
		"""

		return self._libinput.libinput_device_config_tap_get_default_button_map(
			self._handle)

	def config_tap_set_drag_enabled(self, state):
		"""Enable or disable tap-and-drag on this device.

		When enabled, a single-finger tap immediately followed by a finger down
		results in a button down event, subsequent finger motion thus triggers
		a drag. The button is released on finger up. See `Tap-and-drag`_
		for more details.

		Args:
			state (~libinput.constant.DragState):
				:attr:`~libinput.constant.DragState.ENABLED` to enable,
				:attr:`~libinput.constant.DragState.DISABLED` to disable
				tap-and-drag.
		Returns:
			~libinput.constant.ConfigStatus: Whether this method succeeds.
		"""

		return self._libinput.libinput_device_config_tap_set_drag_enabled(
			self._handle, state)

	def config_tap_get_drag_enabled(self):
		"""Return whether tap-and-drag is enabled or disabled on this device.

		Returns:
			~libinput.constant.DragState: Whether tap-and-drag is enabled.
		"""

		return self._libinput.libinput_device_config_tap_get_drag_enabled(
			self._handle)

	def config_tap_get_default_drag_enabled(self):
		"""Return whether tap-and-drag is enabled or disabled by default
		on this device.

		Returns:
			~libinput.constant.DragState: Whether tap-and-drag is enabled
			by default.
		"""

		return self._libinput \
			.libinput_device_config_tap_get_default_drag_enabled(self._handle)

	def config_tap_set_drag_lock_enabled(self, state):
		"""Enable or disable drag-lock during tapping on this device.

		When enabled, a finger may be lifted and put back on the touchpad
		within a timeout and the drag process continues. When disabled,
		lifting the finger during a tap-and-drag will immediately stop
		the drag. See `Tap-and-drag`_ for details.

		Enabling drag lock on a device that has tapping disabled is permitted,
		but has no effect until tapping is enabled.

		Args:
			state (~libinput.constant.DragLockState):
				:attr:`~libinput.constant.DragLockState.ENABLED` to enable
				drag lock or :attr:`~libinput.constant.DragLockState.DISABLED`
				to disable drag lock.
		Returns:
			~libinput.constant.ConfigStatus: A config status code. Disabling
			drag lock on a device that does not support tapping always succeeds.
		"""

		return self._libinput.libinput_device_config_tap_set_drag_lock_enabled(
			self._handle, state)

	def config_tap_get_drag_lock_enabled(self):
		"""Check if drag-lock during tapping is enabled on this device.

		If the device does not support tapping, this function always returns
		:attr:`~libinput.constant.DragLockState.DISABLED`.

		Drag lock may be enabled even when tapping is disabled.

		Returns:
			~libinput.constant.DragLockState: Whether drag lock is enabled.
		"""

		return self._libinput.libinput_device_config_tap_get_drag_lock_enabled(
			self._handle)

	def config_tap_get_default_drag_lock_enabled(self):
		"""Check if drag-lock during tapping is enabled by default
		on this device.

		If the device does not support tapping, this function always returns
		:attr:`~libinput.constant.DragLockState.DISABLED`.

		Drag lock may be enabled by default even when tapping is disabled
		by default.

		Returns:
			~libinput.constant.DragLockState: Whether drag lock is enabled
			by default.
		"""

		return self._libinput \
			.libinput_device_config_tap_get_default_drag_lock_enabled(
				self._handle)

	def config_calibration_has_matrix(self):
		"""Check if the device can be calibrated via a calibration matrix.

		Returns:
			bool: :obj:`True` if the device can be calibrated, :obj:`False`
			otherwise.
		"""

		return self._libinput.libinput_device_config_calibration_has_matrix(
			self._handle)

	def config_calibration_set_matrix(self, matrix):
		"""Apply the 3x3 transformation matrix to absolute device coordinates.

		This matrix has no effect on relative events.

		Given a 6-element array [a, b, c, d, e, f], the matrix is applied as
		::

			[ a  b  c ]   [ x ]
			[ d  e  f ] * [ y ]
			[ 0  0  1 ]   [ 1 ]

		The translation component (c, f) is expected to be normalized to
		the device coordinate range. For example, the matrix
		::

			[ 1 0  1 ]
			[ 0 1 -1 ]
			[ 0 0  1 ]

		moves all coordinates by 1 device-width to the right and
		1 device-height up.

		The rotation matrix for rotation around the origin is defined as
		::

			[ cos(a) -sin(a) 0 ]
			[ sin(a)  cos(a) 0 ]
			[   0      0     1 ]

		Note that any rotation requires an additional translation component
		to translate the rotated coordinates back into the original device
		space. The rotation matrixes for 90, 180 and 270 degrees clockwise are::

			90 deg cw:              180 deg cw:             270 deg cw:
			[ 0 -1 1]               [ -1  0 1]              [  0 1 0 ]
			[ 1  0 0]               [  0 -1 1]              [ -1 0 1 ]
			[ 0  0 1]               [  0  0 1]              [  0 0 1 ]

		Args:
			matrix (iterable): An array representing the first two rows of
				a 3x3 matrix as described above.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		matrix = (c_float * 6)(*matrix)
		return self._libinput.libinput_device_config_calibration_set_matrix(
			self._handle, matrix)

	def config_calibration_get_matrix(self):
		"""Return the current calibration matrix for this device.

		Returns:
			(bool, tuple): :obj:`False` if no calibration is set and
			the returned matrix is the identity matrix, :obj:`True`
			otherwise. :obj:`tuple` representing the first two rows of
			a 3x3 matrix as described
			in :meth:`config_calibration_set_matrix`.
		"""

		matrix = (c_float * 6)()
		rc = self._libinput.libinput_device_config_calibration_get_matrix(
			self._handle, matrix)
		return bool(rc), tuple(matrix)

	def config_calibration_get_default_matrix(self):
		"""Return the default calibration matrix for this device.

		On most devices, this is the identity matrix. If the udev property
		``LIBINPUT_CALIBRATION_MATRIX`` is set on the respective udev device,
		that property's value becomes the default matrix, see
		`Static device configuration via udev`_.

		Returns:
			(bool, tuple): :obj:`False` if no calibration is set and
			the returned matrix is the identity matrix, :obj:`True`
			otherwise. :obj:`tuple` representing the first two rows of
			a 3x3 matrix as described
			in :meth:`config_calibration_set_matrix`.
		"""

		matrix = (c_float * 6)()
		rc = self._libinput \
			.libinput_device_config_calibration_get_default_matrix(
				self._handle, matrix)
		return bool(rc), tuple(matrix)

	def config_send_events_get_modes(self):
		"""Return the possible send-event modes for this device.

		These modes define when a device may process and send events.

		Returns:
			~libinput.constant.SendEventsMode: A bitmask of possible modes.
		"""

		return self._libinput.libinput_device_config_send_events_get_modes(
			self._handle)

	def config_send_events_set_mode(self, mode):
		"""Set the send-event mode for this device.

		The mode defines when the device processes and sends events to
		the caller.

		The selected mode may not take effect immediately. Events already
		received and processed from this device are unaffected and will
		be passed to the caller on the next call to
		:meth:`~libinput.LibInput.get_event`.

		If the mode is a bitmask of :class:`~libinput.constant.SendEventsMode`,
		the device may wait for or generate events until it is in
		a neutral state. For example, this may include waiting for or
		generating button release events.

		If the device is already suspended, this function does nothing and
		returns success. Changing the send-event mode on a device that has
		been removed is permitted.

		Args:
			mode (~libinput.constant.SendEventsMode): A bitmask of
				send-events modes.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput.libinput_device_config_send_events_set_mode(
			self._handle, mode)

	def config_send_events_get_mode(self):
		"""Get the send-event mode for this device.

		The mode defines when the device processes and sends events to
		the caller.

		If a caller enables the bits for multiple modes, some of which are
		subsets of another mode libinput may drop the bits that are subsets.
		In other words, don't expect :meth:`config_send_events_get_mode` to
		always return exactly the same bitmask as passed into
		:meth:`config_send_events_set_mode`.

		Returns:
			~libinput.constant.SendEventsMode: The current bitmask of
			the send-event mode for this device.
		"""

		return self._libinput.libinput_device_config_send_events_get_mode(
			self._handle)

	def config_send_events_get_default_mode(self):
		"""Get the default send-event mode for this device.

		The mode defines when the device processes and sends events to
		the caller.

		Returns:
			~libinput.constant.SendEventsMode: The bitmask of
			the send-event mode for this device.
		"""

		return self._libinput \
			.libinput_device_config_send_events_get_default_mode(self._handle)

	def config_accel_is_available(self):
		"""Check if a device uses libinput-internal pointer-acceleration.

		Returns:
			bool: :obj:`False` if the device is not accelerated,
			:obj:`True` if it is accelerated
		"""

		return self._libinput.libinput_device_config_accel_is_available(
			self._handle)

	def config_accel_set_speed(self, speed):
		"""Set the pointer acceleration speed of this pointer device within
		a range of [-1, 1], where 0 is the default acceleration for
		this device, -1 is the slowest acceleration and 1 is the maximum
		acceleration available on this device.

		The actual pointer acceleration mechanism is implementation-dependent,
		as is the number of steps available within the range. libinput picks
		the semantically closest acceleration step if the requested value
		does not match a discrete setting.

		Args:
			speed (float): The normalized speed, in a range of [-1, 1].
		Returns:
			~libinput.constant.ConfigStatus: A config status code.

		"""

		return self._libinput.libinput_device_config_accel_set_speed(
			self._handle, speed)

	def config_accel_get_speed(self):
		"""Get the current pointer acceleration setting for
		this pointer device.

		The returned value is normalized to a range of [-1, 1]. See
		:meth:`config_accel_set_speed` for details.

		Returns:
			float: The current speed, range -1 to 1.
		"""

		return self._libinput.libinput_device_config_accel_get_speed(
			self._handle)

	def config_accel_get_default_speed(self):
		"""Return the default speed setting for this device, normalized to
		a range of [-1, 1].

		See :meth:`config_accel_set_speed` for details.

		Returns:
			float: The default speed setting for this device.
		"""

		return self._libinput.libinput_device_config_accel_get_default_speed(
			self._handle)

	def config_accel_get_profiles(self):
		"""Returns a bitmask of the configurable acceleration modes available
		on this device.

		Returns:
			~libinput.constant.AccelProfile: A bitmask of all configurable
			modes available on this device.
		"""

		return self._libinput.libinput_device_config_accel_get_profiles(
			self._handle)

	def config_accel_set_profile(self, profile):
		"""Set the pointer acceleration profile of this pointer device to
		the given mode.

		Args:
			profile (~libinput.constant.AccelProfile): The mode to set
			the device to.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput.libinput_device_config_accel_set_profile(
			self._handle, profile)

	def config_accel_get_profile(self):
		"""Get the current pointer acceleration profile for this pointer device.

		Returns:
			~libinput.constant.AccelProfile: The currently configured pointer
			acceleration profile.
		"""

		return self._libinput.libinput_device_config_accel_get_profile(
			self._handle)

	def config_accel_get_default_profile(self):
		"""Return the default pointer acceleration profile for
		this pointer device.

		Returns:
			~libinput.constant.AccelProfile: The default acceleration profile
			for this device.
		"""

		return self._libinput.libinput_device_config_accel_get_default_profile(
			self._handle)

	def config_scroll_has_natural_scroll(self):
		"""Return :obj:`True` if the device supports "natural scrolling".

		In traditional scroll mode, the movement of fingers on a touchpad
		when scrolling matches the movement of the scroll bars. When
		the fingers move down, the scroll bar moves down, a line of text on
		the screen moves towards the upper end of the screen. This also matches
		scroll wheels on mice (wheel down, content moves up).

		Natural scrolling is the term coined by Apple for inverted scrolling.
		In this mode, the effect of scrolling movement of fingers on a touchpad
		resemble physical manipulation of paper. When the fingers move down,
		a line of text on the screen moves down (scrollbars move up). This is
		the opposite of scroll wheels on mice.

		A device supporting natural scrolling can be switched between
		traditional scroll mode and natural scroll mode.

		Returns:
			bool: :obj:`False` if natural scrolling is not supported,
			:obj:`True` if natural scrolling is supported by this device.
		"""

		return self._libinput.libinput_device_config_scroll_has_natural_scroll(
			self._handle)

	def config_scroll_set_natural_scroll_enabled(self, enable):
		"""Enable or disable natural scrolling on the device.

		Args:
			enable (bool): :obj:`True` to enable, :obj:`False` to disable
				natural scrolling.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput \
			.libinput_device_config_scroll_set_natural_scroll_enabled(
				self._handle, enable)

	def config_scroll_get_natural_scroll_enabled(self):
		"""Get the current mode for scrolling on this device.

		Returns:
			bool: :obj:`False` if natural scrolling is disabled, :obj:`True`
			if enabled.
		"""

		return self._libinput \
			.libinput_device_config_scroll_get_natural_scroll_enabled(
				self._handle)

	def config_scroll_get_default_natural_scroll_enabled(self):
		"""Get the default mode for scrolling on this device.

		Returns:
			bool: :obj:`False` if natural scrolling is disabled by default,
			:obj:`True` if enabled.
		"""

		return self._libinput \
			.libinput_device_config_scroll_get_default_natural_scroll_enabled(
				self._handle)

	def config_left_handed_is_available(self):
		"""Check if a device has a configuration that supports left-handed
		usage.

		Returns:
			bool: :obj:`True` if the device can be set to left-handed,
			or :obj:`False` otherwise
		"""

		return self._libinput.libinput_device_config_left_handed_is_available(
			self._handle)

	def config_left_handed_set(self, enable):
		"""Set the left-handed configuration of the device.

		The exact behavior is device-dependent. On a mouse and most pointing
		devices, left and right buttons are swapped but the middle button is
		unmodified. On a touchpad, physical buttons (if present) are swapped.
		On a clickpad, the top and bottom software-emulated buttons are
		swapped where present, the main area of the touchpad remains a left
		button. Tapping and clickfinger behavior is not affected by this
		setting.

		Changing the left-handed configuration of a device may not take effect
		until all buttons have been logically released.

		Args:
			enable (bool): :obj:`False` to disable, :obj:`True` to enable
			left-handed mode.
		Returns:
			~libinput.constant.ConfigStatus: A configuration status code.
		"""

		return self._libinput.libinput_device_config_left_handed_set(
			self._handle, enable)

	def config_left_handed_get(self):
		"""Get the current left-handed configuration of the device.

		Returns:
			bool: :obj:`False` if the device is in right-handed mode,
			:obj:`True` if the device is in left-handed mode.
		"""

		return self._libinput.libinput_device_config_left_handed_get(
			self._handle)

	def config_left_handed_get_default(self):
		"""Get the default left-handed configuration of the device.

		Returns:
			bool: :obj:`False` if the device is in right-handed mode
			by default, or :obj:`True` if the device is in left-handed mode
			by default.
		"""

		return self._libinput.libinput_device_config_left_handed_get_default(
			self._handle)

	def config_click_get_methods(self):
		"""Check which button click methods a device supports.

		The button click method defines when to generate software-emulated
		buttons, usually on a device that does not have a specific physical
		button available.

		Returns:
			~libinput.constant.ClickMethod: A bitmask of possible methods.
		"""

		return self._libinput.libinput_device_config_click_get_methods(
			self._handle)

	def config_click_set_method(self, method):
		"""Set the button click method for this device.

		The button click method defines when to generate software-emulated
		buttons, usually on a device that does not have a specific physical
		button available.

		Note:
			The selected click method may not take effect immediately.
			The device may require changing to a neutral state first before
			activating the new method.
		Args:
			method (~libinput.constant.ClickMethod): The button click method.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput.libinput_device_config_click_set_method(
			self._handle, method)

	def config_click_get_method(self):
		"""Get the button click method for this device.

		The button click method defines when to generate software-emulated
		buttons, usually on a device that does not have a specific physical
		button available.

		Returns:
			~libinput.constant.ClickMethod: The current button click method
			for this device.
		"""

		return self._libinput.libinput_device_config_click_get_method(
			self._handle)

	def config_click_get_default_method(self):
		"""Get the default button click method for this device.

		The button click method defines when to generate software-emulated
		buttons, usually on a device that does not have a specific physical
		button available.

		Returns:
			~libinput.constant.ClickMethod: The default button click method
			for this device.
		"""

		return self._libinput.libinput_device_config_click_get_default_method(
			self._handle)

	def config_middle_emulation_is_available(self):
		"""Check if middle mouse button emulation configuration is available
		on this device.

		See `Middle button emulation`_ for details.

		Note:
			Some devices provide middle mouse button emulation but do not
			allow enabling/disabling that emulation. These devices return
			:obj:`False` in :meth:`config_middle_emulation_is_available`.
		Returns:
			bool: :obj:`True` if middle mouse button emulation is available
			and can be configured, :obj:`False` otherwise.
		"""

		return self._libinput \
			.libinput_device_config_middle_emulation_is_available(self._handle)

	def config_middle_emulation_set_enabled(self, state):
		"""Enable or disable middle button emulation on this device.

		When enabled, a simultaneous press of the left and right button
		generates a middle mouse button event. Releasing the buttons generates
		a middle mouse button release, the left and right button events are
		discarded otherwise.

		See `Middle button emulation`_ for details.

		Args:
			state (~libinput.constant.MiddleEmulationState):
				:attr:`~libinput.constant.MiddleEmulationState.DISABLED`
				to disable,
				:attr:`~libinput.constant.MiddleEmulationState.ENABLED`
				to enable middle button emulation.
		Returns:
			~libinput.constant.ConfigStatus: A config status code. Disabling
			middle button emulation on a device that does not support
			middle button emulation always succeeds.
		"""

		return self._libinput \
			.libinput_device_config_middle_emulation_set_enabled(
				self._handle, state)

	def config_middle_emulation_get_enabled(self):
		"""Check if configurable middle button emulation is enabled on
		this device.

		See `Middle button emulation`_ for details.

		If the device does not have configurable middle button emulation,
		this method returns
		:attr:`~libinput.constant.MiddleEmulationState.DISABLED`.

		Note:
			Some devices provide middle mouse button emulation but do not
			allow enabling/disabling that emulation. These devices always
			return :attr:`~libinput.constant.MiddleEmulationState.DISABLED`.
		Returns:
			~libinput.constant.MiddleEmulationState:
				:attr:`~libinput.constant.MiddleEmulationState.DISABLED` if
				disabled or not available/configurable,
				:attr:`~libinput.constant.MiddleEmulationState.ENABLED`
				if enabled.
		"""

		return self._libinput \
			.libinput_device_config_middle_emulation_get_enabled(self._handle)

	def config_middle_emulation_get_default_enabled(self):
		"""Check if configurable middle button emulation is enabled by default
		on this device.

		See `Middle button emulation`_ for details.

		If the device does not have configurable middle button emulation,
		this method returns
		:attr:`~libinput.constant.MiddleEmulationState.DISABLED`.

		Note:
			Some devices provide middle mouse button emulation but do not
			allow enabling/disabling that emulation. These devices always
			return :attr:`~libinput.constant.MiddleEmulationState.DISABLED`.
		Returns:
			~libinput.constant.MiddleEmulationState:
				:attr:`~libinput.constant.MiddleEmulationState.DISABLED` if
				disabled or not available,
				:attr:`~libinput.constant.MiddleEmulationState.ENABLED`
				if enabled.
		"""

		return self._libinput \
			.libinput_device_config_middle_emulation_get_default_enabled(
				self._handle)

	def config_scroll_get_methods(self):
		"""Check which scroll methods a device supports.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Returns:
			~libinput.constant.ScrollMethod: A bitmask of possible methods.
		"""

		return self._libinput.libinput_device_config_scroll_get_methods(
			self._handle)

	def config_scroll_set_method(self, method):
		"""Set the scroll method for this device.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Note:
			Setting :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN`
			enables the scroll method, but scrolling is only activated when
			the configured button is held down. If no button is set, i.e.
			:meth:`config_scroll_get_button` returns 0, scrolling cannot
			activate.
		Args:
			method (~libinput.constant.ScrollMethod): The scroll method for
				this device.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput.libinput_device_config_scroll_set_method(
			self._handle, method)

	def config_scroll_get_method(self):
		"""Get the scroll method for this device.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Returns:
			~libinput.constant.ScrollMethod: The current scroll method for
			this device.
		"""

		return self._libinput.libinput_device_config_scroll_get_method(
			self._handle)

	def config_scroll_get_default_method(self):
		"""Get the default scroll method for this device.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Returns:
			~libinput.constant.ScrollMethod: The default scroll method for
			this device.
		"""

		return self._libinput.libinput_device_config_scroll_get_default_method(
			self._handle)

	def config_scroll_set_button(self, button):
		"""Set the button for the
		:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` method for
		this device.

		When the current scroll method is set to
		:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN`, no button
		press/release events will be send for the configured button.

		When the configured button is pressed, any motion events along
		a scroll-capable axis are turned into scroll axis events.

		Note:
			Setting the button does not change the scroll method. To change
			the scroll method call :meth:`config_scroll_set_method`.
			If the button is :attr:`~libinput.evcodes.Button.BTN_NONE`,
			button scrolling is effectively disabled.
		Args:
			button (~libinput.evcodes.Button): The button which when pressed
				switches to sending scroll events.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput.libinput_device_config_scroll_set_button(
			self._handle, button)

	def config_scroll_get_button(self):
		"""Get the button for the
		:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` method for
		this device.

		If :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` scroll method
		is not supported, or no button is set, this function returns
		:attr:`~libinput.evcodes.Button.BTN_NONE`.

		Note:
			The return value is independent of the currently selected
			scroll-method. For button scrolling to activate, a device must
			have the :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN`
			method enabled, and a non-zero button set as scroll button.
		Returns:
			~libinput.evcodes.Button: The button which when pressed switches
			to sending scroll events.
		"""

		return self._libinput.libinput_device_config_scroll_get_button(
			self._handle)

	def config_scroll_get_default_button(self):
		"""Get the default button for the
		:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` method for
		this device.

		If :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` scroll method
		is not supported, or no default button is set, this function returns
		:attr:`~libinput.evcodes.Button.BTN_NONE`.

		Returns:
			~libinput.evcodes.Button: The default button for the
			:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` method.
		"""

		return self._libinput.libinput_device_config_scroll_get_default_button(
			self._handle)

	def config_dwt_is_available(self):
		"""Check if this device supports configurable
		disable-while-typing feature.

		This feature is usually available on built-in touchpads and disables
		the touchpad while typing. See `Disable-while-typing`_ for details.

		Returns:
			bool: :obj:`False` if this device does not support
			disable-while-typing, or :obj:`True` otherwise.
		"""

		return self._libinput.libinput_device_config_dwt_is_available(
			self._handle)

	def config_dwt_set_enabled(self, state):
		"""Enable or disable the disable-while-typing feature.

		When enabled, the device will be disabled while typing and for
		a short period after. See `Disable-while-typing`_ for details.

		Note:
			Enabling or disabling disable-while-typing may not take
			effect immediately.
		Args:
			state (~libinput.constant.DwtState):
				:attr:`~libinput.constant.DwtState.DISABLED` to disable
				disable-while-typing,
				:attr:`~libinput.constant.DwtState.ENABLED` to enable.
		Returns:
			~libinput.constant.ConfigStatus: A config status code. Disabling
			disable-while-typing on a device that does not support the feature
			always succeeds.
		"""

		return self._libinput.libinput_device_config_dwt_set_enabled(
			self._handle, state)

	def config_dwt_get_enabled(self):
		"""Check if the disable-while typing feature is currently enabled on
		this device.

		If the device does not support disable-while-typing, this method
		returns :attr:`~libinput.constant.DwtState.DISABLED`.

		Returns:
			~libinput.constant.DwtState:
				:attr:`~libinput.constant.DwtState.DISABLED` if disabled,
				:attr:`~libinput.constant.DwtState.ENABLED` if enabled.
		"""

		return self._libinput.libinput_device_config_dwt_get_enabled(
			self._handle)

	def config_dwt_get_default_enabled(self):
		"""Check if the disable-while typing feature is enabled on this device
		by default.

		If the device does not support disable-while-typing, this method
		returns :attr:`~libinput.constant.DwtState.DISABLED`.

		Returns:
			~libinput.constant.DwtState:
				:attr:`~libinput.constant.DwtState.DISABLED` if disabled,
				:attr:`~libinput.constant.DwtState.ENABLED` if enabled.
		"""

		return self._libinput.libinput_device_config_dwt_get_default_enabled(
			self._handle)

	def config_rotation_is_available(self):
		"""Check whether a device can have a custom rotation applied.

		Returns:
			bool: :obj:`True` if a device can be rotated, :obj:`False`
			otherwise.
		"""

		return self._libinput.libinput_device_config_rotation_is_available(
			self._handle)

	def config_rotation_set_angle(self, degrees_cw):
		"""Set the rotation of a device in degrees clockwise off the logical
		neutral position.

		Any subsequent motion events are adjusted according to the given angle.

		The angle has to be in the range of [0, 360] degrees, otherwise this
		function returns :attr:`~libinput.constant.ConfigStatus.INVALID`.
		If the angle is a multiple of 360 or negative, the caller must ensure
		the correct ranging before calling this method.

		libinput guarantees that this method accepts multiples of 90 degrees.
		If a value is within the [0, 360] range but not a multiple of
		90 degrees, this function may return
		:attr:`~libinput.constant.ConfigStatus.INVALID` if the underlying
		device or implementation does not support finer-grained rotation angles.

		The rotation angle is applied to all motion events emitted by
		the device. Thus, rotating the device also changes the angle required
		or presented by scrolling, gestures, etc.

		Args:
			degrees_cw (int): The angle in degrees clockwise.
		Returns:
			~libinput.constant.ConfigStatus: A config status code. Setting
			a rotation of 0 degrees on a device that does not support rotation
			always succeeds.
		"""

		return self._libinput.libinput_device_config_rotation_set_angle(
			self._handle, degrees_cw)

	def config_rotation_get_angle(self):
		"""Get the current rotation of a device in degrees clockwise off
		the logical neutral position.

		If this device does not support rotation, the return value is always 0.

		Returns:
			int: The angle in degrees clockwise.
		"""

		return self._libinput.libinput_device_config_rotation_get_angle(
			self._handle)

	def config_rotation_get_default_angle(self):
		"""Get the default rotation of a device in degrees clockwise off
		the logical neutral position.

		If this device does not support rotation, the return value is always 0.

		Returns:
			int: The default angle in degrees clockwise.
		"""

		return self._libinput.libinput_device_config_rotation_get_default_angle(
			self._handle)


class Device(DeviceConfig):
	"""An input device.
	"""

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
		"""Get the system name of the device.

		To get the descriptive device name, use :meth:`get_name`.

		Returns:
			str: System name of the device.
		"""

		pchar = self._libinput.libinput_device_get_sysname(self._handle)
		return string_at(pchar).decode()

	def get_name(self):
		"""The descriptive device name as advertised by the kernel
		and/or the hardware itself.

		To get the sysname for this device, use :meth:`get_sysname`.

		Returns:
			str: The device name.
		"""

		pchar = self._libinput.libinput_device_get_name(self._handle)
		return string_at(pchar).decode()

	def get_id_product(self):
		"""Get the product ID for this device.

		Returns:
			int: The product ID of this device.
		"""

		return self._libinput.libinput_device_get_id_product(self._handle)

	def get_id_vendor(self):
		"""Get the vendor ID for this device.

		Returns:
			int: The vendor ID of this device.
		"""

		return self._libinput.libinput_device_get_id_vendor(self._handle)

	def get_seat(self):
		"""Get the seat associated with this input device, see `Seats`_
		for details.

		A seat can be uniquely identified by the physical and logical seat
		name. As long as a reference to a seat is kept, it will compare equal
		to another seat object with the same physical/logical name pair.

		Returns:
			.Seat: The seat this input device belongs to.
		"""

		hseat = self._libinput.libinput_device_get_seat(self._handle)
		return Seat(hseat, self._libinput)

	def set_seat_logical_name(self, seat):
		"""Change the logical seat associated with this device by removing
		the device and adding it to the new seat.

		This command is identical to physically unplugging the device, then
		re-plugging it as a member of the new seat. libinput will generate
		a :attr:`~libinput.constant.Event.DEVICE_REMOVED` event and this
		:class:`Device` is considered removed from the context; it will not
		generate further events. A :attr:`~libinput.constant.Event.DEVICE_ADDED`
		event is generated with a new :class:`Device`. It is the caller's
		responsibility to update references to the new device accordingly.

		If the logical seat name already exists in the device's physical seat,
		the device is added to this seat. Otherwise, a new seat is created.

		Note:
			This change applies to this device until removal or
			:meth:`~libinput.LibInput.suspend`, whichever happens earlier.
		Args:
			name (str): The new logical seat name.
		Raises:
			AssertionError
		"""

		rc = self._libinput.libinput_device_set_seat_logical_name(
			self._handle, seat.encode())
		assert rc == 0, 'Cannot assign device to {}'.format(seat)

	def get_udev_device(self):
		"""Return a udev handle to the device that is this libinput device,
		if any.

		The returned handle has a refcount of at least 1, the caller must call
		:func:`udev_device_unref` once to release the associated resources.
		See the libudev documentation for details.

		Some devices may not have a udev device, or the udev device may be
		unobtainable. This function returns :obj:`None` if no udev device
		was available.

		Calling this function multiple times for the same device may not
		return the same udev handle each time.

		Returns:
			int: A udev handle to the device with a refcount of >= 1 or
			:obj:`None` if this device is not represented by a udev device.
		"""

		return self._libinput.libinput_device_get_udev_device(self._handle)

	def led_update(self, leds):
		"""Update the LEDs on the device, if any.

		If the device does not have LEDs, or does not have one or more of
		the LEDs given in the mask, this function does nothing.

		Args:
			leds (~libinput.constant.Led): A mask of the LEDs to set, or unset.
		"""

		self._libinput.libinput_device_led_update(self._handle, leds)

	def has_capability(self, capability):
		"""Check if the given device has the specified capability.

		Args:
			capability (~libinput.constant.DeviceCapability): A capability
			to check for.
		Returns:
			bool: :obj:`True` if the given device has the capability or
			:obj:`False` otherwise.
		"""

		return self._libinput.libinput_device_has_capability(
			self._handle, capability)

	def get_size(self):
		"""Get the physical size of a device in mm, where meaningful.

		This function only succeeds on devices with the required data, i.e.
		tablets, touchpads and touchscreens.

		Returns:
			tuple: (Success, Width, Height). If Success is :obj:`False`
			Width and Height are 0.
		"""

		width = c_double(0)
		height = c_double(0)
		rc = self._libinput.libinput_device_get_size(
			self._handle, byref(width), byref(height))
		if not rc:
			return True, width.value, height.value
		else:
			return False, 0.0, 0.0

	def pointer_has_button(self, button):
		"""Check if a :attr:`~libinput.constant.DeviceCapability.POINTER`
		device has a given button.

		Args:
			button (~libinput.evcodes.Button): Button to check for,
				e.g. :attr:`~libinput.evcodes.Button.BTN_LEFT`.
		Returns:
			bool: :obj:`True` if the device has this button, :obj:`False` if
			it does not.
		Raises:
			AssertionError
		"""

		rc = self._libinput.libinput_device_pointer_has_button(
			self._handle, button)
		assert rc >= 0, 'Device is not a pointer device'
		return bool(rc)

	def keyboard_has_key(self, key):
		"""Check if a :attr:`~libinput.constant.DeviceCapability.KEYBOARD`
		device has a given key.

		Args:
			key (~libinput.evcodes.Key): Key to check for, e.g.
				:attr:`~libinput.evcodes.Key.KEY_ESC`.
		Returns:
			bool: :obj:`True` if the device has this key, :obj:`False` if
			it does not.
		Raises:
			AssertionError
		"""

		rc = self._libinput.libinput_device_keyboard_has_key(
			self._handle, key)
		assert rc >= 0, 'Device is not a keyboard device'
		return bool(rc)

	def tablet_pad_get_num_buttons(self):
		"""Return the number of buttons on a device with
		the :attr:`~libinput.constant.DeviceCapability.TABLET_PAD` capability.

		Buttons on a pad device are numbered sequentially, see
		`Tablet pad button numbers`_ for details.

		Returns:
			int: The number of buttons supported by the device.
		Raises:
			AssertionError
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_buttons(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'
		return num

	def tablet_pad_get_num_rings(self):
		"""Return the number of rings a device with
		the :attr:`~libinput.constant.DeviceCapability.TABLET_PAD`
		capability provides.

		Returns:
			int: The number of rings or 0 if the device has no rings.
		Raises:
			AssertionError
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_rings(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'
		return num

	def tablet_pad_get_num_strips(self):
		"""Return the number of strips a device with
		the :attr:`~libinput.constant.DeviceCapability.TABLET_PAD`
		capability provides.

		Returns:
			int: The number of strips or 0 if the device has no strips.
		Raises:
			AssertionError
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_strips(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'
		return num

	def tablet_pad_get_num_mode_groups(self):
		"""Most devices only provide a single mode group, however devices
		such as the Wacom Cintiq 22HD provide two mode groups.

		If multiple mode groups are available, a caller should use
		:meth:`.TabletPadModeGroup.has_button`,
		:meth:`.TabletPadModeGroup.has_ring`
		and :meth:`.TabletPadModeGroup.has_strip` to associate each button,
		ring and strip with the correct mode group.

		Returns:
			int: The number of mode groups available on this device.
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_mode_groups(
			self._handle)
		assert num >= 0, 'Device is not a tablet pad device'

	def tablet_pad_get_mode_group(self, group):
		"""While a reference is kept by the caller, the returned mode group
		will compare equal with mode group returned by each subsequent call of
		this method with the same index and mode group returned from
		:meth:`~libinput.event.TabletPadEvent.get_mode_group`, provided
		the event was generated by this mode group.

		Args:
			group (int): A mode group index.
		Returns:
			.TabletPadModeGroup: The mode group with the given index
			or :obj:`None` if an invalid index is given.
		"""

		hmodegroup = self._libinput.libinput_device_tablet_pad_get_mode_group(
			self._handle, group)
		if hmodegroup:
			return TabletPadModeGroup(hmodegroup, self._libinput)
		return None


class Seat(object):
	"""A seat has two identifiers, the physical name and the logical name.

	A device is always assigned to exactly one seat. It may change to
	a different logical seat but it cannot change physical seats.
	See `Seats`_ for details.

	Two instances of :class:`.Seat` compare equal if they refer to the same
	physical/logical seat.
	"""

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
		"""Return the physical name of the seat.

		For libinput contexts created from udev, this is always the same value
		as passed into :meth:`~libinput.LibInput.udev_assign_seat` and all
		seats from that context will have the same physical name.

		The physical name of the seat is one that is usually set by the system
		or lower levels of the stack. In most cases, this is the base filter
		for devices - devices assigned to seats outside the current seat will
		not be available to the caller.

		Returns:
			str: The physical name of this seat.
		"""

		pchar = self._libinput.libinput_seat_get_physical_name(self._handle)
		return string_at(pchar).decode()

	def get_logical_name(self):
		"""Return the logical name of the seat.

		This is an identifier to group sets of devices within the compositor.

		Returns:
			str: The logical name of this seat.
		"""

		pchar = self._libinput.libinput_seat_get_logical_name(self._handle)
		return string_at(pchar).decode()


class TabletTool(object):
	"""An object representing a tool being used by a device with
	the :attr:`~libinput.constant.DeviceCapability.TABLET_TOOL` capability.

	Tablet events generated by such a device are bound to a specific tool
	rather than coming from the device directly. Depending on the hardware
	it is possible to track the same physical tool across multiple
	:class:`.Device` instances, see `Tracking unique tools`_.

	As long as a reference to a :class:`.TabletTool` is kept, multiple
	instances will compare equal if they refer to the same physical tool and
	the hardware supports it.
	"""

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
		"""Return the tool type for a tool object.

		See `Vendor-specific tablet tool types`_ for details.

		Returns:
			~libinput.constant.TabletToolType: The tool type for this tool
			object.
		"""

		return self._libinput.libinput_tablet_tool_get_type(self._handle)

	def get_tool_id(self):
		"""Return the tool ID for a tool object.

		If nonzero, this number identifies the specific type of the tool with
		more precision than the type returned in :meth:`get_type`,
		see `Vendor-specific tablet tool types`_. Not all tablets support
		a tool ID.

		Tablets known to support tool IDs include the Wacom Intuos 3, 4, 5,
		Wacom Cintiq and Wacom Intuos Pro series.

		Returns:
			int: The tool ID for this tool object or 0 if none is provided.
		"""

		return self._libinput.libinput_tablet_tool_get_tool_id(self._handle)

	def has_pressure(self):
		"""Return whether the tablet tool supports pressure.

		Returns:
			bool: :obj:`True` if the axis is available, :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_tool_has_pressure(self._handle)

	def has_distance(self):
		"""Return whether the tablet tool supports distance.

		Returns:
			bool: :obj:`True` if the axis is available, :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_tool_has_distance(self._handle)

	def has_tilt(self):
		"""Return whether the tablet tool supports tilt.

		Returns:
			bool: :obj:`True` if the axis is available, :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_tool_has_tilt(self._handle)

	def has_rotation(self):
		"""Return whether the tablet tool supports z-rotation.

		Returns:
			bool: :obj:`True` if the axis is available, :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_tool_has_rotation(self._handle)

	def has_slider(self):
		"""Return whether the tablet tool has a slider axis.

		Returns:
			bool: :obj:`True` if the axis is available, :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_tool_has_slider(self._handle)

	def has_wheel(self):
		"""Return whether the tablet tool has a relative wheel.

		Returns:
			bool: :obj:`True` if the axis is available, :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_tool_has_wheel(self._handle)

	def has_button(self, button):
		"""Check if a tablet tool has a specified button.

		Args:
			button (~libinput.evcodes.Button): Button to check for.
		Returns:
			bool: :obj:`True` if the tool supports this button, :obj:`False`
			if it does not.
		"""

		return self._libinput.libinput_tablet_tool_has_button(
			self._handle, button)

	def is_unique(self):
		"""Return :obj:`True` if the physical tool can be uniquely identified
		by libinput, or :obj:`False` otherwise.

		If a tool can be uniquely identified, keeping a reference to the tool
		allows tracking the tool across proximity out sequences and across
		compatible tablets. See `Tracking unique tools`_ for more details.

		Returns:
			bool: :obj:`True` if the tool can be uniquely identified,
			:obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_tool_is_unique(self._handle)

	def get_serial(self):
		"""Return the serial number of a tool.

		If the tool does not report a serial number, this method returns zero.
		See `Tracking unique tools`_ for details.

		Returns:
			int: The tool serial number.
		"""

		return self._libinput.libinput_tablet_tool_get_serial(self._handle)


class TabletPadModeGroup(object):
	"""A mode on a tablet pad is a virtual grouping of functionality, usually
	based on some visual feedback like LEDs on the pad.

	The set of buttons, rings and strips that share the same mode are
	a "mode group". Whenever the mode changes, all buttons, rings and strips
	within this mode group are affected. See `Tablet pad modes`_ for detail.

	Most tablets only have a single mode group, some tablets provide multiple
	mode groups through independent banks of LEDs (e.g. the Wacom Cintiq 24HD).
	libinput guarantees that at least one mode group is always available.
	"""

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
		"""The returned number is the same index as passed to
		:meth:`~libinput.define.Device.tablet_pad_get_mode_group`.

		For tablets with only one mode this number is always 0.

		Returns:
			int: The numeric index this mode group represents, starting at 0.
		"""

		return self._libinput.libinput_tablet_pad_mode_group_get_index(
			self._handle)

	def get_num_modes(self):
		"""Query the mode group for the number of available modes.

		The number of modes is usually decided by the number of physical LEDs
		available on the device. Different mode groups may have a different
		number of modes. Use :meth:`get_mode` to get the currently active mode.

		libinput guarantees that at least one mode is available. A device
		without mode switching capability has a single mode group and
		a single mode.

		Returns:
			int: The number of modes available in this mode group.
		"""

		return self._libinput.libinput_tablet_pad_mode_group_get_num_modes(
			self._handle)

	def get_mode(self):
		"""Return the current mode this mode group is in.

		Returns:
			int: The numeric index of the current mode in this group, starting
			at 0.
		"""

		return self._libinput.libinput_tablet_pad_mode_group_get_mode(
			self._handle)

	def has_button(self, button):
		"""Devices without mode switching capabilities return :obj:`True`
		for every button.

		Args:
			button (int): A button index, starting at 0.
		Returns:
			bool: :obj:`True` if the given button index is part of this
			mode group or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_pad_mode_group_has_button(
			self._handle, button)

	def has_ring(self, ring):
		"""Devices without mode switching capabilities return :obj:`True`
		for every ring.

		Args:
			ring (int): A ring index, starting at 0.
		Returns:
			bool: :obj:`True` if the given ring index is part of this
			mode group or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_pad_mode_group_has_ring(
			self._handle, ring)

	def has_strip(self, strip):
		"""Devices without mode switching capabilities return :obj:`True`
		for every strip.

		Args:
			strip (int): A strip index, starting at 0.
		Returns:
			bool: :obj:`True` if the given strip index is part of this
			mode group or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_pad_mode_group_has_strip(
			self._handle, strip)

	def button_is_toggle(self, button):
		"""The toggle button in a mode group is the button assigned to cycle
		to or directly assign a new mode when pressed.

		Not all devices have a toggle button and some devices may have more
		than one toggle button. For example, the Wacom Cintiq 24HD has six
		toggle buttons in two groups, each directly selecting one of the three
		modes per group.

		Devices without mode switching capabilities return :obj:`False`
		for every button.

		Args:
			button (int): A button index, starting at 0.
		Returns:
			bool: :obj:`True` if the button is a mode toggle button for
			this group, or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_tablet_pad_mode_group_button_is_toggle(
			self._handle, button)
