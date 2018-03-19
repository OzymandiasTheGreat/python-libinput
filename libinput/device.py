#!/usr/bin/env python3

from __future__ import absolute_import
from ctypes import c_void_p, c_char_p, c_uint, c_int, c_bool, c_double
from ctypes import POINTER, string_at, byref, c_uint32, c_float
from .constant import Led, DeviceCapability, ConfigStatus, TapState
from .constant import TapButtonMap, DragState, DragLockState, SendEventsMode
from .constant import AccelProfile, ClickMethod, MiddleEmulationState
from .constant import ScrollMethod, DwtState
from .define import TabletPadModeGroup


class BaseDevice(object):

	def __init__(self, hdevice, libinput):

		self._handle = hdevice
		self._libinput = libinput


class DeviceConfig(BaseDevice):
	"""A configuration object.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

		self._tap = DeviceConfigTap(self._handle, self._libinput)
		self._calibration = DeviceConfigCalibration(
			self._handle, self._libinput)
		self._send_events = DeviceConfigSendEvents(
			self._handle, self._libinput)
		self._accel = DeviceConfigAccel(self._handle, self._libinput)
		self._scroll = DeviceConfigScroll(self._handle, self._libinput)
		self._left_handed = DeviceConfigLeftHanded(
			self._handle, self._libinput)
		self._click = DeviceConfigClick(self._handle, self._libinput)
		self._middle_emulation = DeviceConfigMiddleEmulation(
			self._handle, self._libinput)
		self._dwt = DeviceConfigDwt(self._handle, self._libinput)
		self._rotation = DeviceConfigRotation(self._handle, self._libinput)

	@property
	def tap(self):
		"""Tapping-related configuration methods.

		Returns:
			.DeviceConfigTap:
		"""

		return self._tap

	@property
	def calibration(self):
		"""Calibration matrix configuration methods.

		Returns:
			.DeviceConfigCalibration:
		"""

		return self._calibration

	@property
	def send_events(self):
		"""Event sending configuration methods.

		Returns:
			.DeviceConfigSendEvents:
		"""

		return self._send_events

	@property
	def accel(self):
		"""Pointer acceleration configuration methods.

		Returns:
			.DeviceConfigAccel:
		"""

		return self._accel

	@property
	def scroll(self):
		"""Scrolling configuration methods.

		Returns:
			.DeviceConfigScroll:
		"""

		return self._scroll

	@property
	def left_handed(self):
		"""Left-handed usage configuration methods.

		Returns:
			.DeviceConfigLeftHanded:
		"""

		return self._left_handed

	@property
	def click(self):
		"""Click method configuration methods.

		Returns:
			.DeviceConfigClick:
		"""

		return self._click

	@property
	def middle_emulation(self):
		"""Middle mouse button emulation configuration methods.

		Returns:
			.DeviceConfigMiddleEmulation:
		"""

		return self._middle_emulation

	@property
	def dwt(self):
		"""Disable-while-typing configuration methods.

		Returns:
			.DeviceConfigDwt:
		"""

		return self._dwt

	@property
	def rotation(self):
		"""Rotation configuration methods.

		Returns:
			.DeviceConfigRotation:
		"""

		return self._rotation


class DeviceConfigTap(BaseDevice):
	"""Tapping-related configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

	@property
	def finger_count(self):
		"""Check if the device supports tap-to-click and how many fingers can
		be used for tapping.

		See :meth:`set_enabled` for more information.

		Returns:
			int: The number of fingers that can generate a tap event, or 0 if
			the device does not support tapping.
		"""

		return self._libinput.libinput_device_config_tap_get_finger_count(
			self._handle)

	def set_enabled(self, state):
		"""Enable or disable tap-to-click on this device, with
		a default mapping of 1, 2, 3 finger tap mapping to left, right, middle
		click, respectively.

		Tapping is limited by the number of simultaneous touches supported by
		the device, see :attr:`finger_count`.

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

	@property
	def enabled(self):
		"""Check if tap-to-click is enabled on this device.

		If the device does not support tapping, this property is always
		:attr:`~libinput.constant.TapState.DISABLED`.

		Returns:
			~libinput.constant.TapState: Whether tapping is enabled or disabled.
		"""

		return self._libinput.libinput_device_config_tap_get_enabled(
			self._handle)

	@property
	def default_enabled(self):
		"""The default setting for whether tap-to-click is enabled
		on this device.

		Returns:
			~libinput.constant.TapState: Whether tapping is enabled or disabled.
		"""

		return self._libinput.libinput_device_config_tap_get_default_enabled(
			self._handle)

	def set_button_map(self, button_map):
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

		If :attr:`finger_count` is 0, this method raises :exc:`AssertionError`.

		Args:
			button_map (~libinput.constant.TapButtonMap): The new
				finger-to-button number mapping.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		Raises:
			AssertionError
		"""

		assert self.finger_count > 0, 'This device does not support tapping'
		return self._libinput.libinput_device_config_tap_set_button_map(
			self._handle, button_map)

	@property
	def button_map(self):
		"""The finger number to button number mapping for tap-to-click.

		For devices that do not support tapping (i.e. :attr:`finger_count`
		is 0), this property raises :exc:`AssertionError`.

		Returns:
			~libinput.constant.TapButtonMap: The current finger-to-button
			number mapping.
		Raises:
			AssertionError
		"""

		assert self.finger_count > 0, 'This device does not support tapping'
		return self._libinput.libinput_device_config_tap_get_button_map(
			self._handle)

	@property
	def default_button_map(self):
		"""The default finger number to button number mapping
		for tap-to-click.

		For devices that do not support tapping (i.e. :attr:`finger_count`
		is 0), this property raises :exc:`AssertionError`.

		Returns:
			~libinput.constant.TapButtonMap: The default finger-to-button
			number mapping.
		Raises:
			AssertionError
		"""

		assert self.finger_count > 0, 'This device does not support tapping'
		return self._libinput.libinput_device_config_tap_get_default_button_map(
			self._handle)

	def set_drag_enabled(self, state):
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

	@property
	def drag_enabled(self):
		"""Whether tap-and-drag is enabled or disabled on this device.

		Returns:
			~libinput.constant.DragState: Whether tap-and-drag is enabled.
		"""

		return self._libinput.libinput_device_config_tap_get_drag_enabled(
			self._handle)

	@property
	def default_drag_enabled(self):
		"""Whether tap-and-drag is enabled or disabled by default
		on this device.

		Returns:
			~libinput.constant.DragState: Whether tap-and-drag is enabled
			by default.
		"""

		return self._libinput \
			.libinput_device_config_tap_get_default_drag_enabled(self._handle)

	def set_drag_lock_enabled(self, state):
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

	@property
	def drag_lock_enabled(self):
		"""Check if drag-lock during tapping is enabled on this device.

		If the device does not support tapping, this function always returns
		:attr:`~libinput.constant.DragLockState.DISABLED`.

		Drag lock may be enabled even when tapping is disabled.

		Returns:
			~libinput.constant.DragLockState: Whether drag lock is enabled.
		"""

		return self._libinput.libinput_device_config_tap_get_drag_lock_enabled(
			self._handle)

	@property
	def default_drag_lock_enabled(self):
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


