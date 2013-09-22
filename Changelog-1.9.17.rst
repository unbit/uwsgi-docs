uWSGI 1.9.17
============

Changelog [20130917]


Bugfixes
********

- the 'pty' client is now blocking (safer approach)
- removed strtok() usage (substituted by a new uwsgi api function on top of strtok_r() )



New features
************

The Master FIFO
^^^^^^^^^^^^^^^

The TCC (libtcc) plugin
^^^^^^^^^^^^^^^^^^^^^^^

The forkptyrouter gateway
^^^^^^^^^^^^^^^^^^^^^^^^^

added a new magic var for ANSI escaping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

logpipe
^^^^^^^

Author: INADA Naoki

added "fd" logger to "logfile" plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Availability
************
