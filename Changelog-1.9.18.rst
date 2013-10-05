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

Authors:

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
