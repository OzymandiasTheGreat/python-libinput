#!/usr/bin/env python3

from __future__ import absolute_import
from ctypes import c_void_p, c_uint32, c_uint64, c_double, c_bool, c_int32
from ctypes import c_int
from .constant import Event as enumEvent, ButtonState, PointerAxis, KeyState
from .constant import PointerAxisSource, Switch, SwitchState
from .define import Device, TabletTool
from .evcodes import Key, Button


class BaseEvent(object):
	"""Base class all event classes inherit from.

	This class has no public methods and should not be used directly.
	"""

	def __init__(self, hevent, libinput):

		self._handle = hevent
		self._libinput = libinput

	def __eq__(self, other):

		if issubclass(type(other), BaseEvent):
			return self._handle == other._handle
		else:
			return NotImplemented


class Event(BaseEvent):
	"""Generic event.

	Use one of the methods to get device-specific event.

	Attributes:
		type: An enum describing event type.
	"""

	def __init__(self, *args):

		BaseEvent.__init__(self, *args)

		self._libinput.libinput_event_destroy.argtypes = (c_void_p,)
		self._libinput.libinput_event_destroy.restype = None
		self._libinput.libinput_event_get_type.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_type.restype = enumEvent
		self._libinput.libinput_event_get_device.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_device.restype = c_void_p
		self._libinput.libinput_event_get_pointer_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_pointer_event.restype = c_void_p
		self._libinput.libinput_event_get_keyboard_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_keyboard_event.restype = c_void_p
		self._libinput.libinput_event_get_touch_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_touch_event.restype = c_void_p
		self._libinput.libinput_event_get_gesture_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_gesture_event.restype = c_void_p
		self._libinput.libinput_event_get_tablet_tool_event.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_get_tablet_tool_event.restype = c_void_p
		self._libinput.libinput_event_get_tablet_pad_event.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_get_tablet_pad_event.restype = c_void_p
		self._libinput.libinput_event_get_switch_event.argtypes = (c_void_p,)
		self._libinput.libinput_event_get_switch_event.restype = c_void_p
		self._libinput.libinput_event_get_device_notify_event.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_get_device_notify_event.restype = c_void_p

		self.type = self._libinput.libinput_event_get_type(self._handle)

	def __del__(self):

		self._libinput.libinput_event_destroy(self._handle)

	def get_device(self):
		"""Return the device associated with this event.

		For device added/removed events this is the device added or removed.
		For all other device events, this is the device that generated the
		event.

		Returns:
			~libinput.define.Device: device object.
		"""

		hdevice = self._libinput.libinput_event_get_device(self._handle)
		return Device(hdevice, self._libinput)

	def get_pointer_event(self):
		"""Return the pointer event that is this input event.

		If the event type does not match the pointer event types, this
		method returns :obj:`None`.

		Returns:
			PointerEvent: A pointer event or :obj:`None`.
		"""

		pevent = self._libinput.libinput_event_get_pointer_event(self._handle)
		if pevent:
			return PointerEvent(pevent, self, self._libinput)
		return None

	def get_keyboard_event(self):
		"""Return the keyboard event that is this input event.

		If the event type does not match the keyboard event types, this
		method returns :obj:`None`.

		Returns:
			KeyboardEvent: A keyboard event or :obj:`None`.
		"""

		kevent = self._libinput.libinput_event_get_keyboard_event(self._handle)
		if kevent:
			return KeyboardEvent(kevent, self, self._libinput)
		return None

	def get_touch_event(self):
		"""Return the touch event that is this input event.

		If the event type does not match the touch event types, this
		method returns :obj:`None`.

		Returns:
			TouchEvent: A touch event or :obj:`None`.
		"""

		tevent = self._libinput.libinput_event_get_touch_event(self._handle)
		if tevent:
			return TouchEvent(tevent, self, self._libinput)
		return None

	def get_gesture_event(self):
		"""Return the gesture event that is this input event.

		If the event type does not match the gesture event types, this
		method returns :obj:`None`.

		Returns:
			GestureEvent: A gesture event or :obj:`None`.
		"""

		gevent = self._libinput.libinput_event_get_gesture_event(self._handle)
		if gevent:
			return GestureEvent(gevent, self, self._libinput)
		return None

	def get_tablet_tool_event(self):
		"""Return the tablet tool event that is this input event.

		If the event type does not match the tablet tool event types, this
		method returns :obj:`None`.

		Returns:
			TabletToolEvent: A tablet tool event or :obj:`None`.
		"""

		ttevent = self._libinput.libinput_event_get_tablet_tool_event(
			self._handle)
		if ttevent:
			return TabletToolEvent(ttevent, self, self._libinput)
		return None

	def get_tablet_pad_event(self):
		"""Return the tablet pad event that is this input event.

		If the event type does not match the tablet pad event types, this
		method returns :obj:`None`.

		Returns:
			TabletPadEvent: A tablet pad event or :obj:`None`.
		"""

		tpevent = self._libinput.libinput_event_get_tablet_pad_event(
			self._handle)
		if tpevent:
			return TabletPadEvent(tpevent, self, self._libinput)
		return None

	def get_switch_event(self):
		"""Return the switch event that is this input event.

		If the event type does not match the switch event types, this
		method returns :obj:`None`.

		Returns:
			SwitchEvent: A switch event or :obj:`None`.
		"""

		sevent = self._libinput.libinput_event_get_switch_event(self._handle)
		if sevent:
			return SwitchEvent(sevent, self, self._libinput)
		return None

	def get_device_notify_event(self):
		"""Return the device event that is this input event.

		If the event type does not match the device event types, this
		method returns :obj:`None`.

		Returns:
			DeviceNotifyEvent: A device event or :obj:`None`.
		"""

		dnevent = self._libinput.libinput_event_get_device_notify_event(
			self._handle)
		if dnevent:
			return DeviceNotifyEvent(dnevent, self, self._libinput)
		return None