class DeviceConfigCalibration(BaseDevice):
	"""Calibration matrix configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

	def has_matrix(self):
		"""Check if the device can be calibrated via a calibration matrix.

		Returns:
			bool: :obj:`True` if the device can be calibrated, :obj:`False`
			otherwise.
		"""

		return self._libinput.libinput_device_config_calibration_has_matrix(
			self._handle)

	def set_matrix(self, matrix):
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

	@property
	def matrix(self):
		"""The current calibration matrix for this device.

		Returns:
			(bool, (float, float, float, float, float, float)): :obj:`False` if
			no calibration is set and
			the returned matrix is the identity matrix, :obj:`True`
			otherwise. :obj:`tuple` representing the first two rows of
			a 3x3 matrix as described in :meth:`set_matrix`.
		"""

		matrix = (c_float * 6)()
		rc = self._libinput.libinput_device_config_calibration_get_matrix(
			self._handle, matrix)
		return rc, tuple(matrix)

	@property
	def default_matrix(self):
		"""The default calibration matrix for this device.

		On most devices, this is the identity matrix. If the udev property
		``LIBINPUT_CALIBRATION_MATRIX`` is set on the respective udev device,
		that property's value becomes the default matrix, see
		`Static device configuration via udev`_.

		Returns:
			(bool, (float, float, float, float, float, float)): :obj:`False` if
			no calibration is set and
			the returned matrix is the identity matrix, :obj:`True`
			otherwise. :obj:`tuple` representing the first two rows of
			a 3x3 matrix as described
			in :meth:`config_calibration_set_matrix`.
		"""

		matrix = (c_float * 6)()
		rc = self._libinput \
			.libinput_device_config_calibration_get_default_matrix(
				self._handle, matrix)
		return rc, tuple(matrix)


class DeviceConfigSendEvents(BaseDevice):
	"""Event sending configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

	@property
	def modes(self):
		"""The possible send-event modes for this device.

		These modes define when a device may process and send events.

		Returns:
			~libinput.constant.SendEventsMode: A bitmask of possible modes.
		"""

		return self._libinput.libinput_device_config_send_events_get_modes(
			self._handle)

	def set_mode(self, mode):
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

	@property
	def mode(self):
		"""The send-event mode for this device.

		The mode defines when the device processes and sends events to
		the caller.

		If a caller enables the bits for multiple modes, some of which are
		subsets of another mode libinput may drop the bits that are subsets.
		In other words, don't expect :attr:`mode` to always be exactly the same
		bitmask as passed into :meth:`set_mode`.

		Returns:
			~libinput.constant.SendEventsMode: The current bitmask of
			the send-event mode for this device.
		"""

		return self._libinput.libinput_device_config_send_events_get_mode(
			self._handle)

	@property
	def default_mode(self):
		"""The default send-event mode for this device.

		The mode defines when the device processes and sends events to
		the caller.

		Returns:
			~libinput.constant.SendEventsMode: The bitmask of
			the send-event mode for this device.
		"""

		return self._libinput \
			.libinput_device_config_send_events_get_default_mode(self._handle)


