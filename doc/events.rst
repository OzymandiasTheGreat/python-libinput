Events
------

.. Note::
   Device events and their generic versions compare equal if they refer to the
   same physical event.
   ::

      >>> Event() == PointerEvent()
      True

.. _Event timestamps: https://wayland.freedesktop.org/libinput/doc/latest/timestamps.html
.. _Normalization of relative motion: https://wayland.freedesktop.org/libinput/doc/1.8.2/motion_normalization.html
.. _Gestures: https://wayland.freedesktop.org/libinput/doc/latest/gestures.html
.. _Out-of-bounds motion events: https://wayland.freedesktop.org/libinput/doc/latest/tablet-support.html#tablet-bounds
.. _Relative motion for tablet tools: https://wayland.freedesktop.org/libinput/doc/latest/tablet-support.html#tablet-relative-motion
.. _Tracking unique tools: https://wayland.freedesktop.org/libinput/doc/latest/tablet-support.html#tablet-serial-numbers
.. _Handling of proximity events: https://wayland.freedesktop.org/libinput/doc/latest/tablet-support.html#tablet-fake-proximity
.. _Tablet pad button numbers: https://wayland.freedesktop.org/libinput/doc/latest/tablet-support.html#tablet-pad-buttons
.. _Tablet pad modes: https://wayland.freedesktop.org/libinput/doc/latest/tablet-support.html#tablet-pad-modes

.. module:: libinput.event

BaseEvent
~~~~~~~~~

.. autoclass:: BaseEvent
   :members:

Event
~~~~~

.. autoclass:: Event
   :members:

DeviceEvent
~~~~~~~~~~~

.. autoclass:: DeviceEvent
   :members:

PointerEvent
~~~~~~~~~~~~

.. autoclass:: PointerEvent
   :members:

KeyboardEvent
~~~~~~~~~~~~~

.. autoclass:: KeyboardEvent
   :members:

TouchEvent
~~~~~~~~~~

.. autoclass:: TouchEvent
   :members:

GestureEvent
~~~~~~~~~~~~

.. autoclass:: GestureEvent
   :members:

TabletToolEvent
~~~~~~~~~~~~~~~

.. autoclass:: TabletToolEvent
   :members:

TabletPadEvent
~~~~~~~~~~~~~~

.. autoclass:: TabletPadEvent
   :members:

SwitchEvent
~~~~~~~~~~~

.. autoclass:: SwitchEvent
   :members:

DeviceNotifyEvent
~~~~~~~~~~~~~~~~~

.. autoclass:: DeviceNotifyEvent
   :members:
