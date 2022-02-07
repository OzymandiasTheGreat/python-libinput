#!/usr/bin/env python3

try:
	from enum import Enum, Flag, auto
except ImportError:
	from aenum import Enum, Flag, auto


class LogPriority(Enum):

	DEBUG = 10
	INFO = 20
	ERROR = 30

	@classmethod
	def from_param(cls, self):

		return self.value


class ContextType(Enum):

	PATH = auto()
	UDEV = auto()


class EventType(Enum):

	# ~ NONE = 0

	DEVICE_ADDED = auto()
	DEVICE_REMOVED = auto()

	KEYBOARD_KEY = 300

	POINTER_MOTION = 400
	POINTER_MOTION_ABSOLUTE = auto()
	POINTER_BUTTON = auto()
	POINTER_AXIS = auto()
	POINTER_SCROLL_WHEEL = auto()
	POINTER_SCROLL_FINGER = auto()
	POINTER_SCROLL_CONTINUOUS = auto()

	TOUCH_DOWN = 500
	TOUCH_UP = auto()
	TOUCH_MOTION = auto()
	TOUCH_CANCEL = auto()
	TOUCH_FRAME = auto()

	TABLET_TOOL_AXIS = 600
	TABLET_TOOL_PROXIMITY = auto()
	TABLET_TOOL_TIP = auto()
	TABLET_TOOL_BUTTON = auto()

	TABLET_PAD_BUTTON = 700
	TABLET_PAD_RING = auto()
	TABLET_PAD_STRIP = auto()

	GESTURE_SWIPE_BEGIN = 800
	GESTURE_SWIPE_UPDATE = auto()
	GESTURE_SWIPE_END = auto()
	GESTURE_PINCH_BEGIN = auto()
	GESTURE_PINCH_UPDATE = auto()
	GESTURE_PINCH_END = auto()
	GESTURE_HOLD_BEGIN = auto()
	GESTURE_HOLD_END = auto()

	SWITCH_TOGGLE = 900

	@classmethod
	def from_param(cls, self):

		return self.value

	def is_device(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.DeviceNotifyEvent`.
		"""

		if self in {type(self).DEVICE_ADDED, type(self).DEVICE_REMOVED}:
			return True
		else:
			return False

	def is_keyboard(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.KeyboardEvent`.
		"""

		if self in {type(self).KEYBOARD_KEY}:
			return True
		else:
			return False

	def is_pointer(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.PointerEvent`.
		"""

		if self in {type(self).POINTER_MOTION, type(self).POINTER_BUTTON,
			type(self).POINTER_MOTION_ABSOLUTE, type(self).POINTER_AXIS,
			type(self).POINTER_SCROLL_WHEEL,type(self).POINTER_SCROLL_CONTINUOUS}:
			return True
		else:
			return False

	def is_touch(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.TouchEvent`.
		"""

		if self in {type(self).TOUCH_DOWN, type(self).TOUCH_UP,
			type(self).TOUCH_MOTION, type(self).TOUCH_CANCEL,
			type(self).TOUCH_FRAME}:
			return True
		else:
			return False

	def is_tablet_tool(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.TabletToolEvent`.
		"""

		if self in {type(self).TABLET_TOOL_AXIS, type(self).TABLET_TOOL_BUTTON,
			type(self).TABLET_TOOL_PROXIMITY, type(self).TABLET_TOOL_TIP}:
			return True
		else:
			return False

	def is_tablet_pad(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.TabletPadEvent`.
		"""

		if self in {type(self).TABLET_PAD_BUTTON, type(self).TABLET_PAD_RING,
			type(self).TABLET_PAD_STRIP}:
			return True
		else:
			return False

	def is_gesture(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.GestureEvent`.
		"""

		if self in {type(self).GESTURE_SWIPE_BEGIN, type(self).GESTURE_SWIPE_END,
			type(self).GESTURE_SWIPE_UPDATE, type(self).GESTURE_PINCH_BEGIN,
			type(self).GESTURE_PINCH_UPDATE, type(self).GESTURE_PINCH_END,
			type(self).GESTURE_HOLD_END,type(self).GESTURE_HOLD_BEGIN}:
			return True
		else:
			return False

	def is_switch(self):
		"""Macro to check if this event is
		a :class:`~libinput.event.SwitchEvent`.
		"""

		if self in {type(self).SWITCH_TOGGLE}:
			return True
		else:
			return False


class DeviceCapability(Enum):

	KEYBOARD = 0
	POINTER = 1
	TOUCH = 2
	TABLET_TOOL = 3
	TABLET_PAD = 4
	GESTURE = 5
	SWITCH = 6

	@classmethod
	def from_param(cls, self):

		return self.value


class KeyState(Enum):

	RELEASED = 0
	PRESSED = 1

	@classmethod
	def from_param(cls, self):

		return self.value


class Led(Flag):

	NUM_LOCK = (1 << 0)
	CAPS_LOCK = (1 << 1)
	SCROLL_LOCK = (1 << 2)

	@classmethod
	def from_param(cls, self):

		return self.value


class ButtonState(Enum):

	RELEASED = 0
	PRESSED = 1

	@classmethod
	def from_param(cls, self):

		return self.value


class PointerAxis(Enum):

	SCROLL_VERTICAL = 0
	SCROLL_HORIZONTAL = 1

	@classmethod
	def from_param(cls, self):

		return self.value


class PointerAxisSource(Enum):

	NONE = 0
	WHEEL = 1
	FINGER = auto()
	CONTINUOUS = auto()
	WHEEL_TILT = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class TabletPadRingAxisSource(Enum):

	UNKNOWN = 1
	FINGER = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class TabletPadStripAxisSource(Enum):

	UNKNOWN = 1
	FINGER = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class TabletToolType(Enum):

	PEN = 1
	ERASER = auto()
	BRUSH = auto()
	PENCIL = auto()
	AIRBRUSH = auto()
	MOUSE = auto()
	LENS = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class TabletToolProximityState(Enum):

	OUT = 0
	IN = 1

	@classmethod
	def from_param(cls, self):

		return self.value


class TabletToolTipState(Enum):

	UP = 0
	DOWN = 1

	@classmethod
	def from_param(cls, self):

		return self.value


class SwitchState(Enum):

	OFF = 0
	ON = 1

	@classmethod
	def from_param(cls, self):

		return self.value


class Switch(Enum):

	LID = 1

	@classmethod
	def from_param(cls, self):

		return self.value


# Device configuration enums

class ConfigStatus(Enum):

	SUCCESS = 0
	UNSUPPORTED = auto()
	INVALID = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class TapState(Enum):

	DISABLED = 0
	ENABLED = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class TapButtonMap(Enum):

	LRM = 0
	LMR = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class DragState(Enum):

	DISABLED = 0
	ENABLED = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class DragLockState(Enum):

	DISABLED = 0
	ENABLED = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class SendEventsMode(Flag):

	ENABLED = 0
	DISABLED = (1 << 0)
	DISABLED_ON_EXTERNAL_MOUSE = (1 << 1)

	@classmethod
	def from_param(cls, self):

		return self.value


class AccelProfile(Flag):

	NONE = 0
	FLAT = (1 << 0)
	ADAPTIVE = (1 << 1)

	@classmethod
	def from_param(cls, self):

		return self.value


class ClickMethod(Flag):

	NONE = 0
	BUTTON_AREAS = (1 << 0)
	CLICKFINGER = (1 << 1)

	@classmethod
	def from_param(cls, self):

		return self.value


class MiddleEmulationState(Enum):

	DISABLED = 0
	ENABLED = auto()

	@classmethod
	def from_param(cls, self):

		return self.value


class ScrollMethod(Flag):

	NO_SCROLL = 0
	SCROLL_2FG = (1 << 0)
	EDGE = (1 << 1)
	ON_BUTTON_DOWN = (1 << 2)

	@classmethod
	def from_param(cls, self):

		return self.value


class DwtState(Enum):

	DISABLED = 0
	ENABLED = auto()

	@classmethod
	def from_param(cls, self):

		return self.value