class DeviceConfigAccel(BaseDevice):
	"""Pointer acceleration configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

	def is_available(self):
		"""Check if a device uses libinput-internal pointer-acceleration.

		Returns:
			bool: :obj:`False` if the device is not accelerated,
			:obj:`True` if it is accelerated
		"""

		return self._libinput.libinput_device_config_accel_is_available(
			self._handle)

	def set_speed(self, speed):
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

	@property
	def speed(self):
		"""The current pointer acceleration setting for
		this pointer device.

		The returned value is normalized to a range of [-1, 1]. See
		:meth:`set_speed` for details.

		Returns:
			float: The current speed, range -1 to 1.
		"""

		return self._libinput.libinput_device_config_accel_get_speed(
			self._handle)

	@property
	def default_speed(self):
		"""The default speed setting for this device, normalized to
		a range of [-1, 1].

		See :meth:`set_speed` for details.

		Returns:
			float: The default speed setting for this device.
		"""

		return self._libinput.libinput_device_config_accel_get_default_speed(
			self._handle)

	@property
	def profiles(self):
		"""A bitmask of the configurable acceleration modes available
		on this device.

		Returns:
			~libinput.constant.AccelProfile: A bitmask of all configurable
			modes available on this device.
		"""

		return self._libinput.libinput_device_config_accel_get_profiles(
			self._handle)

	def set_profile(self, profile):
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

	@property
	def profile(self):
		"""The current pointer acceleration profile for this pointer device.

		Returns:
			~libinput.constant.AccelProfile: The currently configured pointer
			acceleration profile.
		"""

		return self._libinput.libinput_device_config_accel_get_profile(
			self._handle)

	@property
	def default_profile(self):
		"""The default pointer acceleration profile for
		this pointer device.

		Returns:
			~libinput.constant.AccelProfile: The default acceleration profile
			for this device.
		"""

		return self._libinput.libinput_device_config_accel_get_default_profile(
			self._handle)


class DeviceConfigScroll(BaseDevice):
	"""Scrolling configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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
			c_void_p, c_uint32)
		self._libinput.libinput_device_config_scroll_set_button.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_scroll_get_button.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_scroll_get_button.restype = (
			c_uint32)
		self._libinput \
			.libinput_device_config_scroll_get_default_button.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_scroll_get_default_button.restype = (
				c_uint32)

	def has_natural_scroll(self):
		""":obj:`True` if the device supports "natural scrolling".

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

	def set_natural_scroll_enabled(self, enable):
		"""Enable or disable natural scrolling on the device.

		Args:
			enable (bool): :obj:`True` to enable, :obj:`False` to disable
				natural scrolling.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput \
			.libinput_device_config_scroll_set_natural_scroll_enabled(
				self._handle)

	@property
	def natural_scroll_enabled(self):
		"""The current mode for scrolling on this device.

		Returns:
			bool: :obj:`False` if natural scrolling is disabled, :obj:`True`
			if enabled.
		"""

		return self._libinput \
			.libinput_device_config_scroll_get_natural_scroll_enabled(
				self._handle)

	@property
	def default_natural_scroll_enabled(self):
		"""The default mode for scrolling on this device.

		Returns:
			bool: :obj:`False` if natural scrolling is disabled by default,
			:obj:`True` if enabled.
		"""

		return self._libinput \
			.libinput_device_config_scroll_get_default_natural_scroll_enabled(
				self._handle)

	@property
	def methods(self):
		"""Check which scroll methods a device supports.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Returns:
			~libinput.constant.ScrollMethod: A bitmask of possible methods.
		"""

		return self._libinput.libinput_device_config_scroll_get_methods(
			self._handle)

	def set_method(self, method):
		"""Set the scroll method for this device.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Note:
			Setting :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN`
			enables the scroll method, but scrolling is only activated when
			the configured button is held down. If no button is set, i.e.
			:attr:`button` is 0, scrolling cannot activate.
		Args:
			method (~libinput.constant.ScrollMethod): The scroll method for
				this device.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput.libinput_device_config_scroll_set_method(
			self._handle, method)

	@property
	def method(self):
		"""The scroll method for this device.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Returns:
			~libinput.constant.ScrollMethod: The current scroll method for
			this device.
		"""

		return self._libinput.libinput_device_config_scroll_get_method(
			self._handle)

	@property
	def default_method(self):
		"""The default scroll method for this device.

		The method defines when to generate scroll axis events instead of
		pointer motion events.

		Returns:
			~libinput.constant.ScrollMethod: The default scroll method for
			this device.
		"""

		return self._libinput.libinput_device_config_scroll_get_default_method(
			self._handle)

	def set_button(self, button):
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
			the scroll method call :meth:`set_method`.
			If the button is 0, button scrolling is effectively disabled.
		Args:
			button (int): The button which when pressed
				switches to sending scroll events.
		Returns:
			~libinput.constant.ConfigStatus: A config status code.
		"""

		return self._libinput.libinput_device_config_scroll_set_button(
			self._handle, button)

	@property
	def button(self):
		"""The button for the
		:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` method for
		this device.

		If :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` scroll method
		is not supported, or no button is set, this property is 0.

		Note:
			The return value is independent of the currently selected
			scroll-method. For button scrolling to activate, a device must
			have the :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN`
			method enabled, and a non-zero button set as scroll button.
		Returns:
			int: The button which when pressed switches
			to sending scroll events.
		"""

		return self._libinput.libinput_device_config_scroll_get_button(
			self._handle)

	@property
	def default_button(self):
		"""The default button for the
		:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` method for
		this device.

		If :attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` scroll method
		is not supported, or no default button is set, this property is 0.

		Returns:
			int: The default button for the
			:attr:`~libinput.constant.ScrollMethod.ON_BUTTON_DOWN` method.
		"""

		return self._libinput.libinput_device_config_scroll_get_default_button(
			self._handle)


