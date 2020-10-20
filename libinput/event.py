#!/usr/bin/env python3

from __future__ import absolute_import
from ctypes import c_void_p, c_uint32, c_uint64, c_double, c_bool, c_int32
from .constant import EventType, ButtonState, PointerAxis, KeyState
from .constant import PointerAxisSource, Switch, SwitchState
from .device import Device
from .define import TabletTool, TabletPadModeGroup


_wrong_prop = 'This property is undefined for events of {} type.'
_wrong_meth = 'This method is undefined for events of {} type.'


class Event(object):
	"""Base class for device events.
	"""

	def __init__(self, hevent, libinput):

		self._libinput = libinput
		self._hevent = hevent

		self._libinput.libinput_event_destroy.argtypes = (c_void_p,)
		self._libinput.libinput_event_destroy.restype = None
		self._libinput.libinput_event_get_type.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_type.restype = EventType
		self._libinput.libinput_event_get_device.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_device.restype = c_void_p

	def __eq__(self, other):

		if issubclass(type(other), Event):
			return self._hevent == other._hevent
		else:
			return NotImplemented

	def __del__(self):

		self._libinput.libinput_event_destroy(self._hevent)

	@property
	def type(self):
		"""An enum describing event type.

		Returns:
			~libinput.constant.EventType: Event type.
		"""

		return self._libinput.libinput_event_get_type(self._hevent)

	@property
	def device(self):
		"""The device associated with this event.

		For device added/removed events this is the device added or removed.
		For all other device events, this is the device that generated the
		event.

		Returns:
			~libinput.define.Device: Device object.
		"""

		hdevice = self._libinput.libinput_event_get_device(self._hevent)
		return Device(hdevice, self._libinput)


