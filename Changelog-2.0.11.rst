uWSGI 2.0.11
============

[20150701]

Bugfixes
********

- [pypy] fixed misuse of ffi.string
- fixed detection for gcc 5 (jimfunk)
- fixed shared sockets for gateways
- [psgi] Changed abs to labs because offset is declared as a long (Peter H. Ezetta)
- add null terminator to uwsgi_get_dot_h() and uwsgi_config_py() (Jay Oster)
- fixed thread waiting during stop/restart (Kaiwen Xu)
- fixed chain reloading verbosity
- [python] fixed spooler job reference counting (Curtis Maloney)
- various static analysis improvements (Riccardo Magliocchetti)
- fixed sharedarea support for very big ranges
- fixed gzip transformation for zero-sized responses (Curtis Maloney)
- fixed management of https client certificate authentication (Vladimir Didenko)
- fixed OpenBSD build
- fixed TMPFILE permissions


New Features
************

The mem_collector thread
^^^^^^^^^^^^^^^^^^^^^^^^

fixpathinfo routing action
^^^^^^^^^^^^^^^^^^^^^^^^^^

sor and micros routing vars
^^^^^^^^^^^^^^^^^^^^^^^^^^^

wait-for-socket
^^^^^^^^^^^^^^^

wait_for hooks
^^^^^^^^^^^^^^

Availability
************
