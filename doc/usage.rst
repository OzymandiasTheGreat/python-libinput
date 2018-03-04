Usage
-----

Creating manual context
~~~~~~~~~~~~~~~~~~~~~~~

::

   >>>from libinput import LibInput, constant

   >>> li = LibInput(context_type=constant.ContextType.PATH)
   >>> device = li.path_add_device('/dev/input/event7')
   >>> li.path_remove_device(device)

Creating udev context
~~~~~~~~~~~~~~~~~~~~~

udev context adds/removes devices from a given seat as they're physically
added/removed. :meth:`LibInputUdev.assign_seat` should only be called once
per context.
::

   >>> li = LibInput(context_type=constant.ContextType.UDEV)
   >>> li.assign_seat('seat0')

Viewing device information
~~~~~~~~~~~~~~~~~~~~~~~~~~

::

   >>> device.name
   'SIGMACHIP Usb Mouse'
   >>> device.has_capability(constant.DeviceCapability.POINTER)
   True
   >>> device.pointer_has_button(0x110) # BTN_LEFT
   True

Getting/filtering events
~~~~~~~~~~~~~~~~~~~~~~~~

::

   >>> for event in li.get_event():
   >>>     if event.type == constant.EventType.POINTER_MOTION:
   >>>         print(event.delta)
   (15, 76)
   >>> ...
