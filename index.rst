The uWSGI project
=================

uWSGI is an extremely advanced, sysadmin-friendly, highly-modular **application container server** written in POSIX-compatible C.

It can communicate with your front-end webserver via `HTTP <HTTP.rst>`_, FastCGI, ZeroMQ and its highly specified/optimized protocol named 'uwsgi' (all-lowercase) already supported out-of-the-box by a lot of webservers.

Born as a simple WSGI-only server, over time it has evolved in a complete stack for networked/:doc:`clustered<Clustering>` web applications, implementing :doc:`message/object passing<CustomRouting>`, :doc:`caching<Caching>`, :doc:`RPC` and :doc:`process management<ProcessManagement>`.

uWSGI can be run in preforking, threaded, :doc:`asynchronous/evented<Async>` and :doc:`green thread/coroutine<GreenThread>` modes. Various forms of green threads/coroutines are supported, including :doc:`uGreen`, Greenlet, Stackless, :doc:`Gevent` and :doc:`FiberLoop`.

Sysadmins will love it as it can be :doc:`configured via several methods<Configuration>`, including command line, environment variables, XML, INI, YAML, JSON, SQLite and LDAP.

Thanks to its pluggable architecture it can be extended without limits to support more platforms and languages. Currently, you can write plugins in C, C++ and Objective-C

To get started with uWSGI, take a look at the :doc:`Install` page. Then continue to :doc:`Quickstart` or if you are feeling daring, the :doc:`Options` page. Some example configurations are available on the :doc:`Examples` page.

.. note::

  With a large open source project such as uWSGI the code and the documentation may not always be in sync.
  The mailing list is the best source for help regarding uWSGI.


Table of Contents
=================

.. toctree::
   :maxdepth: 1

   Download
   Install
   LanguagesAndPlatforms
   WebServers
   FAQ
   ThingsToKnow
   Configuration
   ConfigLogic
   Options
   Vars
   Protocol
   AlarmSubsystem
   AttachingDaemons
   Signals
   Reload
   SharedArea
   Glossary

Scaling with uWSGI
==================

.. toctree::
   :maxdepth: 1

   Emperor
   Broodlord
   Zerg

Securing uWSGI
==============

.. toctree::
   :maxdepth: 1

   Capabilities
   Cgroups
   KSM
   Namespaces


Keeping an eye on your apps
===========================

.. toctree::
   :maxdepth: 1

   SNMP

Async and loop engines
======================

.. toctree::
   :maxdepth: 1

   Async
   Gevent


Web Server support
==================
   
.. toctree::
   :maxdepth: 1
 
   Apache
   Cherokee
   HTTP
   Lighttpd
   Mongrel2
   Nginx


Language support
==================
   
.. toctree::
   :maxdepth: 2
 
   Python
   PHP
   Perl
   Ruby
   Lua
   Erlang
   JVM
   Mono
   CGI
   Go

