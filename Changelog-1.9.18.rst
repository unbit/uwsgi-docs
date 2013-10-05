uWSGI 1.9.18
============

WORK IN PROGRESS THINGS MAY CHANGE BEFORE OFFICIAL RELEASE

Bugfixes
********

- fixed uwsgi native protocol support on big endian machines
- fixed jvm build system for arm (Jorge Gallegos)
- fixed a memleak spotted by cppcheck in zlib management
- chdir() at every emperor glob iteration
- correctly honour --force-cwd
- fixed ia64/Linux compilation (Jonas Smedegaard/Riccardo Magliocchetti)
- fixed ruby rvm paths parsing order
- added waitpid() after daemon's SIGTERM (Łukasz Mierzwa)
- fixed pid numbering after --idle (Łukasz Mierzwa)
- fixed/improved cheaper memory limits (Łukasz Mierzwa)
- correctly close inherited sockets in gateways
- fix checks for MAP_FAILED in mmap() (instead of NULL)

New Features
************



The "raw" mode (preview technology, only for CPython)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While working on a new server-side project in Unbit we had the need to expose our web application using a very specific protocol (none of the ones supported by uWSGI).

Our first way was adding the new protocol as a plugin, but soon we realize that is was too-specific. So we decided to introduce the RAW mode.

Raw mode allows you to directly parse the request in your application callable. Instead of getting a list of CGI vars/headers in your callable
you only get the file descriptor soon after accept().

You can then read()/write() to that file descriptor in full freedom.

.. code-block:: python

   import os
   def application(fd):
      os.write(fd, "Hello World")
      
.. code-block:: sh

   uwsgi --raw-socket :7070 --python-raw yourapp.py

Raw mode disables request logging. We currently support it only for CPython, if we get reports (or interest) about it for the other languages we will add
support for sure.

IMPORTANT: raw mode is not a standard, so do not expect any middleware or common usage patterns will apply. Use it as a low-level socket wrapper. 



Optional NON-standard support for CPython buffer protocol for WSGI responses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Authors: yihuang with help of INADA Naoki (methane)

The WSGI (PEP333/3333) is pretty clear about the type of valid objects for responses: str for python2, bytes for python3

uWSGI (heavily using mod_wsgi as a reference) always enforce such behaviour, so "exotic" patterns like returning bytearray
where not supported. Such uses are somewhat involuntary supported on pure-python application servers, just because they simply call write() over them or because they cast them to string
before returning (very inefficient)

The patch proposed by yihuang suggests the use of the low-level buffer protocol exposed by the CPython C api. Strings (in python2) and bytes (in python3) support the buffer protocol, so its use is transparent
and backward compatibility is granted too. (for the CPython C api experts: yes we support both old and new buffer protocol)

This is a NON-standard behaviour you have to voluntary enable with --wsgi-accept-buffer.

Use with care as it could mask errors and/or wrong behaviours.

Note: if you tried 1.9.18-dev you may note this option was enabled by default. It was an error. Thanks to Graham Dumpleton (mod_wsgi author) for pointing it out.

Emperor improvements
^^^^^^^^^^^^^^^^^^^^

Build system improvements
^^^^^^^^^^^^^^^^^^^^^^^^^

Pluginized the 'schemes' management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

mountpoints checks
^^^^^^^^^^^^^^^^^^

Preliminary libffi plugin
^^^^^^^^^^^^^^^^^^^^^^^^^

Official support for kFreeBSD
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
