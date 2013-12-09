uWSGI 1.9.21
============

Latest 1.9 before 2.0 (scheduled at December 30th 2013)

From now on, all of the releases will be -rc's (no new features will be added)

A document describing notes for upgrades from the (extremely obsolete) 1.2 and 1.4 versions is on work.

Bugfixes
********

- croak if the psgi streamer fails
- allows building coroae on raspberrypi
- do not wait for write availability until strictly required
- avoid segfault when async mode api is called without async mode
- fixed plain (without suspend engine) async mode
- do not spit errors on non x86 timerfd_create
- support timerfd_create/timerfd_settime on __arm__

Optimizations
*************

writev() for the first chunk
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

use a single buffer for websockets outgoing packets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New features
************

removed zeromq api
^^^^^^^^^^^^^^^^^^

The new sharedarea
^^^^^^^^^^^^^^^^^^

report request data in writers and readers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tmsecs and tmicros, werr, rerr, ioerr
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

mountpoints and mules support for symcall
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

read2 and wait_milliseconds async hooks
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

websockets binary messages
^^^^^^^^^^^^^^^^^^^^^^^^^^

the 'S' master fifo command
^^^^^^^^^^^^^^^^^^^^^^^^^^^

as-mule hook
^^^^^^^^^^^^

accepting hook and improved chain reloading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

error pages
^^^^^^^^^^^

Simplified plugins builder
^^^^^^^^^^^^^^^^^^^^^^^^^^