class DeviceConfigLeftHanded(BaseDevice):
	"""Left-handed usage configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

		self._libinput \
			.libinput_device_config_left_handed_is_available.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_left_handed_is_available.restype = (
				c_bool)
		self._libinput.libinput_device_config_left_handed_set.argtypes = (
			c_void_p, c_bool)
		self._libinput.libinput_device_config_left_handed_set.restype = (
			ConfigStatus)
		self._libinput.libinput_device_config_left_handed_get.argtypes = (
			c_void_p,)
		self._libinput.libinput_device_config_left_handed_get.restype = c_bool
		self._libinput \
			.libinput_device_config_left_handed_get_default.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_left_handed_get_default.restype = (
				c_bool)

	def is_available(self):
		"""Check if a device has a configuration that supports left-handed
		usage.

		Returns:
			bool: :obj:`True` if the device can be set to left-handed,
			or :obj:`False` otherwise
		"""

		return self._libinput.libinput_device_config_left_handed_is_available(
			self._handle)

	def set(self, enable):
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

	@property
	def enabled(self):
		"""The current left-handed configuration of the device.

		Returns:
			bool: :obj:`False` if the device is in right-handed mode,
			:obj:`True` if the device is in left-handed mode.
		"""

		return self._libinput.libinput_device_config_left_handed_get(
			self._handle)

	@property
	def default_enabled(self):
		"""The default left-handed configuration of the device.

		Returns:
			bool: :obj:`False` if the device is in right-handed mode
			by default, or :obj:`True` if the device is in left-handed mode
			by default.
		"""

		return self._libinput.libinput_device_config_left_handed_get_default(
			self._handle)


class DeviceConfigClick(BaseDevice):
	"""Click method configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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
		self._libinput \
			.libinput_device_config_click_get_default_method.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_click_get_default_method.restype = (
				ClickMethod)

	@property
	def methods(self):
		"""Check which button click methods a device supports.

		The button click method defines when to generate software-emulated
		buttons, usually on a device that does not have a specific physical
		button available.

		Returns:
			~libinput.constant.ClickMethod: A bitmask of possible methods.
		"""

		return self._libinput.libinput_device_config_click_get_methods(
			self._handle)

	def set_method(self, method):
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

	@property
	def method(self):
		"""The button click method for this device.

		The button click method defines when to generate software-emulated
		buttons, usually on a device that does not have a specific physical
		button available.

		Returns:
			~libinput.constant.ClickMethod: The current button click method
			for this device.
		"""

		return self._libinput.libinput_device_config_click_get_method(
			self._handle)

	@property
	def default_method(self):
		"""The default button click method for this device.

		The button click method defines when to generate software-emulated
		buttons, usually on a device that does not have a specific physical
		button available.

		Returns:
			~libinput.constant.ClickMethod: The default button click method
			for this device.
		"""

		return self._libinput.libinput_device_config_click_get_default_method(
			self._handle)