class DeviceEvent(BaseEvent):
	"""A base class for device events.

	Attributes:
		base_event: A generic event this device event is derived from.
		type: An enum describing event type.
	"""

	def __init__(self, devent, base_event, libinput):

		BaseEvent.__init__(self, devent, libinput)
		self.base_event = base_event
		self.type = base_event.type


class PointerEvent(DeviceEvent):
	"""A pointer event.

	An event representing relative or absolute pointer movement, a button
	press/release or scroll axis events.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)

		self._libinput.libinput_event_pointer_get_time.argtypes = (c_void_p,)
		self._libinput.libinput_event_pointer_get_time.restype = c_uint32
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
		self._libinput.libinput_event_pointer_get_button.restype = Button
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

	def get_time(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event.
		"""

		return self._libinput.libinput_event_pointer_get_time(self._handle)

	def get_time_usec(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_pointer_get_time_usec(self._handle)

	def get_dx(self):
		"""Return the delta between the last event and the current event.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION`, this method returns 0.
		If a device employs pointer acceleration, the delta returned by this
		method is the accelerated delta.

		Relative motion deltas are to be interpreted as pixel movement of a
		standardized mouse. See `Normalization of relative motion`_
		for more details.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION`.
		Returns:
			float: The relative x movement since the last event.
		"""

		return self._libinput.libinput_event_pointer_get_dx(self._handle)

	def get_dy(self):
		"""Return the delta between the last event and the current event.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION`, this method returns 0.
		If a device employs pointer acceleration, the delta returned by this
		method is the accelerated delta.

		Relative motion deltas are to be interpreted as pixel movement of a
		standardized mouse. See `Normalization of relative motion`_
		for more details.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION`.
		Returns:
			float: The relative y movement since the last event.
		"""

		return self._libinput.libinput_event_pointer_get_dy(self._handle)

	def get_dx_unaccelerated(self):
		"""Return the relative delta of the unaccelerated motion vector of the
		current event.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION`, this method returns 0.

		Relative unaccelerated motion deltas are raw device coordinates. Note
		that these coordinates are subject to the device's native resolution.
		Touchpad coordinates represent raw device coordinates in the
		X resolution of the touchpad. See `Normalization of relative motion`_
		for more details.

		Any rotation applied to the device also applies to unaccelerated motion
		(see :meth:`~libinput.define.Device.config_rotation_set_angle`).

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION`.
		Returns:
			float: The unaccelerated relative x movement since the last event.
		"""

		return self._libinput.libinput_event_pointer_get_dx_unaccelerated(
			self._handle)

	def get_dy_unaccelerated(self):
		"""Return the relative delta of the unaccelerated motion vector of the
		current event.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION`, this method returns 0.

		Relative unaccelerated motion deltas are raw device coordinates. Note
		that these coordinates are subject to the device's native resolution.
		Touchpad coordinates represent raw device coordinates in the
		X resolution of the touchpad. See `Normalization of relative motion`_
		for more details.

		Any rotation applied to the device also applies to unaccelerated motion
		(see :meth:`~libinput.define.Device.config_rotation_set_angle`).

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION`.
		Returns:
			float: The unaccelerated relative y movement since the last event.
		"""

		return self._libinput.libinput_event_pointer_get_dy_unaccelerated(
			self._handle)

	def get_absolute_x(self):
		"""Return the current absolute x coordinate of the pointer event,
		in mm from the top left corner of the device.

		To get the corresponding output screen coordinate, use
		:meth:`get_absolute_x_transformed`.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`, this method
		returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`.
		Returns:
			float: The current absolute x coordinate.
		"""

		return self._libinput.libinput_event_pointer_get_absolute_x(
			self._handle)

	def get_absolute_y(self):
		"""Return the current absolute y coordinate of the pointer event,
		in mm from the top left corner of the device.

		To get the corresponding output screen coordinate, use
		:meth:`get_absolute_y_transformed`.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`, this method
		returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`.
		Returns:
			float: The current absolute y coordinate.
		"""

		return self._libinput.libinput_event_pointer_get_absolute_y(
			self._handle)

	def get_absolute_x_transformed(self, width):
		"""Return the current absolute x coordinate of the pointer event,
		transformed to screen coordinates.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`, the return
		value of this method is undefined.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`.
		Args:
			width (int): The current output screen width.
		Returns:
			float: The current absolute x coordinate transformed to a screen
			coordinate.
		"""

		return self._libinput.libinput_event_pointer_get_absolute_x_transformed(
			self._handle, width)

	def get_absolute_y_transformed(self, height):
		"""Return the current absolute y coordinate of the pointer event,
		transformed to screen coordinates.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`, the return
		value of this method is undefined.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_MOTION_ABSOLUTE`.
		Args:
			height (int): The current output screen height.
		Returns:
			float: The current absolute y coordinate transformed to a screen
			coordinate.
		"""

		return self._libinput.libinput_event_pointer_get_absolute_y_transformed(
			self._handle, height)

	def get_button(self):
		"""Return the button that triggered this event.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_BUTTON`, this method returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_BUTTON`.
		Returns:
			~libinput.evcodes.Button: The button triggering this event.
		"""

		return self._libinput.libinput_event_pointer_get_button(self._handle)

	def get_button_state(self):
		"""Return the button state that triggered this event.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_BUTTON`, this method returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_BUTTON`.
		Returns:
			~libinput.constant.ButtonState: The button state triggering this
			event.
		"""

		return self._libinput.libinput_event_pointer_get_button_state(
			self._handle)

	def get_seat_button_count(self):
		"""Return the total number of buttons pressed on all devices on the
		associated seat after the event was triggered.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_BUTTON`. For other events,
			this function returns 0.
		Returns:
			int: The seat wide pressed button count for the key of this event.
		"""

		return self._libinput.libinput_event_pointer_get_seat_button_count(
			self._handle)

	def has_axis(self, axis):
		"""Check if the event has a valid value for the given axis.

		If this method returns True for an axis and :meth:`get_axis_value`
		returns a value of 0, the event is a scroll stop event.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_AXIS`, this method returns
		False.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_AXIS`.
		Args:
			axis (~libinput.constant.PointerAxis): The axis to check.
		Returns:
			bool: True if this event contains a value for this axis.
		"""

		return self._libinput.libinput_event_pointer_has_axis(
			self._handle, axis)

	def get_axis_value(self, axis):
		"""Return the axis value of the given axis.

		The interpretation of the value depends on the axis. For the two
		scrolling axes :attr:`~libinput.constant.PointerAxis.SCROLL_VERTICAL`
		and :attr:`~libinput.constant.PointerAxis.SCROLL_HORIZONTAL`, the value
		of the event is in relative scroll units, with the positive direction
		being down or right, respectively. For the interpretation of the value,
		see :meth:`get_axis_source`.

		If :meth:`has_axis` returns False for an axis, this method returns 0
		for that axis.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_AXIS`, this method returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_AXIS`.
		Args:
			axis (~libinput.constant.PointerAxis): The axis who's value to get.
		Returns:
			float: The axis value of this event.
		"""

		return self._libinput.libinput_event_pointer_get_axis_value(
			self._handle, axis)

	def get_axis_source(self):
		"""Return the source for a given axis event.

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
		returned here. For backwards compatibility, the value returned by this
		method is identical to a single mouse wheel rotation by this device
		(see the documentation for
		:attr:`~libinput.constant.PointerAxisSource.WHEEL` above). Callers
		should not use this value but instead exclusively refer to the value
		returned by :meth:`get_axis_value_discrete`.

		For pointer events that are not of type
		:attr:`~libinput.constant.Event.POINTER_AXIS`, this method returns
		:attr:`~libinput.constant.PointerAxisSource.NONE`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.POINTER_AXIS`.
		Returns:
			~libinput.constant.PointerAxisSource: The source for this axis
			event.
		"""

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
		"""

		return self._libinput.libinput_event_pointer_get_axis_value_discrete(
			self._handle, axis)


class KeyboardEvent(DeviceEvent):
	"""A keyboard event representing a key press/release.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)

		self._libinput.libinput_event_keyboard_get_time.argtypes = (c_void_p,)
		self._libinput.libinput_event_keyboard_get_time.restype = c_uint32
		self._libinput.libinput_event_keyboard_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_keyboard_get_time_usec.restype = c_uint64
		self._libinput.libinput_event_keyboard_get_key.argtypes = (c_void_p,)
		self._libinput.libinput_event_keyboard_get_key.restype = Key
		self._libinput.libinput_event_keyboard_get_key_state.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_keyboard_get_key_state.restype = KeyState
		self._libinput.libinput_event_keyboard_get_seat_key_count.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_keyboard_get_seat_key_count.restype = (
			c_uint32)

	def get_time(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event.
		"""

		return self._libinput.libinput_event_keyboard_get_time(self._handle)

	def get_time_usec(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_keyboard_get_time_usec(
			self._handle)

	def get_key(self):
		"""Returns the keycode that triggered this event.

		Returns:
			~libinput.evcodes.Key: The keycode that triggered this key event.
		"""

		return self._libinput.libinput_event_keyboard_get_key(self._handle)

	def get_key_state(self):
		"""Returns the logical state of the key.

		Returns:
			~libinput.constant.KeyState: The state change of the key.
		"""

		return self._libinput.libinput_event_keyboard_get_key_state(
			self._handle)

	def get_seat_key_count(self):
		"""Return the total number of keys pressed on all devices on the
		associated seat after the event was triggered.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.KEYBOARD_KEY`. For other events,
			this method returns 0.
		Returns:
			int: The seat wide pressed key count for the key of this event.
		"""

		return self._libinput.libinput_event_keyboard_get_seat_key_count(
			self._handle)


class TouchEvent(DeviceEvent):
	"""Touch event representing a touch down, move or up, as well as
	a touch cancel and touch frame events.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)

		self._libinput.libinput_event_touch_get_time.argtypes = (c_void_p,)
		self._libinput.libinput_event_touch_get_time.restype = c_uint32
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

	def get_time(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event.
		"""

		return self._libinput.libinput_event_touch_get_time(self._handle)

	def get_time_usec(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_touch_get_time_usec(self._handle)

	def get_slot(self):
		"""Get the slot of this touch event.

		See the kernel's multitouch protocol B documentation for more
		information.

		If the touch event has no assigned slot, for example if it is from
		a single touch device, this function returns -1.

		For events not of type :attr:`~libinput.constant.Event.TOUCH_DOWN`,
		:attr:`~libinput.constant.Event.TOUCH_UP`,
		:attr:`~libinput.constant.Event.TOUCH_MOTION` or
		:attr:`~libinput.constant.Event.TOUCH_CANCEL`, this method returns 0.

		Note:
			It is an application bug to call this method for events of type
			other than :attr:`~libinput.constant.Event.TOUCH_DOWN`,
			:attr:`~libinput.constant.Event.TOUCH_UP`,
			:attr:`~libinput.constant.Event.TOUCH_MOTION` or
			:attr:`~libinput.constant.Event.TOUCH_CANCEL`.
		Returns:
			int: The slot of this touch event.
		"""

		return self._libinput.libinput_event_touch_get_slot(self._handle)

	def get_seat_slot(self):
		"""Get the seat slot of the touch event.

		A seat slot is a non-negative seat wide unique identifier of an active
		touch point.

		Events from single touch devices will be represented as one individual
		touch point per device.

		For events not of type :attr:`~libinput.constant.Event.TOUCH_DOWN`,
		:attr:`~libinput.constant.Event.TOUCH_UP`,
		:attr:`~libinput.constant.Event.TOUCH_MOTION` or
		:attr:`~libinput.constant.Event.TOUCH_CANCEL`, this method returns 0.

		Note:
			It is an application bug to call this method for events of type
			other than :attr:`~libinput.constant.Event.TOUCH_DOWN`,
			:attr:`~libinput.constant.Event.TOUCH_UP`,
			:attr:`~libinput.constant.Event.TOUCH_MOTION` or
			:attr:`~libinput.constant.Event.TOUCH_CANCEL`.
		Returns:
			int: The seat slot of the touch event.
		"""

		return self._libinput.libinput_event_touch_get_seat_slot(self._handle)

	def get_x(self):
		"""Return the current absolute x coordinate of the touch event,
		in mm from the top left corner of the device.

		To get the corresponding output screen coordinate, use
		:meth:`get_x_transformed`.

		For events not of type :attr:`~libinput.constant.Event.TOUCH_DOWN`,
		:attr:`~libinput.constant.Event.TOUCH_MOTION`, this method returns 0.

		Note:
			It is an application bug to call this method for events of type
			other than :attr:`~libinput.constant.Event.TOUCH_DOWN`
			or :attr:`~libinput.constant.Event.TOUCH_MOTION`.
		Returns:
			float: The current absolute x coordinate.
		"""

		return self._libinput.libinput_event_touch_get_x(self._handle)

	def get_y(self):
		"""Return the current absolute y coordinate of the touch event,
		in mm from the top left corner of the device.

		To get the corresponding output screen coordinate, use
		:meth:`get_y_transformed`.

		For events not of type :attr:`~libinput.constant.Event.TOUCH_DOWN`,
		:attr:`~libinput.constant.Event.TOUCH_MOTION`, this method returns 0.

		Note:
			It is an application bug to call this method for events of type
			other than :attr:`~libinput.constant.Event.TOUCH_DOWN`
			or :attr:`~libinput.constant.Event.TOUCH_MOTION`.
		Returns:
			float: The current absolute y coordinate.
		"""

		return self._libinput.libinput_event_touch_get_y(self._handle)

	def get_x_transformed(self, width):
		"""Return the current absolute x coordinate of the touch event,
		transformed to screen coordinates.

		For events not of type :attr:`~libinput.constant.Event.TOUCH_DOWN`,
		:attr:`~libinput.constant.Event.TOUCH_MOTION`, this method returns 0.

		Note:
			It is an application bug to call this method for events of type
			other than :attr:`~libinput.constant.Event.TOUCH_DOWN`
			or :attr:`~libinput.constant.Event.TOUCH_MOTION`.
		Args:
			width (int): The current output screen width.
		Returns:
			float: The current absolute x coordinate transformed to
			a screen coordinate.
		"""

		return self._libinput.libinput_event_touch_get_x_transformed(
			self._handle, width)

	def get_y_transformed(self, height):
		"""Return the current absolute y coordinate of the touch event,
		transformed to screen coordinates.

		For events not of type :attr:`~libinput.constant.Event.TOUCH_DOWN`,
		:attr:`~libinput.constant.Event.TOUCH_MOTION`, this method returns 0.

		Note:
			It is an application bug to call this method for events of type
			other than :attr:`~libinput.constant.Event.TOUCH_DOWN`
			or :attr:`~libinput.constant.Event.TOUCH_MOTION`.
		Args:
			height (int): The current output screen height.
		Returns:
			float: The current absolute y coordinate transformed to
			a screen coordinate.
		"""

		return self._libinput.libinput_event_touch_get_y_transformed(
			self._handle, height)


class GestureEvent(DeviceEvent):
	"""A gesture event representing gesture on a touchpad.

	Gesture sequences always start with a
	:attr:`libinput.constant.Event.GESTURE_FOO_START` event. All following
	gesture events will be of the
	:attr:`libinput.constant.Event.GESTURE_FOO_UPDATE` type until
	a :attr:`libinput.constant.Event.GESTURE_FOO_END` is generated which
	signals the end of the gesture.

	See `Gestures`_ for more information on gesture handling.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)

		self._libinput.libinput_event_gesture_get_time.argtypes = (c_void_p,)
		self._libinput.libinput_event_gesture_get_time.restype = c_uint32
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

	def get_time(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event.
		"""

		return self._libinput.libinput_event_gesture_get_time(self._handle)

	def get_time_usec(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_gesture_get_time_usec(self._handle)

	def get_finger_count(self):
		"""Return the number of fingers used for a gesture.

		This can be used e.g. to differentiate between 3 or 4 finger swipes.
		This method can be called on all gesture events and the returned
		finger count value will not change during a sequence.

		Returns:
			int: The number of fingers used for a gesture.
		"""

		return self._libinput.libinput_event_gesture_get_finger_count(
			self._handle)

	def get_cancelled(self):
		"""Return if the gesture ended normally, or if it was cancelled.

		For gesture events that are not of type
		:attr:`~libinput.constant.Event.GESTURE_SWIPE_END` or
		:attr:`~libinput.constant.Event.GESTURE_PINCH_END`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.GESTURE_SWIPE_END` or
			:attr:`~libinput.constant.Event.GESTURE_PINCH_END`.
		Returns:
			bool: :obj:`True` indicating that the gesture was cancelled.
		"""

		return self._libinput.libinput_event_gesture_get_cancelled(self._handle)

	def get_dx(self):
		"""Return the delta between the last event and the current event.

		For gesture events that are not of type
		:attr:`~libinput.constant.Event.GESTURE_SWIPE_UPDATE` or
		:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE`, this method
		returns 0.

		If a device employs pointer acceleration, the delta returned by this
		method is the accelerated delta.


		Relative motion deltas are normalized to represent those of a device
		with 1000dpi resolution. See `Normalization of relative motion`_
		for more details.

		Returns:
			float: The relative x movement since the last event.
		"""

		return self._libinput.libinput_event_gesture_get_dx(self._handle)

	def get_dy(self):
		"""Return the delta between the last event and the current event.

		For gesture events that are not of type
		:attr:`~libinput.constant.Event.GESTURE_SWIPE_UPDATE` or
		:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE`, this method
		returns 0.

		If a device employs pointer acceleration, the delta returned by this
		method is the accelerated delta.

		Relative motion deltas are normalized to represent those of a device
		with 1000dpi resolution. See `Normalization of relative motion`_
		for more details.

		Returns:
			float: The relative y movement since the last event.
		"""

		return self._libinput.libinput_event_gesture_get_dy(self._handle)

	def get_dx_unaccelerated(self):
		"""Return the relative delta of the unaccelerated motion vector of
		the current event.

		For gesture events that are not of type
		:attr:`~libinput.constant.Event.GESTURE_SWIPE_UPDATE` or
		:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE`, this method
		returns 0.

		Relative unaccelerated motion deltas are normalized to represent those
		of a device with 1000dpi resolution. See
		`Normalization of relative motion`_ for more details.
		Note that unaccelerated events are not equivalent to 'raw' events
		as read from the device.

		Any rotation applied to the device also applies to gesture motion
		(see :meth:`~libinput.define.Device.config_rotation_set_angle`).

		Returns:
			float: The unaccelerated relative x movement since the last event.
		"""

		return self._libinput.libinput_event_gesture_get_dx_unaccelerated(
			self._handle)

	def get_dy_unaccelerated(self):
		"""Return the relative delta of the unaccelerated motion vector of
		the current event.

		For gesture events that are not of type
		:attr:`~libinput.constant.Event.GESTURE_SWIPE_UPDATE` or
		:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE`, this method
		returns 0.

		Relative unaccelerated motion deltas are normalized to represent those
		of a device with 1000dpi resolution. See
		`Normalization of relative motion`_ for more details.
		Note that unaccelerated events are not equivalent to 'raw' events
		as read from the device.

		Any rotation applied to the device also applies to gesture motion
		(see :meth:`~libinput.define.Device.config_rotation_set_angle`).

		Returns:
			float: The unaccelerated relative y movement since the last event.
		"""

		return self._libinput.libinput_event_gesture_get_dy_unaccelerated(
			self._handle)

	def get_scale(self):
		"""Return the absolute scale of a pinch gesture, the scale is
		the division of the current distance between the fingers and
		the distance at the start of the gesture.

		The scale begins at 1.0, and if e.g. the fingers moved together by
		50% then the scale will become 0.5, if they move twice as far apart
		as initially the scale becomes 2.0, etc.

		For gesture events that are of type
		:attr:`~libinput.constant.Event.GESTURE_PINCH_BEGIN`, this method
		returns 1.0.

		For gesture events that are of type
		:attr:`~libinput.constant.Event.GESTURE_PINCH_END`, this method
		returns the scale value of the most recent
		:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE` event (if any)
		or 1.0 otherwise.

		For all other events this method returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.GESTURE_PINCH_BEGIN`,
			:attr:`~libinput.constant.Event.GESTURE_PINCH_END` or
			:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE`.
		Returns:
			float: The absolute scale of a pinch gesture.
		"""

		return self._libinput.libinput_event_gesture_get_scale(self._handle)

	def get_angle_delta(self):
		"""Return the angle delta in degrees between the last and the current
		:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE` event.

		For gesture events that are not of type
		:attr:`~libinput.constant.Event.GESTURE_PINCH_UPDATE`, this method
		returns 0.

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
		"""

		return self._libinput.libinput_event_gesture_get_angle_delta(
			self._handle)


class TabletToolEvent(DeviceEvent):
	"""Tablet tool event representing an axis update, button press,
	or tool update.

	Valid event types for this event are
	:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
	:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
	:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`
	and :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)

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
		self._libinput.libinput_event_tablet_tool_get_button.restype = Button
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
		self._libinput.libinput_event_tablet_tool_get_time.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_time.restype = c_uint32
		self._libinput.libinput_event_tablet_tool_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_tool_get_time_usec.restype = (
			c_uint64)

	def x_has_changed(self):
		"""Check if the x axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_x_has_changed(
			self._handle)

	def y_has_changed(self):
		"""Check if the y axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_y_has_changed(
			self._handle)

	def pressure_has_changed(self):
		"""Check if the pressure axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_pressure_has_changed(
			self._handle)

	def distance_has_changed(self):
		"""Check if the distance axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`. For tablet tool events of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		always returns :obj:`True`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_distance_has_changed(
			self._handle)

	def tilt_x_has_changed(self):
		"""Check if the tilt x axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_tilt_x_has_changed(
			self._handle)

	def tilt_y_has_changed(self):
		"""Check if the tilt y axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_tilt_y_has_changed(
			self._handle)

	def rotation_has_changed(self):
		"""Check if the z-rotation axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_rotation_has_changed(
			self._handle)

	def slider_has_changed(self):
		"""Check if the slider axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_slider_has_changed(
			self._handle)

	def wheel_has_changed(self):
		"""Check if the wheel axis was updated in this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
		:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
		or :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`, this method
		returns :obj:`False`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_AXIS`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_TIP`,
			:attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`,
			or :attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			bool: :obj:`True` if the axis was updated or :obj:`False` otherwise.
		"""

		return self._libinput.libinput_event_tablet_tool_wheel_has_changed(
			self._handle)

	def get_x(self):
		"""Returns the X coordinate of the tablet tool, in mm from
		the top left corner of the tablet in its current logical orientation.

		Use :meth:`get_x_transformed` for transforming the axis value into
		a different coordinate space.

		Note:
			On some devices, returned value may be negative or larger than
			the width of the device. See `Out-of-bounds motion events`_
			for more details.
		Returns:
			float: The current value of the the axis.
		"""

		return self._libinput.libinput_event_tablet_tool_get_x(self._handle)

	def get_y(self):
		"""Returns the Y coordinate of the tablet tool, in mm from
		the top left corner of the tablet in its current logical orientation.

		Use :meth:`get_y_transformed` for transforming the axis value into
		a different coordinate space.

		Note:
			On some devices, returned value may be negative or larger than
			the width of the device. See `Out-of-bounds motion events`_
			for more details.
		Returns:
			float: The current value of the the axis.
		"""

		return self._libinput.libinput_event_tablet_tool_get_y(self._handle)

	def get_dx(self):
		"""Return the delta between the last event and the current event.

		If the tool employs pointer acceleration, the delta returned by this
		method is the accelerated delta.

		This value is in screen coordinate space, the delta is to be
		interpreted like the return value of :meth:`.PointerEvent.get_dx`.
		See `Relative motion for tablet tools`_ for more details.

		Returns:
			float: The relative x movement since the last event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_dx(self._handle)

	def get_dy(self):
		"""Return the delta between the last event and the current event.

		If the tool employs pointer acceleration, the delta returned by this
		method is the accelerated delta.

		This value is in screen coordinate space, the delta is to be
		interpreted like the return value of :meth:`.PointerEvent.get_dx`.
		See `Relative motion for tablet tools`_ for more details.

		Returns:
			float: The relative y movement since the last event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_dy(self._handle)

	def get_pressure(self):
		"""Returns the current pressure being applied on the tool in use,
		normalized to the range [0, 1].

		If this axis does not exist on the current tool, this method returns 0.

		Returns:
			float: The current value of the the axis.
		"""

		return self._libinput.libinput_event_tablet_tool_get_pressure(
			self._handle)

	def get_distance(self):
		"""Returns the current distance from the tablet's sensor,
		normalized to the range [0, 1].

		If this axis does not exist on the current tool, this method returns 0.

		Returns:
			float: The current value of the the axis.
		"""

		return self._libinput.libinput_event_tablet_tool_get_distance(
			self._handle)

	def get_tilt_x(self):
		"""Returns the current tilt along the X axis of the tablet's
		current logical orientation, in degrees off the tablet's z axis.

		That is, if the tool is perfectly orthogonal to the tablet,
		the tilt angle is 0. When the top tilts towards the logical top/left
		of the tablet, the x/y tilt angles are negative, if the top tilts
		towards the logical bottom/right of the tablet, the x/y tilt angles
		are positive.

		If this axis does not exist on the current tool, this method returns 0.

		Returns:
			float: The current value of the axis in degrees.
		"""

		return self._libinput.libinput_event_tablet_tool_get_tilt_x(
			self._handle)

	def get_tilt_y(self):
		"""Returns the current tilt along the Y axis of the tablet's
		current logical orientation, in degrees off the tablet's z axis.

		That is, if the tool is perfectly orthogonal to the tablet,
		the tilt angle is 0. When the top tilts towards the logical top/left
		of the tablet, the x/y tilt angles are negative, if the top tilts
		towards the logical bottom/right of the tablet, the x/y tilt angles
		are positive.

		If this axis does not exist on the current tool, this method returns 0.

		Returns:
			float: The current value of the the axis in degrees.
		"""

		return self._libinput.libinput_event_tablet_tool_get_tilt_y(
			self._handle)

	def get_rotation(self):
		"""Returns the current z rotation of the tool in degrees, clockwise
		from the tool's logical neutral position.

		For tools of type :attr:`~libinput.constant.TabletToolType.MOUSE`
		and :attr:`~libinput.constant.TabletToolType.LENS` the logical
		neutral position is pointing to the current logical north
		of the tablet. For tools of type
		:attr:`~libinput.constant.TabletToolType.BRUSH`, the logical
		neutral position is with the buttons pointing up.

		If this axis does not exist on the current tool, this method returns 0.

		Returns:
			float: The current value of the the axis.
		"""

		return self._libinput.libinput_event_tablet_tool_get_rotation(
			self._handle)

	def get_slider_position(self):
		"""Returns the current position of the slider on the tool,
		normalized to the range [-1, 1].

		The logical zero is the neutral position of the slider, or
		the logical center of the axis. This axis is available on e.g.
		the Wacom Airbrush.

		If this axis does not exist on the current tool, this method returns 0.

		Returns:
			float: The current value of the the axis.
		"""

		return self._libinput.libinput_event_tablet_tool_get_slider_position(
			self._handle)

	def get_wheel_delta(self):
		"""Return the delta for the wheel in degrees.

		Returns:
			float: The delta of the wheel, in degrees, compared to
			the last event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_wheel_delta(
			self._handle)

	def get_wheel_delta_discrete(self):
		"""Return the delta for the wheel in discrete steps (e.g. wheel clicks).

		Returns:
			int: The delta of the wheel, in discrete steps, compared to
			the last event.
		"""

		return self._libinput \
			.libinput_event_tablet_tool_get_wheel_delta_discrete(self._handle)

	def get_x_transformed(self, width):
		"""Return the current absolute x coordinate of the tablet tool event,
		transformed to screen coordinates.

		Note:
			This method may be called for a specific axis even if
			:meth:`*_has_changed` returns :obj:`False` for that axis. libinput
			always includes all device axes in the event.

			On some devices, returned value may be negative or larger than
			the width of the device. See `Out-of-bounds motion events`_
			for more details.
		Args:
			width (int): The current output screen width.
		Returns:
			float: The current absolute x coordinate transformed to
			a screen coordinate.
		"""

		return self._libinput.libinput_event_tablet_tool_get_x_transformed(
			self._handle, width)

	def get_y_transformed(self, height):
		"""Return the current absolute y coordinate of the tablet tool event,
		transformed to screen coordinates.

		Note:
			This method may be called for a specific axis even if
			:meth:`*_has_changed` returns :obj:`False` for that axis. libinput
			always includes all device axes in the event.

			On some devices, returned value may be negative or larger than
			the width of the device. See `Out-of-bounds motion events`_
			for more details.
		Args:
			height (int): The current output screen height.
		Returns:
			float: The current absolute y coordinate transformed to
			a screen coordinate.
		"""

		return self._libinput.libinput_event_tablet_tool_get_y_transformed(
			self._handle, height)

	def get_tool(self):
		"""Returns the tool that was in use during this event.

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

	def get_proximity_state(self):
		"""Returns the new proximity state of a tool from a proximity event.

		Used to check whether or not a tool came in or out of proximity during
		an event of type :attr:`~libinput.constant.Event.TABLET_TOOL_PROXIMITY`.

		See `Handling of proximity events`_ for
		recommendations on proximity handling.

		Returns:
			~libinput.constant.TabletToolProximityState: The new proximity
			state of the tool from the event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_proximity_state(
			self._handle)

	def get_tip_state(self):
		"""Returns the new tip state of a tool from a tip event.

		Used to check whether or not a tool came in contact with
		the tablet surface or left contact with the tablet surface during
		an event of type :attr:`~libinput.constant.Event.TABLET_TOOL_TIP`.

		Returns:
			~libinput.constant.TabletToolTipState: The new tip state of
			the tool from the event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_tip_state(
			self._handle)

	def get_button(self):
		"""Return the button that triggered this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`, this method
		returns :attr:`~libinput.evcodes.Button.BTN_NONE`.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			~libinput.evcodes.Button: The button triggering this event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_button(
			self._handle)

	def get_button_state(self):
		"""Return the button state of the event.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`.
		Returns:
			~libinput.constant.ButtonState: The button state triggering
			this event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_button_state(
			self._handle)

	def get_seat_button_count(self):
		"""Return the total number of buttons pressed on all devices on
		the associated seat after the the event was triggered.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_TOOL_BUTTON`. For other
			events, this method returns 0.
		Returns:
			int: The seat wide pressed button count for the key of this event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_seat_button_count(
			self._handle)

	def get_time(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event.
		"""

		return self._libinput.libinput_event_tablet_tool_get_time(self._handle)

	def get_time_usec(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_tablet_tool_get_time_usec(
			self._handle)


class TabletPadEvent(DeviceEvent):
	"""Tablet pad event representing a button press or ring/strip update
	on the tablet pad itself.

	Valid event types for this event are
	:attr:`~libinput.constant.Event.TABLET_PAD_BUTTON`,
	:attr:`~libinput.constant.Event.TABLET_PAD_RING`
	and :attr:`~libinput.constant.Event.TABLET_PAD_STRIP`.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)

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
		self._libinput.libinput_event_tablet_pad_get_time.argtypes = (c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_time.restype = c_uint32
		self._libinput.libinput_event_tablet_pad_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_tablet_pad_get_time_usec.restype = (
			c_uint64)

	def get_ring_position(self):
		"""Returns the current position of the ring, in degrees
		counterclockwise from the northern-most point of the ring in
		the tablet's current logical orientation.

		If the source is
		:attr:`~libinput.constant.TabletPadRingAxisSource.FINGER`,
		libinput sends a terminating event with a ring value of -1 when
		the finger is lifted from the ring. A caller may use this information
		to e.g. determine if kinetic scrolling should be triggered.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_RING`. For other events,
			this method returns 0.
		Returns:
			float: The current value of the the axis. -1 if the finger was
			lifted.
		"""

		return self._libinput.libinput_event_tablet_pad_get_ring_position(
			self._handle)

	def get_ring_number(self):
		"""Returns the number of the ring that has changed state,
		with 0 being the first ring.

		On tablets with only one ring, this method always returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_RING`. For other events,
			this method returns 0.
		Returns:
			int: The index of the ring that changed state.
		"""

		return self._libinput.libinput_event_tablet_pad_get_ring_number(
			self._handle)

	def get_ring_source(self):
		"""Returns the source of the interaction with the ring.

		If the source is
		:attr:`~libinput.constant.TabletPadRingAxisSource.FINGER`,
		libinput sends a ring position value of -1 to terminate
		the current interaction.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_RING`. For other events,
			this method raises :exc:`ValueError`.
		Returns:
			~libinput.constant.TabletPadRingAxisSource: The source of the ring
			interaction.
		Raises:
			ValueError
		"""

		return self._libinput.libinput_event_tablet_pad_get_ring_source(
			self._handle)

	def get_strip_position(self):
		"""Returns the current position of the strip, normalized to
		the range [0, 1], with 0 being the top/left-most point in the tablet's
		current logical orientation.

		If the source is
		:attr:`~libinput.constant.TabletPadStripAxisSource.FINGER`,
		libinput sends a terminating event with a value of -1 when the finger
		is lifted from the strip. A caller may use this information to e.g.
		determine if kinetic scrolling should be triggered.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_STRIP`. For other events,
			this method returns 0.
		Returns:
			float: The current value of the the axis. -1 if the finger was
			lifted.
		"""

		return self._libinput.libinput_event_tablet_pad_get_strip_position(
			self._handle)

	def get_strip_number(self):
		"""Returns the number of the strip that has changed state,
		with 0 being the first strip.

		On tablets with only one strip, this method always returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_STRIP`. For other events,
			this method returns 0.
		Returns:
			int: The index of the strip that changed state.
		"""

		return self._libinput.libinput_event_tablet_pad_get_strip_number(
			self._handle)

	def get_strip_source(self):
		"""Returns the source of the interaction with the strip.

		If the source is
		:attr:`~libinput.constant.TabletPadStripAxisSource.FINGER`, libinput
		sends a strip position value of -1 to terminate the current interaction.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_STRIP`. For other events,
			this method returns 0.
		Returns:
			~libinput.constant.TabletPadStripAxisSource: The source of
			the strip interaction.
		"""

		return self._libinput.libinput_event_tablet_pad_get_strip_source(
			self._handle)

	def get_button_number(self):
		"""Return the button number that triggered this event, starting at 0.

		For events that are not of type
		:attr:`~libinput.constant.Event.TABLET_PAD_BUTTON`,
		this method returns 0.

		Note that the number returned is a generic sequential button number
		and not a semantic button code as defined in ``linux/input.h``.
		See `Tablet pad button numbers`_ for more details.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_BUTTON`.
			For other events, this method returns 0.
		Returns:
			int: The button triggering this event.
		"""

		return self._libinput.libinput_event_tablet_pad_get_button_number(
			self._handle)

	def get_button_state(self):
		"""Return the button state of the event.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.TABLET_PAD_BUTTON`.
			For other events, this method returns
			:attr:`~libinput.constant.ButtonState.RELEASED`.
		Returns:
			~libinput.constant.ButtonState: The button state triggering
			this event.
		"""

		return self._libinput.libinput_event_tablet_pad_get_button_state(
			self._handle)

	def get_mode(self):
		"""Returns the mode the button, ring, or strip that triggered
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
		returned by :meth:`~libinput.define.TabletPadModeGroup.get_mode`.
		See :meth:`~libinput.define.TabletPadModeGroup.get_mode` for details.

		Returns:
			int: The 0-indexed mode of this button, ring or strip at the time
			of the event.
		"""

		return self._libinput.libinput_event_tablet_pad_get_mode(self._handle)

	def get_mode_group(self):
		"""Returns the mode group that the button, ring, or strip that
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

	def get_time(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event.
		"""

		return self._libinput.libinput_event_tablet_pad_get_time(self._handle)

	def get_time_usec(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_tablet_pad_get_time_usec(
			self._handle)


class SwitchEvent(DeviceEvent):
	"""A switch event representing a changed state in a switch.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)

		self._libinput.libinput_event_switch_get_switch.argtypes = (c_void_p,)
		self._libinput.libinput_event_switch_get_switch.restype = Switch
		self._libinput.libinput_event_switch_get_switch_state.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_switch_get_switch_state.restype = (
			SwitchState)
		self._libinput.libinput_event_switch_get_time.argtypes = (c_void_p,)
		self._libinput.libinput_event_switch_get_time.restype = c_uint32
		self._libinput.libinput_event_switch_get_time_usec.argtypes = (
			c_void_p,)
		self._libinput.libinput_event_switch_get_time_usec.restype = c_uint64

	def get_switch(self):
		"""Return the switch that triggered this event.

		For events that are not of type
		:attr:`~libinput.constant.Event.SWITCH_TOGGLE`, this method returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.SWITCH_TOGGLE`.
		Returns:
			~libinput.constant.Switch: The switch triggering this event.
		"""

		return self._libinput.libinput_event_switch_get_switch(self._handle)

	def get_switch_state(self):
		"""Return the switch state that triggered this event.

		For switch events that are not of type
		:attr:`~libinput.constant.Event.SWITCH_TOGGLE`, this method returns 0.

		Note:
			It is an application bug to call this method for events other than
			:attr:`~libinput.constant.Event.SWITCH_TOGGLE`.
		Returns:
			~libinput.constant.SwitchState: The switch state triggering this
			event.
		"""

		return self._libinput.libinput_event_switch_get_switch_state(
			self._handle)

	def get_time(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event.
		"""

		return self._libinput.libinput_event_switch_get_time(self._handle)

	def get_time_usec(self):
		"""Note:
			Timestamps may not always increase. See `Event timestamps`_ for
			details.
		Returns:
			int: The event time for this event in microseconds.
		"""

		return self._libinput.libinput_event_switch_get_time_usec(self._handle)


class DeviceNotifyEvent(DeviceEvent):
	"""An event notifying the caller of a device being added or removed.
	"""

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)