class PointerEvent(Event):
	"""A pointer event.

	An event representing relative or absolute pointer movement, a button
	press/release or scroll axis events.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_pointer_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_pointer_event.restype = c_void_p
		self._libinput.libinput_event_pointer_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_time_usec.restype = c_uint64
		self._libinput.libinput_event_pointer_get_dx.argtypes = (c_void_p,)
		self._libinput.libinput_event_pointer_get_dx.restype = c_double
		self._libinput.libinput_event_pointer_get_dy.argtypes = (c_void_p,)
		self._libinput.libinput_event_pointer_get_dy.restype = c_double
		self._libinput.libinput_event_pointer_get_dx_unaccelerated.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_dx_unaccelerated.restype = (
			c_double)
		self._libinput.libinput_event_pointer_get_dy_unaccelerated.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_dy_unaccelerated.restype = (
			c_double)
		self._libinput.libinput_event_pointer_get_absolute_x.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_absolute_x.restype = c_double
		self._libinput.libinput_event_pointer_get_absolute_y.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_absolute_y.restype = c_double
		self._libinput \
			.libinput_event_pointer_get_absolute_x_transformed.argtypes = (
				c_void_p, c_uint32)
		self._libinput \
			.libinput_event_pointer_get_absolute_x_transformed.restype = (
				c_double)
		self._libinput \
			.libinput_event_pointer_get_absolute_y_transformed.argtypes = (
				c_void_p, c_uint32)
		self._libinput \
			.libinput_event_pointer_get_absolute_y_transformed.restype = (
				c_double)
		self._libinput.libinput_event_pointer_get_button.argtypes = (c_void_p,)
		self._libinput.libinput_event_pointer_get_button.restype = c_uint32
		self._libinput.libinput_event_pointer_get_button_state.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_button_state.restype = (
			ButtonState)
		self._libinput.libinput_event_pointer_get_seat_button_count.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_seat_button_count.restype = (
			c_uint32)
		self._libinput.libinput_event_pointer_has_axis.argtypes = (
			c_void_p, PointerAxis)
		self._libinput.libinput_event_pointer_has_axis.restype = c_bool
		self._libinput.libinput_event_pointer_get_axis_value.argtypes = (
			c_void_p, PointerAxis)
		self._libinput.libinput_event_pointer_get_axis_value.restype = c_double
		self._libinput.libinput_event_pointer_get_axis_source.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_pointer_get_axis_source.restype = (
			PointerAxisSource)
		self._libinput \
			.libinput_event_pointer_get_axis_value_discrete.argtypes = (
				c_void_p, PointerAxis)
		self._libinput \
			.libinput_event_pointer_get_axis_value_discrete.restype = c_double

		self._handle = self._libinput.libinput_event_get_pointer_event(
			self._hevent)

	@property
	def time(self):
		""".. note::
			Timestamps may not always increase. See `Event timestamps`_ for
			details.

		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_pointer_get_time_usec(self._handle)

	@property
	def delta(self):
		"""The delta between the last event and the current event.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_MOTION`, this property
		raises :exc:`AttributeError`.

		If a device employs pointer acceleration, the delta
		returned by this method is the accelerated delta.

		Relative motion deltas are to be interpreted as pixel movement of a
		standardized mouse. See `Normalization of relative motion`_
		for more details.

		Returns:
			(float, float): The relative (x, y) movement since the last event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_MOTION:
			raise AttributeError(_wrong_prop.format(self.type))
		delta_x = self._libinput.libinput_event_pointer_get_dx(self._handle)
		delta_y = self._libinput.libinput_event_pointer_get_dy(self._handle)
		return delta_x, delta_y

	@property
	def delta_unaccelerated(self):
		"""The relative delta of the unaccelerated motion vector of the
		current event.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_MOTION`, this property
		raises :exc:`AttributeError`.

		Relative unaccelerated motion deltas are raw device coordinates. Note
		that these coordinates are subject to the device's native resolution.
		Touchpad coordinates represent raw device coordinates in the
		(X, Y) resolution of the touchpad.
		See `Normalization of relative motion`_ for more details.

		Any rotation applied to the device also applies to unaccelerated motion
		(see :meth:`~libinput.define.Device.config_rotation_set_angle`).

		Returns:
			(float, float): The unaccelerated relative (x, y) movement since
			the last event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_MOTION:
			raise AttributeError(_wrong_prop.format(self.type))
		delta_x = self._libinput.libinput_event_pointer_get_dx_unaccelerated(
			self._handle)
		delta_y = self._libinput.libinput_event_pointer_get_dy_unaccelerated(
			self._handle)
		return delta_x, delta_y

	@property
	def absolute_coords(self):
		"""The current absolute coordinates of the pointer event,
		in mm from the top left corner of the device.

		To get the corresponding output screen coordinate, use
		:meth:`transform_absolute_coords`.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_MOTION_ABSOLUTE`,
		this property raises :exc:`AttributeError`.

		Returns:
			(float, float): The current absolute coordinates.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_MOTION_ABSOLUTE:
			raise AttributeError(_wrong_prop.format(self.type))
		abs_x = self._libinput.libinput_event_pointer_get_absolute_x(
			self._handle)
		abs_y = self._libinput.libinput_event_pointer_get_absolute_y(
			self._handle)
		return abs_x, abs_y

	def transform_absolute_coords(self, width, height):
		"""Return the current absolute coordinates of the pointer event,
		transformed to screen coordinates.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_MOTION_ABSOLUTE`,
		this method raises :exc:`AttributeError`.

		Args:
			width (int): The current output screen width.
			height (int): The current output screen height.
		Returns:
			(float, float): The current absolute (x, y) coordinates transformed
			to a screen coordinates.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_MOTION_ABSOLUTE:
			raise AttributeError(_wrong_meth.format(self.type))
		abs_x = self._libinput \
			.libinput_event_pointer_get_absolute_x_transformed(
				self._handle, width)
		abs_y = self._libinput \
			.libinput_event_pointer_get_absolute_y_transformed(
				self._handle, height)
		return abs_x, abs_y

	@property
	def button(self):
		"""The button that triggered this event.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_BUTTON`,
		this property raises :exc:`AttributeError`.

		Returns:
			int: The button triggering this event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_pointer_get_button(self._handle)

	@property
	def button_state(self):
		"""The button state that triggered this event.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_BUTTON`, this property
		raises :exc:`AttributeError`.

		Returns:
			~libinput.constant.ButtonState: The button state triggering this
			event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_pointer_get_button_state(
			self._handle)

	@property
	def seat_button_count(self):
		"""The total number of buttons pressed on all devices on the
		associated seat after the event was triggered.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_BUTTON`, this property
		raises :exc:`AssertionError`.

		Returns:
			int: The seat wide pressed button count for the key of this event.
		Raises:
			AssertionError
		"""

		if self.type != EventType.POINTER_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_pointer_get_seat_button_count(
			self._handle)

	def has_axis(self, axis):
		"""Check if the event has a valid value for the given axis.

		If this method returns True for an axis and :meth:`get_axis_value`
		returns a value of 0, the event is a scroll stop event.

		For pointer events that are not of type
		:attr:`~libinput.constant.EventType.POINTER_AXIS`, this method raises
		:exc:`AttributeError`.

		Args:
			axis (~libinput.constant.PointerAxis): The axis to check.
		Returns:
			bool: True if this event contains a value for this axis.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_AXIS:
			raise AttributeError(_wrong_meth.format(self.type))
		return self._libinput.libinput_event_pointer_has_axis(
			self._handle, axis)

	def get_axis_value(self, axis):
		"""Return the axis value of the given axis.

		The interpretation of the value depends on the axis. For the two
		scrolling axes :attr:`~libinput.constant.PointerAxis.SCROLL_VERTICAL`
		and :attr:`~libinput.constant.PointerAxis.SCROLL_HORIZONTAL`, the value
		of the event is in relative scroll units, with the positive direction
		being down or right, respectively. For the interpretation of the value,
		see :attr:`axis_source`.

		If :meth:`has_axis` returns False for an axis, this method returns 0
		for that axis.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_AXIS`, this method raises
		:exc:`AttributeError`.

		Args:
			axis (~libinput.constant.PointerAxis): The axis who's value to get.
		Returns:
			float: The axis value of this event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_AXIS:
			raise AttributeError(_wrong_meth.format(self.type))
		return self._libinput.libinput_event_pointer_get_axis_value(
			self._handle, axis)

	@property
	def axis_source(self):
		"""The source for a given axis event.

		Axis events (scroll events) can be caused by a hardware item such as
		a scroll wheel or emulated from other input sources, such as two-finger
		or edge scrolling on a touchpad.

		If the source is :attr:`~libinput.constant.PointerAxisSource.FINGER`,
		libinput guarantees that a scroll sequence is terminated with a scroll
		value of 0. A caller may use this information to decide on whether
		kinetic scrolling should be triggered on this scroll sequence. The
		coordinate system is identical to the cursor movement, i.e. a scroll
		value of 1 represents the equivalent relative motion of 1.
		If the source is :attr:`~libinput.constant.PointerAxisSource.WHEEL`,
		no terminating event is guaranteed (though it may happen). Scrolling
		is in discrete steps, the value is the angle the wheel moved in
		degrees. The default is 15 degrees per wheel click, but some mice may
		have differently grained wheels. It is up to the caller how to
		interpret such different step sizes.

		If the source is :attr:`~libinput.constant.PointerAxisSource.CONTINUOUS`,
		no terminating event is guaranteed (though it may happen). The
		coordinate system is identical to the cursor movement, i.e. a scroll
		value of 1 represents the equivalent relative motion of 1.
		If the source is :attr:`~libinput.constant.PointerAxisSource.WHEEL_TILT`,
		no terminating event is guaranteed (though it may happen). Scrolling
		is in discrete steps and there is no physical equivalent for the value
		returned here. For backwards compatibility, the value of this
		property is identical to a single mouse wheel rotation by this device
		(see the documentation for
		:attr:`~libinput.constant.PointerAxisSource.WHEEL` above). Callers
		should not use this value but instead exclusively refer to the value
		returned by :meth:`get_axis_value_discrete`.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_AXIS`, this property raises
		:exc:`AttributeError`.

		Returns:
			~libinput.constant.PointerAxisSource: The source for this axis
			event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_AXIS:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_pointer_get_axis_source(
			self._handle)

	def get_axis_value_discrete(self, axis):
		"""Return the axis value in discrete steps for a given axis event.

		How a value translates into a discrete step depends on the source.
		If the source is :attr:`~libinput.constant.PointerAxisSource.WHEEL`,
		the discrete value correspond to the number of physical mouse wheel
		clicks.

		If the source is :attr:`~libinput.constant.PointerAxisSource.CONTINUOUS`
		or :attr:`~libinput.constant.PointerAxisSource.FINGER`, the discrete
		value is always 0.

		Args:
			axis (~libinput.constant.PointerAxis): The axis who's value to get.
		Returns:
			float: The discrete value for the given event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.POINTER_AXIS:
			raise AttributeError(_wrong_meth.format(self.type))
		return self._libinput.libinput_event_pointer_get_axis_value_discrete(
			self._handle, axis)


class KeyboardEvent(Event):
	"""A keyboard event representing a key press/release.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_keyboard_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_keyboard_event.restype = c_void_p
		self._libinput.libinput_event_keyboard_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_keyboard_get_time_usec.restype = c_uint64
		self._libinput.libinput_event_keyboard_get_key.argtypes = (c_void_p,)
		self._libinput.libinput_event_keyboard_get_key.restype = c_uint32
		self._libinput.libinput_event_keyboard_get_key_state.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_keyboard_get_key_state.restype = KeyState
		self._libinput.libinput_event_keyboard_get_seat_key_count.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_keyboard_get_seat_key_count.restype = (
			c_uint32)

		self._handle = self._libinput.libinput_event_get_keyboard_event(
			self._hevent)

	@property
	def time(self):
		""".. note::
			Timestamps may not always increase. See `Event timestamps`_ for
			details.

		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_keyboard_get_time_usec(
			self._handle)

	@property
	def key(self):
		"""The keycode that triggered this event.

		Returns:
			int: The keycode that triggered this key event.
		"""

		return self._libinput.libinput_event_keyboard_get_key(self._handle)

	@property
	def key_state(self):
		"""The logical state of the key.

		Returns:
			~libinput.constant.KeyState: The state change of the key.
		"""

		return self._libinput.libinput_event_keyboard_get_key_state(
			self._handle)

	@property
	def seat_key_count(self):
		"""The total number of keys pressed on all devices on the
		associated seat after the event was triggered.

		Returns:
			int: The seat wide pressed key count for the key of this event.
		"""

		return self._libinput.libinput_event_keyboard_get_seat_key_count(
			self._handle)


class TouchEvent(Event):
	"""Touch event representing a touch down, move or up, as well as
	a touch cancel and touch frame events.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_touch_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_touch_event.restype = c_void_p
		self._libinput.libinput_event_touch_get_time_usec.argtypes = (c_void_p,)
		self._libinput.libinput_event_touch_get_time_usec.restype = c_uint64
		self._libinput.libinput_event_touch_get_slot.argtypes = (c_void_p,)
		self._libinput.libinput_event_touch_get_slot.restype = c_int32
		self._libinput.libinput_event_touch_get_seat_slot.argtypes = (c_void_p,)
		self._libinput.libinput_event_touch_get_seat_slot.restype = c_int32
		self._libinput.libinput_event_touch_get_x.argtypes = (c_void_p,)
		self._libinput.libinput_event_touch_get_x.restype = c_double
		self._libinput.libinput_event_touch_get_y.argtypes = (c_void_p,)
		self._libinput.libinput_event_touch_get_y.restype = c_double
		self._libinput.libinput_event_touch_get_x_transformed.argtypes = (
			c_void_p, c_uint32)
		self._libinput.libinput_event_touch_get_x_transformed.restype = c_double
		self._libinput.libinput_event_touch_get_y_transformed.argtypes = (
			c_void_p, c_uint32)
		self._libinput.libinput_event_touch_get_y_transformed.restype = c_double

		self._handle = self._libinput.libinput_event_get_touch_event(
			self._hevent)

	@property
	def time(self):
		""".. note::
			Timestamps may not always increase. See `Event timestamps`_ for
			details.

		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_touch_get_time_usec(self._handle)

	@property
	def slot(self):
		"""The slot of this touch event.

		See the kernel's multitouch protocol B documentation for more
		information.

		If the touch event has no assigned slot, for example if it is from
		a single touch device, this property returns -1.

		For events not of type :attr:`~libinput.constant.EventType.TOUCH_DOWN`,
		:attr:`~libinput.constant.EventType.TOUCH_UP`,
		:attr:`~libinput.constant.EventType.TOUCH_MOTION` or
		:attr:`~libinput.constant.EventType.TOUCH_CANCEL`, this property
		raises :exc:`AttributeError`.

		Returns:
			int: The slot of this touch event.
		Raises:
			AttributeError
		"""

		if self.type == EventType.TOUCH_FRAME:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_touch_get_slot(self._handle)

	@property
	def seat_slot(self):
		"""The seat slot of the touch event.

		A seat slot is a non-negative seat wide unique identifier of an active
		touch point.

		Events from single touch devices will be represented as one individual
		touch point per device.

		For events not of type :attr:`~libinput.constant.EventType.TOUCH_DOWN`,
		:attr:`~libinput.constant.EventType.TOUCH_UP`,
		:attr:`~libinput.constant.EventType.TOUCH_MOTION` or
		:attr:`~libinput.constant.EventType.TOUCH_CANCEL`, this property
		raises :exc:`AssertionError`.

		Returns:
			int: The seat slot of the touch event.
		Raises:
			AssertionError
		"""

		if self.type == EventType.TOUCH_FRAME:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_touch_get_seat_slot(self._handle)

	@property
	def coords(self):
		"""The current absolute coordinates of the touch event,
		in mm from the top left corner of the device.

		To get the corresponding output screen coordinates, use
		:meth:`transform_coords`.

		For events not of type :attr:`~libinput.constant.EventType.TOUCH_DOWN`,
		:attr:`~libinput.constant.EventType.TOUCH_MOTION`, this property
		raises :exc:`AttributeError`.

		Returns:
			(float, float): The current absolute (x, y) coordinates.
		Raises:
			AttributeError
		"""

		if self.type not in {EventType.TOUCH_DOWN, EventType.TOUCH_MOTION}:
			raise AttributeError(_wrong_prop.format(self.type))
		x = self._libinput.libinput_event_touch_get_x(self._handle)
		y = self._libinput.libinput_event_touch_get_y(self._handle)
		return x, y

	def transform_coords(self, width, height):
		"""Return the current absolute coordinates of the touch event,
		transformed to screen coordinates.

		For events not of type :attr:`~libinput.constant.EventType.TOUCH_DOWN`,
		:attr:`~libinput.constant.EventType.TOUCH_MOTION`, this method
		raises :exc:`AttributeError`.

		Args:
			width (int): The current output screen width.
			height (int): The current output screen height.
		Returns:
			(float, float): The current absolute (x, y) coordinates transformed
			to screen coordinates.
		"""

		if self.type not in {EventType.TOUCH_DOWN, EventType.TOUCH_MOTION}:
			raise AttributeError(_wrong_meth.format(self.type))
		x = self._libinput.libinput_event_touch_get_x_transformed(
			self._handle, width)
		y = self._libinput.libinput_event_touch_get_y_transformed(
			self._handle, height)
		return x, y


class GestureEvent(Event):
	"""A gesture event representing gesture on a touchpad.

	Gesture sequences always start with a
	:attr:`~libinput.constant.EventType.GESTURE_FOO_START` event. All following
	gesture events will be of the
	:attr:`~libinput.constant.EventType.GESTURE_FOO_UPDATE` type until
	a :attr:`~libinput.constant.EventType.GESTURE_FOO_END` is generated which
	signals the end of the gesture.

	See `Gestures`_ for more information on gesture handling.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_gesture_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_gesture_event.restype = c_void_p
		self._libinput.libinput_event_gesture_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_gesture_get_time_usec.restype = c_uint64
		self._libinput.libinput_event_gesture_get_finger_count.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_gesture_get_finger_count.restype = c_int
		self._libinput.libinput_event_gesture_get_cancelled.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_gesture_get_cancelled.restype = c_bool
		self._libinput.libinput_event_gesture_get_dx.argtypes = (c_void_p,)
		self._libinput.libinput_event_gesture_get_dx.restype = c_double
		self._libinput.libinput_event_gesture_get_dy.argtypes = (c_void_p,)
		self._libinput.libinput_event_gesture_get_dy.restype = c_double
		self._libinput.libinput_event_gesture_get_dx_unaccelerated.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_gesture_get_dx_unaccelerated.restype = (
			c_double)
		self._libinput.libinput_event_gesture_get_dy_unaccelerated.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_gesture_get_dy_unaccelerated.restype = (
			c_double)
		self._libinput.libinput_event_gesture_get_scale.argtypes = (c_void_p,)
		self._libinput.libinput_event_gesture_get_scale.restype = c_double
		self._libinput.libinput_event_gesture_get_angle_delta.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_gesture_get_angle_delta.restype = (
			c_double)

		self._handle = self._libinput.libinput_event_get_gesture_event(
			self._hevent)

	@property
	def time(self):
		""".. note::
			Timestamps may not always increase. See `Event timestamps`_ for
			details.

		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_gesture_get_time_usec(self._handle)

	@property
	def finger_count(self):
		"""The number of fingers used for a gesture.

		This can be used e.g. to differentiate between 3 or 4 finger swipes.
		This property is valid for all gesture events and the returned
		finger count value will not change during a sequence.

		Returns:
			int: The number of fingers used for a gesture.
		"""

		return self._libinput.libinput_event_gesture_get_finger_count(
			self._handle)

	@property
	def cancelled(self):
		"""Return if the gesture ended normally, or if it was cancelled.

		For gesture events that are not of type
		:attr:`~libinput.constant.EventType.GESTURE_SWIPE_END` or
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_END`, this property
		raises :exc:`AttributeError`.

		Returns:
			bool: :obj:`True` indicating that the gesture was cancelled.
		Raises:
			AttributeError
		"""

		if self.type not in {EventType.GESTURE_SWIPE_END,
				EventType.GESTURE_PINCH_END}:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_gesture_get_cancelled(self._handle)

	@property
	def delta(self):
		"""The delta between the last event and the current event.

		For gesture events that are not of type
		:attr:`~libinput.constant.EventType.GESTURE_SWIPE_UPDATE` or
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_UPDATE`, this
		property raises :exc:`AttributeError`.

		If a device employs pointer acceleration, the delta returned by this
		property is the accelerated delta.

		Relative motion deltas are normalized to represent those of a device
		with 1000dpi resolution. See `Normalization of relative motion`_
		for more details.

		Returns:
			(float, float): The relative (x, y) movement since the last event.
		"""

		if self.type not in {EventType.GESTURE_SWIPE_UPDATE,
				EventType.GESTURE_PINCH_UPDATE}:
			raise AttributeError(_wrong_prop.format(self.type))
		delta_x = self._libinput.libinput_event_gesture_get_dx(self._handle)
		delta_y = self._libinput.libinput_event_gesture_get_dy(self._handle)
		return delta_x, delta_y

	@property
	def delta_unaccelerated(self):
		"""The relative delta of the unaccelerated motion vector of
		the current event.

		For gesture events that are not of type
		:attr:`~libinput.constant.EventType.GESTURE_SWIPE_UPDATE` or
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_UPDATE`, this
		property raises :exc:`AttributeError`.

		Relative unaccelerated motion deltas are normalized to represent those
		of a device with 1000dpi resolution. See
		`Normalization of relative motion`_ for more details.
		Note that unaccelerated events are not equivalent to 'raw' events
		as read from the device.

		Any rotation applied to the device also applies to gesture motion
		(see :meth:`~libinput.define.DeviceConfigRotation.set_angle`).

		Returns:
			(float, float): The unaccelerated relative (x, y) movement since
			the last event.
		"""

		if self.type not in {EventType.GESTURE_SWIPE_UPDATE,
				EventType.GESTURE_PINCH_UPDATE}:
			raise AttributeError(_wrong_prop.format(self.type))
		delta_x = self._libinput.libinput_event_gesture_get_dx_unaccelerated(
			self._handle)
		delta_y = self._libinput.libinput_event_gesture_get_dy_unaccelerated(
			self._handle)
		return delta_x, delta_y

	@property
	def scale(self):
		"""The absolute scale of a pinch gesture, the scale is
		the division of the current distance between the fingers and
		the distance at the start of the gesture.

		The scale begins at 1.0, and if e.g. the fingers moved together by
		50% then the scale will become 0.5, if they move twice as far apart
		as initially the scale becomes 2.0, etc.

		For gesture events that are of type
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_BEGIN`, this property
		returns 1.0.

		For gesture events that are of type
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_END`, this property
		returns the scale value of the most recent
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_UPDATE` event
		(if any) or 1.0 otherwise.

		For all other events this property raises :exc:`AttributeError`.

		Returns:
			float: The absolute scale of a pinch gesture.
		Raises:
			AttributeError
		"""

		if self.type not in {EventType.GESTURE_PINCH_BEGIN,
				EventType.GESTURE_PINCH_UPDATE, EventType.GESTURE_PINCH_END}:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_gesture_get_scale(self._handle)

	@property
	def angle_delta(self):
		"""The angle delta in degrees between the last and the current
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_UPDATE` event.

		For gesture events that are not of type
		:attr:`~libinput.constant.EventType.GESTURE_PINCH_UPDATE`, this
		property raises :exc:`AttributeError`.

		The angle delta is defined as the change in angle of the line formed
		by the 2 fingers of a pinch gesture. Clockwise rotation is represented
		by a positive delta, counter-clockwise by a negative delta. If e.g.
		the fingers are on the 12 and 6 location of a clock face plate and
		they move to the 1 resp. 7 location in a single event then the angle
		delta is 30 degrees.

		If more than two fingers are present, the angle represents
		the rotation around the center of gravity. The calculation of
		the center of gravity is implementation-dependent.

		Returns:
			float: The angle delta since the last event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.GESTURE_PINCH_UPDATE:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_gesture_get_angle_delta(
			self._handle)


class TabletToolEvent(Event):
	"""Tablet tool event representing an axis update, button press,
	or tool update.

	Valid event types for this event are
	:attr:`~libinput.constant.EventType.TABLET_TOOL_AXIS`,
	:attr:`~libinput.constant.EventType.TABLET_TOOL_PROXIMITY`,
	:attr:`~libinput.constant.EventType.TABLET_TOOL_TIP`
	and :attr:`~libinput.constant.EventType.TABLET_TOOL_BUTTON`.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_tablet_tool_event.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_get_tablet_tool_event.restype = c_void_p
		self._libinput.libinput_event_tablet_tool_x_has_changed.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_x_has_changed.restype = (
			c_bool)
		self._libinput.libinput_event_tablet_tool_y_has_changed.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_y_has_changed.restype = (
			c_bool)
		self._libinput \
			.libinput_event_tablet_tool_pressure_has_changed.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_pressure_has_changed.restype = c_bool
		self._libinput \
			.libinput_event_tablet_tool_distance_has_changed.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_distance_has_changed.restype = c_bool
		self._libinput \
			.libinput_event_tablet_tool_tilt_x_has_changed.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_tilt_x_has_changed.restype = c_bool
		self._libinput \
			.libinput_event_tablet_tool_tilt_y_has_changed.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_tilt_y_has_changed.restype = c_bool
		self._libinput \
			.libinput_event_tablet_tool_rotation_has_changed.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_rotation_has_changed.restype = c_bool
		self._libinput \
			.libinput_event_tablet_tool_slider_has_changed.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_slider_has_changed.restype = c_bool
		self._libinput \
			.libinput_event_tablet_tool_wheel_has_changed.argtypes = (c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_wheel_has_changed.restype = c_bool
		self._libinput.libinput_event_tablet_tool_get_x.argtypes = (c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_x.restype = c_double
		self._libinput.libinput_event_tablet_tool_get_y.argtypes = (c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_y.restype = c_double
		self._libinput.libinput_event_tablet_tool_get_dx.argtypes = (c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_dx.restype = c_double
		self._libinput.libinput_event_tablet_tool_get_dy.argtypes = (c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_dy.restype = c_double
		self._libinput.libinput_event_tablet_tool_get_pressure.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_pressure.restype = (
			c_double)
		self._libinput.libinput_event_tablet_tool_get_distance.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_distance.restype = (
			c_double)
		self._libinput.libinput_event_tablet_tool_get_tilt_x.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_tilt_x.restype = c_double
		self._libinput.libinput_event_tablet_tool_get_tilt_y.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_tilt_y.restype = c_double
		self._libinput.libinput_event_tablet_tool_get_rotation.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_rotation.restype = (
			c_double)
		self._libinput \
			.libinput_event_tablet_tool_get_slider_position.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_get_slider_position.restype = c_double
		self._libinput.libinput_event_tablet_tool_get_wheel_delta.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_wheel_delta.restype = (
			c_double)
		self._libinput \
			.libinput_event_tablet_tool_get_wheel_delta_discrete.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_get_wheel_delta_discrete.restype = (
				c_int)
		self._libinput.libinput_event_tablet_tool_get_x_transformed.argtypes = (
			c_void_p, c_uint32)
		self._libinput.libinput_event_tablet_tool_get_x_transformed.restype = (
			c_double)
		self._libinput.libinput_event_tablet_tool_get_y_transformed.argtypes = (
			c_void_p, c_uint32)
		self._libinput.libinput_event_tablet_tool_get_y_transformed.restype = (
			c_double)
		self._libinput.libinput_event_tablet_tool_get_tool.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_tool.restype = c_void_p
		self._libinput \
			.libinput_event_tablet_tool_get_proximity_state.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_get_proximity_state.restype = (
				TabletToolProximityState)
		self._libinput.libinput_event_tablet_tool_get_tip_state.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_tip_state.restype = (
			TabletToolTipState)
		self._libinput.libinput_event_tablet_tool_get_button.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_button.restype = c_uint32
		self._libinput.libinput_event_tablet_tool_get_button_state.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_button_state.restype = (
			ButtonState)
		self._libinput \
			.libinput_event_tablet_tool_get_seat_button_count.argtypes = (
				c_void_p,)
		self._libinput \
			.libinput_event_tablet_tool_get_seat_button_count.restype = (
				c_uint32)
		self._libinput.libinput_event_tablet_tool_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_time_usec.restype = (
			c_uint64)

		self._handle = self._libinput.libinput_event_get_tablet_tool_event(
			self._hevent)

	@property
	def coords(self):
		"""The (X, Y) coordinates of the tablet tool, in mm from
		the top left corner of the tablet in its current logical orientation
		and whether they have changed in this event.

		Use :meth:`transform_coords` for transforming the axes values into
		a different coordinate space.

		Note:
			On some devices, returned value may be negative or larger than
			the width of the device. See `Out-of-bounds motion events`_
			for more details.
		Returns:
			((float, float), bool): The current values of the the axes and
			whether they have changed.
		"""

		x_changed = self._libinput.libinput_event_tablet_tool_x_has_changed(
			self._handle)
		y_changed = self._libinput.libinput_event_tablet_tool_y_has_changed(
			self._handle)
		x = self._libinput.libinput_event_tablet_tool_get_x(self._handle)
		y = self._libinput.libinput_event_tablet_tool_get_y(self._handle)
		return (x, y), x_changed or y_changed

	@property
	def delta(self):
		"""The delta between the last event and the current event.

		If the tool employs pointer acceleration, the delta contained in this
		property is the accelerated delta.

		This value is in screen coordinate space, the delta is to be
		interpreted like the value of :attr:`.PointerEvent.delta`.
		See `Relative motion for tablet tools`_ for more details.

		Returns:
			(float, float): The relative (x, y) movement since the last event.
		"""

		delta_x = self._libinput.libinput_event_tablet_tool_get_dx(self._handle)
		delta_y = self._libinput.libinput_event_tablet_tool_get_dy(self._handle)
		return delta_x, delta_y

	@property
	def pressure(self):
		"""The current pressure being applied on the tool in use,
		normalized to the range [0, 1] and whether it has changed in this event.

		If this axis does not exist on the current tool, this property is
		(0, :obj:`False`).

		Returns:
			(float, bool): The current value of the the axis and whether it has
			changed.
		"""

		pressure = self._libinput.libinput_event_tablet_tool_get_pressure(
			self._handle)
		changed = self._libinput. \
			libinput_event_tablet_tool_pressure_has_changed(self._handle)
		return pressure, changed

	@property
	def distance(self):
		"""The current distance from the tablet's sensor,
		normalized to the range [0, 1] and whether it has changed in this event.

		If this axis does not exist on the current tool, this property is
		(0, :obj:`False`).

		Returns:
			(float, bool): The current value of the the axis.
		"""

		distance = self._libinput.libinput_event_tablet_tool_get_distance(
			self._handle)
		changed = self._libinput. \
			libinput_event_tablet_tool_distance_has_changed(self._handle)
		return distance, changed

	@property
	def tilt_axes(self):
		"""The current tilt along the (X, Y) axes of the tablet's
		current logical orientation, in degrees off the tablet's Z axis
		and whether they have changed in this event.

		That is, if the tool is perfectly orthogonal to the tablet,
		the tilt angle is 0. When the top tilts towards the logical top/left
		of the tablet, the x/y tilt angles are negative, if the top tilts
		towards the logical bottom/right of the tablet, the x/y tilt angles
		are positive.

		If these axes do not exist on the current tool, this property returns
		((0, 0), :obj:`False`).

		Returns:
			((float, float), bool): The current value of the axes in degrees
			and whether it has changed.
		"""

		tilt_x = self._libinput.libinput_event_tablet_tool_get_tilt_x(
			self._handle)
		tilt_y = self._libinput.libinput_event_tablet_tool_get_tilt_y(
			self._handle)
		x_changed = self._libinput. \
			libinput_event_tablet_tool_tilt_x_has_changed(self._handle)
		y_changed = self._libinput. \
			libinput_event_tablet_tool_tilt_y_has_changed(self._handle)
		return (tilt_x, tilt_y), x_changed or y_changed

	@property
	def rotation(self):
		"""The current Z rotation of the tool in degrees, clockwise
		from the tool's logical neutral position and whether it has changed
		in this event.

		For tools of type :attr:`~libinput.constant.TabletToolType.MOUSE`
		and :attr:`~libinput.constant.TabletToolType.LENS` the logical
		neutral position is pointing to the current logical north
		of the tablet. For tools of type
		:attr:`~libinput.constant.TabletToolType.BRUSH`, the logical
		neutral position is with the buttons pointing up.

		If this axis does not exist on the current tool, this property is
		(0, :obj:`False`).

		Returns:
			(float, bool): The current value of the the axis and whether it has
			changed.
		"""

		rotation = self._libinput.libinput_event_tablet_tool_get_rotation(
			self._handle)
		changed = self._libinput. \
			libinput_event_tablet_tool_rotation_has_changed(self._handle)
		return rotation, changed

	@property
	def slider_position(self):
		"""The current position of the slider on the tool,
		normalized to the range [-1, 1] and whether it has changed in this
		event.

		The logical zero is the neutral position of the slider, or
		the logical center of the axis. This axis is available on e.g.
		the Wacom Airbrush.

		If this axis does not exist on the current tool, this property is
		(0, :obj:`False`).

		Returns:
			(float, bool): The current value of the the axis.
		"""

		position = self._libinput. \
			libinput_event_tablet_tool_get_slider_position(self._handle)
		changed = self._libinput.libinput_event_tablet_tool_slider_has_changed(
			self._handle)
		return position, changed

	@property
	def wheel_delta(self):
		"""The delta for the wheel in degrees and whether it has changed in
		this event.

		Returns:
			(float, bool): The delta of the wheel, in degrees, compared to
			the last event and whether it has changed.
		"""

		delta = self._libinput.libinput_event_tablet_tool_get_wheel_delta(
			self._handle)
		changed = self._libinput.libinput_event_tablet_tool_wheel_has_changed(
			self._handle)
		return delta, changed

	@property
	def wheel_delta_discrete(self):
		"""The delta for the wheel in discrete steps (e.g. wheel clicks) and
		whether it has changed in this event.

		Returns:
			(int, bool): The delta of the wheel, in discrete steps, compared to
			the last event and whether it has changed.
		"""

		delta =  self._libinput. \
			libinput_event_tablet_tool_get_wheel_delta_discrete(self._handle)
		changed = self._libinput.libinput_event_tablet_tool_wheel_has_changed(
			self._handle)
		return delta, changed

	def transform_coords(self, width, height):
		"""Return the current absolute (x, y) coordinates of
		the tablet tool event, transformed to screen coordinates and
		whether they have changed in this event.

		Note:
			On some devices, returned value may be negative or larger than
			the width of the device. See `Out-of-bounds motion events`_
			for more details.
		Args:
			width (int): The current output screen width.
			height (int): The current output screen height.
		Returns:
			((float, float), bool): The current absolute (x, y) coordinates
			transformed to screen coordinates and whether they have changed.
		"""

		x = self._libinput.libinput_event_tablet_tool_get_x_transformed(
			self._handle, width)
		y = self._libinput.libinput_event_tablet_tool_get_y_transformed(
			self._handle, height)
		x_changed = self._libinput.libinput_event_tablet_tool_x_has_changed(
			self._handle)
		y_changed = self._libinput.libinput_event_tablet_tool_y_has_changed(
			self._handle)
		return (x, y), x_changed or y_changed

	@property
	def tool(self):
		"""The tool that was in use during this event.

		If the caller keeps a reference to a tool, the tool object will
		compare equal to the previously obtained tool object.

		Note:
			Physical tool tracking requires hardware support. If unavailable,
			libinput creates one tool per type per tablet. See
			`Tracking unique tools`_ for more details.
		Returns:
			~libinput.define.TabletTool: The new tool triggering this event.
		"""

		htablettool = self._libinput.libinput_event_tablet_tool_get_tool(
			self._handle)
		return TabletTool(htablettool, self._libinput)

	@property
	def proximity_state(self):
		"""The new proximity state of a tool from a proximity event.

		Used to check whether or not a tool came in or out of proximity during
		an event of type
		:attr:`~libinput.constant.EventType.TABLET_TOOL_PROXIMITY`.

		See `Handling of proximity events`_ for
		recommendations on proximity handling.

		Returns:
			~libinput.constant.TabletToolProximityState: The new proximity
			state of the tool from the event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_proximity_state(
			self._handle)

	@property
	def tip_state(self):
		"""The new tip state of a tool from a tip event.

		Used to check whether or not a tool came in contact with
		the tablet surface or left contact with the tablet surface during
		an event of type :attr:`~libinput.constant.EventType.TABLET_TOOL_TIP`.

		Returns:
			~libinput.constant.TabletToolTipState: The new tip state of
			the tool from the event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_tip_state(
			self._handle)

	@property
	def button(self):
		"""The button that triggered this event.

		For events that are not of type
		:attr:`~libinput.constant.EventType.TABLET_TOOL_BUTTON`, this property
		raises :exc:`AttributeError`.

		Returns:
			int: The button triggering this event.
		"""

		if self.type != EventType.TABLET_TOOL_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_tool_get_button(
			self._handle)

	@property
	def button_state(self):
		"""The button state of the event.

		For events that are not of type
		:attr:`~libinput.constant.EventType.TABLET_TOOL_BUTTON`, this property
		raises :exc:`AttributeError`.

		Returns:
			~libinput.constant.ButtonState: The button state triggering
			this event.
		"""

		if self.type != EventType.TABLET_TOOL_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_tool_get_button_state(
			self._handle)

	@property
	def seat_button_count(self):
		"""The total number of buttons pressed on all devices on
		the associated seat after the the event was triggered.

		For events that are not of type
		:attr:`~libinput.constant.EventType.TABLET_TOOL_BUTTON`, this property
		raises :exc:`AttributeError`.

		Returns:
			int: The seat wide pressed button count for the key of this event.
		"""

		if self.type != EventType.TABLET_TOOL_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_tool_get_seat_button_count(
			self._handle)

	@property
	def time(self):
		""".. note::
			Timestamps may not always increase. See `Event timestamps`_ for
			details.

		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_tablet_tool_get_time_usec(
			self._handle)


class TabletPadEvent(Event):
	"""Tablet pad event representing a button press or ring/strip update
	on the tablet pad itself.

	Valid event types for this event are
	:attr:`~libinput.constant.EventType.TABLET_PAD_BUTTON`,
	:attr:`~libinput.constant.EventType.TABLET_PAD_RING`
	and :attr:`~libinput.constant.EventType.TABLET_PAD_STRIP`.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_tablet_pad_event.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_get_tablet_pad_event.restype = c_void_p
		self._libinput.libinput_event_tablet_pad_get_ring_position.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_ring_position.restype = (
			c_double)
		self._libinput.libinput_event_tablet_pad_get_ring_number.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_ring_number.restype = (
			c_uint)
		self._libinput.libinput_event_tablet_pad_get_ring_source.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_ring_source.restype = (
			TabletPadRingAxisSource)
		self._libinput.libinput_event_tablet_pad_get_strip_position.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_strip_position.restype = (
			c_double)
		self._libinput.libinput_event_tablet_pad_get_strip_number.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_strip_number.restype = (
			c_uint)
		self._libinput.libinput_event_tablet_pad_get_strip_source.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_strip_source.restype = (
			TabletPadStripAxisSource)
		self._libinput.libinput_event_tablet_pad_get_button_number.argtypes = (
			c_void_p)
		self._libinput.libinput_event_tablet_pad_get_button_number.restype = (
			c_uint32)
		self._libinput.libinput_event_tablet_pad_get_button_state.argtypes = (
			c_void_p)
		self._libinput.libinput_event_tablet_pad_get_button_state.restype = (
			ButtonState)
		self._libinput.libinput_event_tablet_pad_get_mode.argtypes = (c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_mode.restype = c_uint
		self._libinput.libinput_event_tablet_pad_get_mode_group.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_mode_group.restype = (
			c_void_p)
		self._libinput.libinput_event_tablet_pad_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_time_usec.restype = (
			c_uint64)

		self._handle = self._libinput.libinput_event_get_tablet_pad_event(
			self._hevent)

	@property
	def ring_position(self):
		"""The current position of the ring, in degrees
		counterclockwise from the northern-most point of the ring in
		the tablet's current logical orientation.

		If the source is
		:attr:`~libinput.constant.TabletPadRingAxisSource.FINGER`,
		libinput sends a terminating event with a ring value of -1 when
		the finger is lifted from the ring. A caller may use this information
		to e.g. determine if kinetic scrolling should be triggered.

		For events not of type
		:attr:`~libinput.constant.EventType.TABLET_PAD_RING`, this property
		raises :exc:`AttributeError`.

		Returns:
			float: The current value of the the axis. -1 if the finger was
			lifted.
		Raises:
			AttributeError
		"""

		if self.type != EventType.TABLET_PAD_RING:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_ring_position(
			self._handle)

	@property
	def ring_number(self):
		"""The number of the ring that has changed state,
		with 0 being the first ring.

		On tablets with only one ring, this method always returns 0.

		For events not of type
		:attr:`~libinput.constant.EventType.TABLET_PAD_RING`, this property
		raises :exc:`AssertionError`.

		Returns:
			int: The index of the ring that changed state.
		Raises:
			AssertionError
		"""

		if self.type != EventType.TABLET_PAD_RING:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_ring_number(
			self._handle)

	@property
	def ring_source(self):
		"""The source of the interaction with the ring.

		If the source is
		:attr:`~libinput.constant.TabletPadRingAxisSource.FINGER`,
		libinput sends a ring position value of -1 to terminate
		the current interaction.

		For events not of type
		:attr:`~libinput.constant.EventType.TABLET_PAD_RING`, this property
		raises :exc:`AttributeError`.

		Returns:
			~libinput.constant.TabletPadRingAxisSource: The source of the ring
			interaction.
		Raises:
			AttributeError
		"""

		if self.type != EventType.TABLET_PAD_RING:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_ring_source(
			self._handle)

	@property
	def strip_position(self):
		"""The current position of the strip, normalized to
		the range [0, 1], with 0 being the top/left-most point in the tablet's
		current logical orientation.

		If the source is
		:attr:`~libinput.constant.TabletPadStripAxisSource.FINGER`,
		libinput sends a terminating event with a value of -1 when the finger
		is lifted from the strip. A caller may use this information to e.g.
		determine if kinetic scrolling should be triggered.

		For events not of type
		:attr:`~libinput.constant.EventType.TABLET_PAD_STRIP`, this property
		raises :exc:`AttributeError`.

		Returns:
			float: The current value of the the axis. -1 if the finger was
			lifted.
		Raises:
			AttributeError
		"""

		if self.type != EventType.TABLET_PAD_STRIP:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_strip_position(
			self._handle)

	@property
	def strip_number(self):
		"""The number of the strip that has changed state,
		with 0 being the first strip.

		On tablets with only one strip, this method always returns 0.

		For events not of type
		:attr:`~libinput.constant.EventType.TABLET_PAD_STRIP`, this property
		raises :exc:`AttributeError`.

		Returns:
			int: The index of the strip that changed state.
		Raises:
			AttributeError
		"""

		if self.type != EventType.TABLET_PAD_STRIP:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_strip_number(
			self._handle)

	@property
	def strip_source(self):
		"""The source of the interaction with the strip.

		If the source is
		:attr:`~libinput.constant.TabletPadStripAxisSource.FINGER`, libinput
		sends a strip position value of -1 to terminate the current interaction.

		For events not of type
		:attr:`~libinput.constant.EventType.TABLET_PAD_STRIP`, this property
		raises :exc:`AttributeError`.

		Returns:
			~libinput.constant.TabletPadStripAxisSource: The source of
			the strip interaction.
		Raises:
			AttributeError
		"""

		if self.type != EventType.TABLET_PAD_STRIP:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_strip_source(
			self._handle)

	@property
	def button_number(self):
		"""The button number that triggered this event, starting at 0.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_PAD_BUTTON`,
		this property raises :exc:`AttributeError`.

		Note that the number returned is a generic sequential button number
		and not a semantic button code as defined in ``linux/input.h``.
		See `Tablet pad button numbers`_ for more details.

		Returns:
			int: The button triggering this event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.TABLET_PAD_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_button_number(
			self._handle)

	@property
	def button_state(self):
		"""The button state of the event.

		For events not of type
		:attr:`~libinput.constant.EventType.TABLET_PAD_BUTTON`, this property
		raises :exc:`AttributeError`.

		Returns:
			~libinput.constant.ButtonState: The button state triggering
			this event.
		Raises:
			AttributeError
		"""

		if self.type != EventType.TABLET_PAD_BUTTON:
			raise AttributeError(_wrong_prop.format(self.type))
		return self._libinput.libinput_event_tablet_pad_get_button_state(
			self._handle)

	@property
	def mode(self):
		"""The mode the button, ring, or strip that triggered
		this event is in, at the time of the event.

		The mode is a virtual grouping of functionality, usually based on
		some visual feedback like LEDs on the pad. See `Tablet pad modes`_
		for details. Mode indices start at 0, a device that does not support
		modes always returns 0.

		Mode switching is controlled by libinput and more than one mode
		may exist on the tablet. This method returns the mode that
		this event's button, ring or strip is logically in. If the button
		is a mode toggle button and the button event caused a new mode to
		be toggled, the mode returned is the new mode the button is in.

		Note that the returned mode is the mode valid as of the time of
		the event. The returned mode may thus be different to the mode
		returned by :attr:`~libinput.define.TabletPadModeGroup.mode`.
		See :attr:`~libinput.define.TabletPadModeGroup.mode` for details.

		Returns:
			int: The 0-indexed mode of this button, ring or strip at the time
			of the event.
		"""

		return self._libinput.libinput_event_tablet_pad_get_mode(self._handle)

	@property
	def mode_group(self):
		"""The mode group that the button, ring, or strip that
		triggered this event is considered in.

		The mode is a virtual grouping of functionality, usually based on some
		visual feedback like LEDs on the pad. See `Tablet pad modes`_
		for details.

		Returns:
			~libinput.define.TabletPadModeGroup: The mode group of the button,
			ring or strip that caused this event.
		"""

		hmodegroup = self._libinput.libinput_event_tablet_pad_get_mode_group(
			self._handle)
		return TabletPadModeGroup(hmodegroup, self._libinput)

	@property
	def time(self):
		""".. note::
			Timestamps may not always increase. See `Event timestamps`_ for
			details.

		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_tablet_pad_get_time_usec(
			self._handle)


class SwitchEvent(Event):
	"""A switch event representing a changed state in a switch.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_switch_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_switch_event.restype = c_void_p
		self._libinput.libinput_event_switch_get_switch.argtypes = (c_void_p,)
		self._libinput.libinput_event_switch_get_switch.restype = Switch
		self._libinput.libinput_event_switch_get_switch_state.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_switch_get_switch_state.restype = (
			SwitchState)
		self._libinput.libinput_event_switch_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_switch_get_time_usec.restype = c_uint64

		self._handle = self._libinput.libinput_event_get_switch_event(
			self._hevent)

	@property
	def switch(self):
		"""The switch that triggered this event.

		Returns:
			~libinput.constant.Switch: The switch triggering this event.
		"""

		return self._libinput.libinput_event_switch_get_switch(self._handle)

	@property
	def switch_state(self):
		"""The switch state that triggered this event.

		Returns:
			~libinput.constant.SwitchState: The switch state triggering this
			event.
		"""

		return self._libinput.libinput_event_switch_get_switch_state(
			self._handle)

	@property
	def time(self):
		""".. note::
			Timestamps may not always increase. See `Event timestamps`_ for
			details.

		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_switch_get_time_usec(self._handle)


class DeviceNotifyEvent(Event):
	"""An event notifying the caller of a device being added or removed.
	"""

	def __init__(self, *args):

		Event.__init__(self, *args)

		self._libinput.libinput_event_get_device_notify_event.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_get_device_notify_event.restype = c_void_p

		self._handle = self._libinput.libinput_event_get_device_notify_event(
			self._hevent)