class DeviceConfigMiddleEmulation(BaseDevice):
	"""Middle mouse button emulation configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

	def is_available(self):
		"""Check if middle mouse button emulation configuration is available
		on this device.

		See `Middle button emulation`_ for details.

		Note:
			Some devices provide middle mouse button emulation but do not
			allow enabling/disabling that emulation. These devices return
			:obj:`False` in :attr:`is_available`.
		Returns:
			bool: :obj:`True` if middle mouse button emulation is available
			and can be configured, :obj:`False` otherwise.
		"""

		return self._libinput \
			.libinput_device_config_middle_emulation_is_available(self._handle)

	def set_enabled(self, state):
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

	@property
	def enabled(self):
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

	@property
	def default_enabled(self):
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


class DeviceConfigDwt(BaseDevice):
	"""Disable-while-typing configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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
		self._libinput \
			.libinput_device_config_dwt_get_default_enabled.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_device_config_dwt_get_default_enabled.restype = (
				DwtState)

	def is_available(self):
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

	def set_enabled(self, state):
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

	@property
	def enabled(self):
		"""Check if the disable-while typing feature is currently enabled on
		this device.

		If the device does not support disable-while-typing, this property
		is :attr:`~libinput.constant.DwtState.DISABLED`.

		Returns:
			~libinput.constant.DwtState:
				:attr:`~libinput.constant.DwtState.DISABLED` if disabled,
				:attr:`~libinput.constant.DwtState.ENABLED` if enabled.
		"""

		return self._libinput.libinput_device_config_dwt_get_enabled(
			self._handle)

	@property
	def default_enabled(self):
		"""Check if the disable-while typing feature is enabled on this device
		by default.

		If the device does not support disable-while-typing, this property
		is :attr:`~libinput.constant.DwtState.DISABLED`.

		Returns:
			~libinput.constant.DwtState:
				:attr:`~libinput.constant.DwtState.DISABLED` if disabled,
				:attr:`~libinput.constant.DwtState.ENABLED` if enabled.
		"""

		return self._libinput.libinput_device_config_dwt_get_default_enabled(
			self._handle)