Current Core Features
=====================

 * Written totally in C
 * Very fast (and simple) communication protocol for web server integration
 * Low memory footprint (thanks to plenty of evil premature optimization)
 * Support for multiple applications in the same process/domain
 * A master process manager that will allows you to automatically respawn processes and monitor the stack status. See :doc:`ProcessManagement`.
 * Support for multiple protocols (:doc:`uwsgi<Protocol>`), :doc:`HTTP<HTTP>`, FastCGI and :doc:`Mongrel2<Mongrel2>` available out of the box)
 * Preforking mode to improve concurrency
 * Address space and rss usage reports
 * Advanced logging (files, TCP, UDP, Redis, MongoDB, ZeroMQ...) -- see :doc:`Logging`.
 * Fast static file serving via `sendfile()` (where available)
 * Portability (tested on Linux 2.6/3.x, Solaris/!OpenSolaris/!OpenIndiana, OpenBSD, NetBSD, DragonflyBSD, FreeBSD >= 8.0, MacOSX, Nexenta, and Haiku), including strange architectures like SPARC64 or ARM.
 * Support for threads (configurable, available from 0.9.7-dev)
 * CGI mode for lazy users or ugly webservers
 * 'Harakiri mode' for self-healing
 * Vector based I/O to minimize syscall usage
 * Hot-add of applications. See :doc:`dynamic apps <DynamicApps>` and :doc:`uwsgi protocol variables <Vars>`
 * On the-fly configuration parameters. See :doc:`ManagementFlag`
 * Big professional user-base (hundreds of production WSGI/PSG/Rack apps being run on uWSGI) thanks to its main development managed and sponsored by the Italian ISP Unbit
 * Commercial support available
 * All code is under GPL2 (but you can buy a commercial license if you want to modify it without releasing source code)
 * Configurable buffer size for low-memory system or to manage big requests
 * Customizable builds (you can remove unneeded functionality) 
 * Intelligent worker respawner with a no-fork-bombing policy
 * Limit requests per worker
 * Process reaper for external process managers (like daemontools). Avoids zombie workers.
 * Per-request modifier for advanced users (See :doc:`Nginx` for example usage, and :doc:`Protocol` for the modifiers list)
 * UNIX and TCP socket support
 * Graceful restart of worker processes and hot-plug substitution/upgrade of the uWSGI server using :doc:`Signals<Signals>`. See :doc:`Reload`
 * A shared memory area to share data between workers/processes. See :doc:`SharedArea<SharedArea>`
 * An integrated :doc:`Spooler<Spooler>` for managing long running tasks and more generic (programmable) :doc:`Mule<Mules>` processes.
 * Message exchanging (via uwsgi protocol) for easy-implementation of distributed applications (look at ClusteredExamples)
 * Get statistics of all the workers using the EmbeddedModule
 * Integrated async/evented :doc:`proxy/load-balancer/router<FastRouter>`
 * Address space usage limiting (from version 0.9.5)
 * Automatically reload workers when a specific memory usage is reached
 * Integrated :doc:`SNMP agent<SNMP>`, StatsServer and :doc:`Nagios` support (from version 0.9.5)
 * RRDTool and :doc:`Graphite/Carbon<Carbon>` support
 * :doc:`VirtualHosting`
 * Embedded async/evented :doc:`HTTP server<HTTP>` for easy development/testing and load balancing (from version 0.9.6)
 * :doc:`Emperor` mode for massive hosting (from version 0.9.7)
 * Linux :doc:`Cgroups<Cgroups>`, :doc:`POSIX Capabilities<Capabilities>`, :doc:`KSM` and :doc:`Namespaces<LinuxNamespace>` support (from version 0.9.7)
 * :doc:`SignalFramework` and :doc:`CronInterface` for managing external events (file system modifications, timers...)
 * Shared cache/hashtable/dictionary. See :doc:`Caching`
 * Shared circular queue (usable as a stack, fifo or simple array). See :doc:`Queue`
 * Cheap, cheaper, idle and lazy modes, to automatically scale/deactivate/activate workers or control fork behaviour. See :doc:`ProcessManagement`
 * ZergMode to automatically add workers to already running instances
 * Snapshotting of running workers to allows emergency resume of apps
 * :doc:`Systemd`, :doc:`Inetd` and :doc:`Upstart` support
 * :doc:`Internal Routing<InternalRouting>` subsystem (from 1.1)
 * :doc:`ConfigLogic` and :doc:`CustomOptions` for simple dynamic configurations

Contact
=======

============  =
Mailing list  http://lists.unbit.it/cgi-bin/mailman/listinfo/uwsgi
Gmane mirror  http://dir.gmane.org/gmane.comp.python.wsgi.uwsgi.general
IRC           #uwsgi @ irc.freenode.org. The owner of the channel is `unbit`.
Twitter       http://twitter.com/unbit
============  =

.

Donate
======

uWSGI development is sponsored by the Italian ISP `Unbit <http://unbit.it/>`_ and its customers. You can buy commercial support and licensing. If you are not an Unbit customer, or you cannot/do not want to buy a commercial uWSGI license, consider making a donation. Obviously please feel free to ask for new features in your donation.

We will give credit to everyone who wants to sponsor new features.

See the `old uWSGI site <http://projects.unbit.it/uwsgi/#Donateifyouwant>`_ for the donation link. You can also donate via `GitTip <https://www.gittip.com/unbit/>`_.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
