uWSGI 1.9.20
============

First round of deprecations and removals for 2.0
************************************************

- The Go plugin is now considere "broken" and has been moved away from the 'plugins' directory. The new blessed way for running Go apps in uWSGI is using the :doc:`GCCGO` plugin

- The --auto-snapshot option has been removed, advanced management of instances now happens via :doc:`MasterFifo`

- The matheval support has been removed, while a generic 'matheval' plugin (for internal routing) is available (but not compiled in by default)

- The 'erlang' and 'pyerl' plugins are broken and has been moved out of the 'plugins' directory. Erlang support will be completely rewritten after 2.0 release


Next scheduled deprecations and removals
****************************************

The zeromq api (a single function indeed) will be removed. Each plugin using zeromq will create its own zmq context (no need to share it). This means libzmq will no more be linked in the uWSGI core binary.

The mongrel2 protocol support will be moved to a 'mongrel2' plugin instead of being embedded in the core

Bugfixes
********

* fixed master hang when gracefully reloading in lazy mode
* fixed default_app usage
* another round of coverity fixes by Riccardo Magliocchetti
* fixed EAGAIN management when reading the body

New features
************

64bit return values for the RPC subsystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before this release every RPC response was limited to a size 64k (16bit).

Now the RPC protocol automatically detect if more space is needed and can scale up to 64bit.

Another advantage of this approach is that only the required amount of memory per-response is allocated instead of blindly
creating a 64k chunk every time.

The new GCCGO plugin
^^^^^^^^^^^^^^^^^^^^

Simple math in configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New magic vars
^^^^^^^^^^^^^^

Perl/PSGI improvements
^^^^^^^^^^^^^^^^^^^^^^

Chunked input api

psgix.io

uwsgi::rpc and uwsgi::connection_fd

--plshell

New native protocols: --https-socket and --ssl-socket
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

PROXY (version1) protocol support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recently Amazon ELB added support for HAProxy PROXY (version 1) protocol support. This simple protocol allows the frontend to pass
the real ip of the client to the backend.

Adding --enable-proxy-protocol will force the --http-socket to check for a PROXY protocol request for setting the REMOTE_ADDR and REMOTE_PORT fields

New metrics collectors
^^^^^^^^^^^^^^^^^^^^^^

avg

accumulator

multiplier


Availability
************
