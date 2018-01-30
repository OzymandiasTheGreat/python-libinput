#!/usr/bin/env python3

from ctypes import c_void_p, c_uint32, c_uint64, c_double, c_bool, c_int32
from ctypes import c_int
from .constant import Event as enumEvent, ButtonState, PointerAxis, KeyState
from .constant import PointerAxisSource, Switch, SwitchState
from .define import Device, TabletTool
from .event_codes import Key, Button


class BaseEvent(object):

	def __init__(self, hevent, libinput):

		self._handle = hevent
		self._libinput = libinput

	def __eq__(self, other):

		if issubclass(type(other), BaseEvent):
			return self._handle == other._handle
		else:
			return NotImplemented


class Event(BaseEvent):

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

		hdevice = self._libinput.libinput_event_get_device(self._handle)
		return Device(hdevice, self._libinput)

	def get_pointer_event(self):

		pevent = self._libinput.libinput_event_get_pointer_event(self._handle)
		return PointerEvent(pevent, self, self._libinput)

	def get_keyboard_event(self):

		kevent = self._libinput.libinput_event_get_keyboard_event(self._handle)
		return KeyboardEvent(kevent, self, self._libinput)

	def get_touch_event(self):

		tevent = self._libinput.libinput_event_get_touch_event(self._handle)
		return TouchEvent(tevent, self, self._libinput)

	def get_gesture_event(self):

		gevent = self._libinput.libinput_event_get_gesture_event(self._handle)
		return GestureEvent(gevent, self, self._libinput)

	def get_tablet_tool_event(self):

		ttevent = self._libinput.libinput_event_get_tablet_tool_event(
			self._handle)
		return TabletToolEvent(ttevent, self, self._libinput)

	def get_tablet_pad_event(self):

		tpevent = self._libinput.libinput_event_get_tablet_pad_event(
			self._handle)
		return TabletPadEvent(tpevent, self, self._libinput)

	def get_switch_event(self):

		sevent = self._libinput.libinput_event_get_switch_event(self._handle)
		return SwitchEvent(sevent, self, self._libinput)

	def get_device_notify_event(self):

		dnevent = self._libinput.libinput_event_get_device_notify_event(
			self._handle)
		return DeviceNotifyEvent(dnevent, self, self._libinput)


class DeviceEvent(BaseEvent):

	def __init__(self, devent, base_event, libinput):

		BaseEvent.__init__(self, devent, libinput)
		self.base_event = base_event
		self.type = base_event.type


class PointerEvent(DeviceEvent):

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

		return self._libinput.libinput_event_pointer_get_time(self._handle)

	def get_time_usec(self):

		return self._libinput.libinput_event_pointer_get_time_usec(self._handle)

	def get_dx(self):

		return self._libinput.libinput_event_pointer_get_dx(self._handle)

	def get_dy(self):

		return self._libinput.libinput_event_pointer_get_dy(self._handle)

	def get_dx_unaccelerated(self):

		return self._libinput.libinput_event_pointer_get_dx_unaccelerated(
			self._handle)

	def get_dy_unaccelerated(self):

		return self._libinput.libinput_event_pointer_get_dy_unaccelerated(
			self._handle)

	def get_absolute_x(self):

		return self._libinput.libinput_event_pointer_get_absolute_x(
			self._handle)

	def get_absolute_y(self):

		return self._libinput.libinput_event_pointer_get_absolute_y(
			self._handle)

	def get_absolute_x_transformed(self, width):

		return self._libinput.libinput_event_pointer_get_absolute_x_transformed(
			self._handle, width)

	def get_absolute_y_transformed(self, height):

		return self._libinput.libinput_event_pointer_get_absolute_y_transformed(
			self._handle, height)

	def get_button(self):

		return self._libinput.libinput_event_pointer_get_button(self._handle)

	def get_button_state(self):

		return self._libinput.libinput_event_pointer_get_button_state(
			self._handle)

	def get_seat_button_count(self):

		return self._libinput.libinput_event_pointer_get_seat_button_count(
			self._handle)

	def has_axis(self, axis):

		return self._libinput.libinput_event_pointer_has_axis(
			self._handle, axis)

	def get_axis_value(self, axis):

		return self._libinput.libinput_event_pointer_get_axis_value(
			self._handle, axis)

	def get_axis_source(self):

		return self._libinput.libinput_event_pointer_get_axis_source(
			self._handle)

	def get_axis_value_discrete(self, axis):

		return self._libinput.libinput_event_pointer_get_axis_value_discrete(
			self._handle, axis)