class DeviceConfigRotation(BaseDevice):
	"""Rotation configuration methods.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

	def is_available(self):
		"""Check whether a device can have a custom rotation applied.

		Returns:
			bool: :obj:`True` if a device can be rotated, :obj:`False`
			otherwise.
		"""

		return self._libinput.libinput_device_config_rotation_is_available(
			self._handle)

	def set_angle(self, degrees_cw):
		"""Set the rotation of a device in degrees clockwise off the logical
		neutral position.

		Any subsequent motion events are adjusted according to the given angle.

		The angle has to be in the range of [0, 360] degrees, otherwise this
		method returns :attr:`~libinput.constant.ConfigStatus.INVALID`.
		If the angle is a multiple of 360 or negative, the caller must ensure
		the correct ranging before calling this method.

		libinput guarantees that this method accepts multiples of 90 degrees.
		If a value is within the [0, 360] range but not a multiple of
		90 degrees, this method may return
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

	@property
	def angle(self):
		"""The current rotation of a device in degrees clockwise off
		the logical neutral position.

		If this device does not support rotation, the return value is always 0.

		Returns:
			int: The angle in degrees clockwise.
		"""

		return self._libinput.libinput_device_config_rotation_get_angle(
			self._handle)

	@property
	def default_angle(self):
		"""The default rotation of a device in degrees clockwise off
		the logical neutral position.

		If this device does not support rotation, the return value is always 0.

		Returns:
			int: The default angle in degrees clockwise.
		"""

		return self._libinput.libinput_device_config_rotation_get_default_angle(
			self._handle)


