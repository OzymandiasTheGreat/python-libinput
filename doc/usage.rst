Usage
-----

Creating manual context
~~~~~~~~~~~~~~~~~~~~~~~

::

   >>>from libinput import LibInput

   >>> li = LibInput()
   >>> device = li.path_add_device('/dev/input/event7')
   >>> li.path_remove_device(device)

Creating udev context
~~~~~~~~~~~~~~~~~~~~~

udev context adds/removes devices from a given seat as they're physically
added/removed. :meth:`LibInput.udev_assign_seat` should only be called once
per context.
::

   >>> li = LibInput(udev=True)
   >>> li.udev_assign_seat('seat0')

Viewing device information
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   >>> device.get_name()
   'SIGMACHIP Usb Mouse'
   >>> from libinput.constant import DeviceCapability
   >>> device.has_capability(DeviceCapability.POINTER)
   True
   >>> from libinput.evcodes import Button
   >>> device.pointer_has_button(Button.BTN_LEFT)
   True

Getting/filtering events
~~~~~~~~~~~~~~~~~~~~~~~~

::

   >>> from libinput.constant import Event
   >>> for event in li.get_event():
   >>>     if event.type.is_pointer():
   >>>         pointer_event = event.get_pointer_event()
   >>>         if pointer_event.type == Event.POINTER_MOTION:
   >>>             delta_x = pointer_event.get_dx()
   >>>             delta_y = pointer_event.get_dy()
   >>>             ...
