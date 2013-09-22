uWSGI 1.9.17
============

Changelog [20130917]


Bugfixes
********

- the 'pty' client is now blocking (safer approach)
- removed strtok() usage (substituted by a new uwsgi api function on top of strtok_r() )
- fixed --pty-exec (Credits: C Anthony Risinger)



New features
************

The Master FIFO
^^^^^^^^^^^^^^^

The asap hook
^^^^^^^^^^^^^

Credits: Matthijs Kooijman

The TCC (libtcc) plugin
^^^^^^^^^^^^^^^^^^^^^^^

The forkptyrouter gateway
^^^^^^^^^^^^^^^^^^^^^^^^^

added a new magic var for ANSI escaping
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

--vassals-include
^^^^^^^^^^^^^^^^^

The Emperor heartbeat system is now mercyless...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

logpipe
^^^^^^^

Author: INADA Naoki

added "fd" logger to "logfile" plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Availability
************