class KeyboardEvent(DeviceEvent):

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

		return self._libinput.libinput_event_keyboard_get_time(self._handle)

	def get_time_usec(self):

		return self._libinput.libinput_event_keyboard_get_time_usec(
			self._handle)

	def get_key(self):

		return self._libinput.libinput_event_keyboard_get_key(self._handle)

	def get_key_state(self):

		return self._libinput.libinput_event_keyboard_get_key_state(
			self._handle)

	def get_seat_key_count(self):

		return self._libinput.libinput_event_keyboard_get_seat_key_count(
			self._handle)


class TouchEvent(DeviceEvent):

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

		return self._libinput.libinput_event_touch_get_time(self._handle)

	def get_time_usec(self):

		return self._libinput.libinput_event_touch_get_time_usec(self._handle)

	def get_slot(self):

		return self._libinput.libinput_event_touch_get_slot(self._handle)

	def get_seat_slot(self):

		return self._libinput.libinput_event_touch_get_seat_slot(self._handle)

	def get_x(self):

		return self._libinput.libinput_event_touch_get_x(self._handle)

	def get_y(self):

		return self._libinput.libinput_event_touch_get_y(self._handle)

	def get_x_transformed(self, width):

		return self._libinput.libinput_event_touch_get_x_transformed(
			self._handle, width)

	def get_y_transformed(self, height):

		return self._libinput.libinput_event_touch_get_y_transformed(
			self._handle, height)


class GestureEvent(DeviceEvent):

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

		return self._libinput.libinput_event_gesture_get_time(self._handle)

	def get_time_usec(self):

		return self._libinput.libinput_event_gesture_get_time_usec(self._handle)

	def get_finger_count(self):

		return self._libinput.libinput_event_gesture_get_finger_count(
			self._handle)

	def get_cancelled(self):

		return self._libinput.libinput_event_gesture_get_cancelled(self._handle)

	def get_dx(self):

		return self._libinput.libinput_event_gesture_get_dx(self._handle)

	def get_dy(self):

		return self._libinput.libinput_event_gesture_get_dy(self._handle)

	def get_dx_unaccelerated(self):

		return self._libinput.libinput_event_gesture_get_dx_unaccelerated(
			self._handle)

	def get_dy_unaccelerated(self):

		return self._libinput.libinput_event_gesture_get_dy_unaccelerated(
			self._handle)

	def get_scale(self):

		return self._libinput.libinput_event_gesture_get_scale(self._handle)

	def get_angle_delta(self):

		return self._libinput.libinput_event_gesture_get_angle_delta(
			self._handle)


