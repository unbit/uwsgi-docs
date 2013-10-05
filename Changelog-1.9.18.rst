uWSGI 1.9.18
============

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

Use of the CPython buffer protocol for WSGI responses
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Authors: yihuang with help of INADA Naoki (methane)

The WSGI (PEP333/3333) is pretty clear about the type of valid objects for responses: str for python2, bytes for python3

uWSGI (heavily using mod_wsgi as a reference) always enforced such behaviour, so "exotic" patterns like returning bytearray
where not supported. Such uses are somewhat involuntary supported on pure-python application servers, just because they simply call write() over them or because they cast them to string
before returning (very inefficient)

The patch proposed by yihuang suggests the use of the low-level buffer protocol exposed by the CPython C api. Strings (in python2) and bytes (in python3) support the buffer protocol, so its use is transparent
and backward compatibility is granted too. (for the CPython C api experts: yes we support both old and new protocol)

The result is that now you can return every object supporting the buffer protocol (like bytearray, array.array...) without making any conversion.

This is a violation of PEP, so if you feel a sinner just add the new option --wsgi-strict that will force the old mod_wsgi like behaviour.

The "raw" mode (preview technology, only for CPython)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
