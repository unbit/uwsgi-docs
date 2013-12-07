uWSGI 1.9.21
============

Bugfixes
********

croak if the psgi streamer fails
allows building coroae on raspberrypi
do not wait for write availability until strictly required
avoid segfault when async mode api is called without async mode
fixed plain (without suspend engine) async mode
do not spit errors on non x86 timerfd_create
support timerfd_create/timerfd_settime on __arm__

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

mountpoints for symcall
^^^^^^^^^^^^^^^^^^^^^^^

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
