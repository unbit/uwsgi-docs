uWSGI 1.9.21
============

Latest 1.9 before 2.0 (scheduled at December 30th 2013)

From now on, all of the releases will be -rc's (no new features will be added)

A document describing notes for upgrades from the (extremely obsolete) 1.2 and 1.4 versions is on work.

This release includes a new simplified plugins builder subsystem directly embedded in the uWSGI binary.

A page reporting all of the third plugins is available: :doc:`ThirdPartyPlugins`

And now....

Changelog [20131211]

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

Inernally when the first response body is sent, uWSGI check if response headers have been sent too, and eventually send them with an additional write() call.

This new optimizations allows uWSGI to send both headers and the first body chunk with single writev() syscall.

If the writev() returns with an incomplete write on the second vector, the system will fallback to simple write().

use a single buffer for websockets outgoing packets
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before this patch every single websocket packet required to allocate a memory chunk.

This patch forces the reuse of a single dynamic buffer. For games this should result in a pretty good improvement in responsiveness.

New features
************

removed zeromq api
^^^^^^^^^^^^^^^^^^

The zeromq api (a single function indeed) has been removed. Each plugin rquiring zeromq cam simply call zmq_init() insteadd of uwsgi_zeromq_init().

The mongrel2 support has been moved to a 'mongrel2' plugin.

The new sharedarea
^^^^^^^^^^^^^^^^^^

The shared area subsystem has been rewritten (it is incompatible with the old api as it requires a new argument as it now supports multiple memory areas).

Check updated docs: :doc:`SharedArea`

report request data in writers and readers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

every error when readign and writing to/from the client will report current request's data.

This should simplify debugging a lot.

Modular logchunks management
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tmsecs and tmicros, werr, rerr, ioerr
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

5 new request logging variables are available:

tmsecs: report the current unix time in milliseconds

tmicros: report the current unix time in microseconds

werr: report the number of write errors for the current request

rerr: report the number of read errors for the current request

ioerr: the sum of werr and rerr

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