class Device(BaseDevice):
	"""An input device.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

		self._libinput.libinput_device_ref(self._handle)

		hseat = self._libinput.libinput_device_get_seat(self._handle)
		self._seat = Seat(hseat, self._libinput)
		self._pointer = DevicePointer(self._handle, self._libinput)
		self._keyboard = DeviceKeyboard(self._handle, self._libinput)
		self._tablet_pad = DeviceTabletPad(self._handle, self._libinput)
		self._config = DeviceConfig(self._handle, self._libinput)

	def __del__(self):

		self._libinput.libinput_device_unref(self._handle)

	def __eq__(self, other):

		if isinstance(other, type(self)):
			return self._handle == other._handle
		else:
			return NotImplemented

	@property
	def sysname(self):
		"""The system name of the device.

		To get the descriptive device name, use :attr:`name`.

		Returns:
			str: System name of the device.
		"""

		pchar = self._libinput.libinput_device_get_sysname(self._handle)
		return string_at(pchar).decode()

	@property
	def name(self):
		"""The descriptive device name as advertised by the kernel
		and/or the hardware itself.

		To get the sysname for this device, use :attr:`sysname`.

		Returns:
			str: The device name.
		"""

		pchar = self._libinput.libinput_device_get_name(self._handle)
		return string_at(pchar).decode()

	@property
	def id_product(self):
		"""The product ID for this device.

		Returns:
			int: The product ID of this device.
		"""

		return self._libinput.libinput_device_get_id_product(self._handle)

	@property
	def id_vendor(self):
		"""The vendor ID for this device.

		Returns:
			int: The vendor ID of this device.
		"""

		return self._libinput.libinput_device_get_id_vendor(self._handle)

	@property
	def seat(self):
		"""The seat associated with this input device, see `Seats`_
		for details.

		A seat can be uniquely identified by the physical and logical seat
		name. As long as a reference to a seat is kept, it will compare equal
		to another seat object with the same physical/logical name pair.

		Returns:
			.Seat: The seat this input device belongs to.
		"""

		return self._seat

	def set_seat_logical_name(self, seat):
		"""Change the logical seat associated with this device by removing
		the device and adding it to the new seat.

		This command is identical to physically unplugging the device, then
		re-plugging it as a member of the new seat. libinput will generate
		a :attr:`~libinput.constant.EventType.DEVICE_REMOVED` event and this
		:class:`Device` is considered removed from the context; it will not
		generate further events.
		A :attr:`~libinput.constant.EventType.DEVICE_ADDED` event is
		generated with a new :class:`Device`. It is the caller's
		responsibility to update references to the new device accordingly.

		If the logical seat name already exists in the device's physical seat,
		the device is added to this seat. Otherwise, a new seat is created.

		Note:
			This change applies to this device until removal or
			:meth:`~libinput.LibInput.suspend`, whichever happens earlier.
		Args:
			seat (str): The new logical seat name.
		Raises:
			AssertionError
		"""

		rc = self._libinput.libinput_device_set_seat_logical_name(
			self._handle, seat.encode())
		assert rc == 0, 'Cannot assign device to {}'.format(seat)

	@property
	def udev_device(self):
		"""A udev handle to the device that is this libinput device,
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
		the LEDs given in the mask, this method does nothing.

		Args:
			leds (~libinput.constant.Led): A mask of the LEDs to set, or unset.
		"""

		self._libinput.libinput_device_led_update(self._handle, leds)

	@property
	def capabilities(self):
		"""A tuple of capabilities this device supports.

		Returns:
			(~libinput.constant.DeviceCapability): Device capabilities.
		"""

		caps = []
		for cap in DeviceCapability:
			if self._libinput.libinput_device_has_capability(self._handle, cap):
				caps.append(cap)
		return tuple(caps)

	@property
	def size(self):
		"""The physical size of a device in mm, where meaningful.

		This property is only valid on devices with the required data, i.e.
		tablets, touchpads and touchscreens. For other devices this property
		raises :exc:`AssertionError`.

		Returns:
			(float, float): (Width, Height) in mm.
		Raises:
			AssertionError
		"""

		width = c_double(0)
		height = c_double(0)
		rc = self._libinput.libinput_device_get_size(
			self._handle, byref(width), byref(height))
		assert rc == 0, 'This device does not provide size information'
		return width.value, height.value

	@property
	def pointer(self):
		"""Methods specific to a device with
		:attr:`~libinput.constant.DeviceCapability.POINTER` capability.

		Returns:
			.DevicePointer:
		"""

		return self._pointer

	@property
	def keyboard(self):
		"""Methods specific to a device with
		:attr:`~libinput.constant.DeviceCapability.KEYBOARD` capability.

		Returns:
			.DeviceKeyboard:
		"""

		return self._keyboard

	@property
	def tablet_pad(self):
		"""Methods specific to a device with
		:attr:`~libinput.constant.DeviceCapability.TABLET_PAD` capability.

		Returns:
			.DeviceTabletPad:
		"""

		return self._tablet_pad

	@property
	def config(self):
		"""Device configuration.

		Returns:
			.DeviceConfig: An object providing device configuration methods.
		"""

		return self._config


class DevicePointer(BaseDevice):
	"""Methods specific to a device with
	:attr:`~libinput.constant.DeviceCapability.POINTER` capability.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

		self._libinput.libinput_device_pointer_has_button.argtypes = (
			c_void_p, c_uint32)
		self._libinput.libinput_device_pointer_has_button.restype = c_int


	def has_button(self, button):
		"""Check if this device has a given button.

		Args:
			button (int): Button to check for, see ``input.h`` for button
				definitions.
		Returns:
			bool: :obj:`True` if the device has this button, :obj:`False` if
			it does not.
		Raises:
			AssertionError
		"""

		rc = self._libinput.libinput_device_pointer_has_button(
			self._handle, button)
		assert rc >= 0, 'This device is not a pointer device'
		return bool(rc)


