uWSGI 1.9.20
============

Changelog [20131117]

First round of deprecations and removals for 2.0
************************************************

- The Go plugin is now considere "broken" and has been moved away from the 'plugins' directory. The new blessed way for running Go apps in uWSGI is using :doc:`GCCGO` plugin

- The --auto-snapshot option has been removed, advanced management of instances now happens via :doc:`MasterFIFO`

- The matheval support has been removed, while a generic 'matheval' plugin (for internal routing) is available (but not compiled in by default). See below for the new way for making "math" in config files.

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

Before this release every RPC response was limited to a size of 64k (16bit).

Now the RPC protocol automatically detects if more space is needed and can scale up to 64bit.

Another advantage of this approach is that only the required amount of memory per-response is allocated instead of blindly
creating a 64k chunk every time.

The new GCCGO plugin
^^^^^^^^^^^^^^^^^^^^

Check official docs: :doc:`GCCGO`

The plugin is in early stage of development but its already quite solid.

Simple math in configuration files
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As seen before we have removed matheval support in favor of a simplified interface:

http://uwsgi-docs.readthedocs.org/en/latest/Configuration.html#placeholders-math-from-uwsgi-1-9-20-dev

For example you can now automatically set the number of threads to (number_of_cpu_cores * 3):

.. code-block:: ini

   [uwsgi]
   ; %k is a magic var translated to the number of cpu cores
   threads = %(%k * 3)
   ...

New magic vars
^^^^^^^^^^^^^^

%t	unix time (in seconds, gathered at instance startup)

%T	unix time (in microseconds, gathered at instance startup)

%k	detected cpu cores

Perl/PSGI improvements
^^^^^^^^^^^^^^^^^^^^^^

Chunked input api: :doc:`Chunked`

psgix.io -> returns a Socket::IO object mapped to the connection file descriptor. You need to voluntary enable it with ``--psgi-enable-psgix-io``

uwsgi::rpc and uwsgi::connection_fd from the api

--plshell will invoke an interactive shell (based on Devel::REPL)

New native protocols: --https-socket and --ssl-socket
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

When built with ssl support uWSGI exposes two new native socket protocols: https and uwsgi over ssl.

Both options taks the following value: <addr>,<cert>,<key>[,ciphers,ca]

.. code-block::

   [uwsgi]
   https-socket = :8443,foobar.crt,foobar.key
   ...

PROXY (version1) protocol support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Recently Amazon ELB added support for HAProxy PROXY (version 1) protocol support. This simple protocol allows the frontend to pass
the real ip of the client to the backend.

Adding ``--enable-proxy-protocol`` will force the ``--http-socket`` to check for a PROXY protocol request for setting the REMOTE_ADDR and REMOTE_PORT fields

New metrics collectors
^^^^^^^^^^^^^^^^^^^^^^

avg -> compute the math average of children: --metric name=foobar,collector=avg,children=metric1;metric2

accumulator -> always add the value of the specified children to the final value

multiplier -> multiply the sum of the specified children for the value specified in arg1n


Availability
************

uWSGI 1.9.20 has been released on 20131117 and can be downloaded from

http://projects.unbit.it/downloads/uwsgi-1.9.20.tar.gz