class TabletToolEvent(DeviceEvent):

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

		return self._libinput.libinput_event_tablet_tool_x_has_changed(
			self._handle)

	def y_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_y_has_changed(
			self._handle)

	def pressure_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_pressure_has_changed(
			self._handle)

	def distance_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_distance_has_changed(
			self._handle)

	def tilt_x_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_tilt_x_has_changed(
			self._handle)

	def tilt_y_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_tilt_y_has_changed(
			self._handle)

	def rotation_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_rotation_has_changed(
			self._handle)

	def slider_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_slider_has_changed(
			self._handle)

	def wheel_has_changed(self):

		return self._libinput.libinput_event_tablet_tool_wheel_has_changed(
			self._handle)

	def get_x(self):

		return self._libinput.libinput_event_tablet_tool_get_x(self._handle)

	def get_y(self):

		return self._libinput.libinput_event_tablet_tool_get_y(self._handle)

	def get_dx(self):

		return self._libinput.libinput_event_tablet_tool_get_dx(self._handle)

	def get_dy(self):

		return self._libinput.libinput_event_tablet_tool_get_dy(self._handle)

	def get_pressure(self):

		return self._libinput.libinput_event_tablet_tool_get_pressure(
			self._handle)

	def get_distance(self):

		return self._libinput.libinput_event_tablet_tool_get_distance(
			self._handle)

	def get_tilt_x(self):

		return self._libinput.libinput_event_tablet_tool_get_tilt_x(
			self._handle)

	def get_tilt_y(self):

		return self._libinput.libinput_event_tablet_tool_get_tilt_y(
			self._handle)

	def get_rotation(self):

		return self._libinput.libinput_event_tablet_tool_get_rotation(
			self._handle)

	def get_slider_position(self):

		return self._libinput.libinput_event_tablet_tool_get_slider_position(
			self._handle)

	def get_wheel_delta(self):

		return self._libinput.libinput_event_tablet_tool_get_wheel_delta(
			self._handle)

	def get_wheel_delta_discrete(self):

		return self._libinput \
			.libinput_event_tablet_tool_get_wheel_delta_discrete(self._handle)

	def get_x_transformed(self, width):

		return self._libinput.libinput_event_tablet_tool_get_x_transformed(
			self._handle, width)

	def get_y_transformed(self, height):

		return self._libinput.libinput_event_tablet_tool_get_y_transformed(
			self._handle, height)

	def get_tool(self):

		htablettool = self._libinput.libinput_event_tablet_tool_get_tool(
			self._handle)
		return TabletTool(htablettool, self._libinput)

	def get_proximity_state(self):

		return self._libinput.libinput_event_tablet_tool_get_proximity_state(
			self._handle)

	def get_tip_state(self):

		return self._libinput.libinput_event_tablet_tool_get_tip_state(
			self._handle)

	def get_button(self):

		return self._libinput.libinput_event_tablet_tool_get_button(
			self._handle)

	def get_button_state(self):

		return self._libinput.libinput_event_tablet_tool_get_button_state(
			self._handle)

	def get_seat_button_count(self):

		return self._libinput.libinput_event_tablet_tool_get_seat_button_count(
			self._handle)

	def get_time(self):

		return self._libinput.libinput_event_tablet_tool_get_time(self._handle)

	def get_time_usec(self):

		return self._libinput.libinput_event_tablet_tool_get_time_usec(
			self._handle)


class TabletPadEvent(DeviceEvent):

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

		return self._libinput.libinput_event_tablet_pad_get_ring_position(
			self._handle)

	def get_ring_number(self):

		return self._libinput.libinput_event_tablet_pad_get_ring_number(
			self._handle)

	def get_ring_source(self):

		return self._libinput.libinput_event_tablet_pad_get_ring_source(
			self._handle)

	def get_strip_position(self):

		return self._libinput.libinput_event_tablet_pad_get_strip_position(
			self._handle)

	def get_strip_number(self):

		return self._libinput.libinput_event_tablet_pad_get_strip_number(
			self._handle)

	def get_strip_source(self):

		return self._libinput.libinput_event_tablet_pad_get_strip_source(
			self._handle)

	def get_button_number(self):

		return self._libinput.libinput_event_tablet_pad_get_button_number(
			self._handle)

	def get_button_state(self):

		return self._libinput.libinput_event_tablet_pad_get_button_state(
			self._handle)

	def get_mode(self):

		return self._libinput.libinput_event_tablet_pad_get_mode(self._handle)

	def get_mode_group(self):

		hmodegroup = self._libinput.libinput_event_tablet_pad_get_mode_group(
			self._handle)
		return TabletPadModeGroup(hmodegroup, self._libinput)

	def get_time(self):

		return self._libinput.libinput_event_tablet_pad_get_time(self._handle)

	def get_time_usec(self):

		return self._libinput.libinput_event_tablet_pad_get_time_usec(
			self._handle)


class SwitchEvent(DeviceEvent):

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

		return self._libinput.libinput_event_switch_get_switch(self._handle)

	def get_switch_state(self):

		return self._libinput.libinput_event_switch_get_switch_state(
			self._handle)

	def get_time(self):

		return self._libinput.libinput_event_switch_get_time(self._handle)

	def get_time_usec(self):

		return self._libinput.libinput_event_switch_get_time_usec(self._handle)


class DeviceNotifyEvent(DeviceEvent):

	def __init__(self, *args):

		DeviceEvent.__init__(self, *args)