class DeviceKeyboard(BaseDevice):
	"""Methods specific to a device with
	:attr:`~libinput.constant.DeviceCapability.KEYBOARD` capability.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

		self._libinput.libinput_device_keyboard_has_key.argtypes = (
			c_void_p, c_uint32)
		self._libinput.libinput_device_keyboard_has_key.restype = c_int

	def has_key(self, key):
		"""Check if a :attr:`~libinput.constant.DeviceCapability.KEYBOARD`
		device has a given key.

		Args:
			key (int): Key to check for, see ``input.h`` for key definitions.
		Returns:
			bool: :obj:`True` if the device has this key, :obj:`False` if
			it does not.
		Raises:
			AssertionError
		"""

		rc = self._libinput.libinput_device_keyboard_has_key(self._handle, key)
		assert rc >= 0, 'This device is not a keyboard device'
		return bool(rc)


class DeviceTabletPad(BaseDevice):
	"""Methods specific to a device with
	:attr:`~libinput.constant.DeviceCapability.TABLET_PAD` capability.
	"""

	def __init__(self, *args):

		BaseDevice.__init__(self, *args)

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

	@property
	def num_buttons(self):
		"""The number of buttons on a device with
		the :attr:`~libinput.constant.DeviceCapability.TABLET_PAD` capability.

		Buttons on a pad device are numbered sequentially, see
		`Tablet pad button numbers`_ for details.

		Returns:
			int: The number of buttons supported by the device.
		Raises:
			AttributeError
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_buttons(
			self._handle)
		if num < 0:
			raise AttributeError('This device is not a tablet pad device')
		return num

	@property
	def num_rings(self):
		"""The number of rings a device with
		the :attr:`~libinput.constant.DeviceCapability.TABLET_PAD`
		capability provides.

		Returns:
			int: The number of rings or 0 if the device has no rings.
		Raises:
			AttributeError
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_rings(
			self._handle)
		if num < 0:
			raise AttributeError('This device is not a tablet pad device')
		return num

	@property
	def num_strips(self):
		"""The number of strips a device with
		the :attr:`~libinput.constant.DeviceCapability.TABLET_PAD`
		capability provides.

		Returns:
			int: The number of strips or 0 if the device has no strips.
		Raises:
			AttributeError
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_strips(
			self._handle)
		if num < 0:
			raise AttributeError('This device is not a tablet pad device')
		return num

	@property
	def num_mode_groups(self):
		"""Most devices only provide a single mode group, however devices
		such as the Wacom Cintiq 22HD provide two mode groups.

		If multiple mode groups are available, a caller should use
		:meth:`~libinput.define.TabletPadModeGroup.has_button`,
		:meth:`~libinput.define.TabletPadModeGroup.has_ring`
		and :meth:`~libinput.define.TabletPadModeGroup.has_strip` to associate
		each button, ring and strip with the correct mode group.

		Returns:
			int: The number of mode groups available on this device.
		Raises:
			AttributeError
		"""

		num = self._libinput.libinput_device_tablet_pad_get_num_mode_groups(
			self._handle)
		if num < 0:
			raise AttributeError('This device is not a tablet pad device')
		return num

	def get_mode_group(self, group):
		"""While a reference is kept by the caller, the returned mode group
		will compare equal with mode group returned by each subsequent call of
		this method with the same index and mode group returned from
		:attr:`~libinput.event.TabletPadEvent.mode_group`, provided
		the event was generated by this mode group.

		Args:
			group (int): A mode group index.
		Returns:
			~libinput.define.TabletPadModeGroup: The mode group with the given
			index or :obj:`None` if an invalid index is given.
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

	@property
	def physical_name(self):
		"""The physical name of the seat.

		For libinput contexts created from udev, this is always the same value
		as passed into :meth:`~libinput.LibInputUdev.assign_seat` and all
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

	@property
	def logical_name(self):
		"""The logical name of the seat.

		This is an identifier to group sets of devices within the compositor.

		Returns:
			str: The logical name of this seat.
		"""

		pchar = self._libinput.libinput_seat_get_logical_name(self._handle)
		return string_at(pchar).decode()
