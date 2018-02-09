Introduction
------------

This package is a pure python wrapper around *libinput* using ctypes.
It provides high-level object oriented api, taking care of reference counting,
memory management and the like automatically.

*libinput* is a library that handles input devices for display servers and
other applications that need to directly deal with input devices.
It provides device detection, device handling, input device event processing
and abstraction so minimize the amount of custom input code the user of
libinput need to provide the common set of functionality that users expect.
Input event processing includes scaling touch coordinates, generating pointer
events from touchpads, pointer acceleration, etc.

*libinput* does this by reading character files in ``/dev/input/``, so to use
this package you need to run your code as root or to belong to ``input`` group.


.. toctree::
   :maxdepth: 2

   install
   usage

.. toctree::
   :caption: API
   :maxdepth: 2

   libinput
   events
   devices
   constants
   evcodes
