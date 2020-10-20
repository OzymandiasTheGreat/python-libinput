-----------------

MAINTAINER WANTED
-----------------

This project started out as a small side project,
that I needed for other things I was working on.

However I've come to realize I have neither time, interest nor hardware
required to maintain python bindings for something as big as libinput.

So, if you use this project, know a little C and think you could take over,
make a couple pull requests fixing some of the outstanding bugs
and we'll arrange for you to take over.

-----------------

libinput
--------

This package provides a pure python wrapper for *libinput*, a library that
handles input devices for display servers and other applications that need to
directly deal with input devices.It provides device detection, device handling,
input device event processing and abstraction.

*libinput* does this by reading character files in ``/dev/input/``, so to use
this package you need to run your code as root or to belong to ``input`` group.

Documentation
~~~~~~~~~~~~~

https://python-libinput.readthedocs.io/

Development
~~~~~~~~~~~

https://github.com/OzymandiasTheGreat/python-libinput

Package
~~~~~~~

https://pypi.org/project/python-libinput/
