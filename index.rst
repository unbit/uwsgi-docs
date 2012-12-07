The uWSGI project
=================

The uWSGI project aims at developing a full stack for building (and hosting) clustered/distributed network applications.

Mainly targeted at the web and its standards, it has been successfully used in a lot of different contexts.

Thanks to its pluggable architecture it can be extended without limits to support more platforms and languages. Currently, you can write plugins in C, C++ and Objective-C.

The 'WSGI' part in the name is a tribute to the namesake python standard, as it has been the first developed plugin for the project.

Versatility, performance, low-resource usage and reliability are the strenghts of the project (and the only rules followed).

Included components (updated to latest stable release)
======================================================

The Core (implements configuration, processes management, sockets creation, monitoring, logging, shared memory areas, ipc, cluster membership and the SubscriptionSystem)

Request plugins (implement application server interfaces for various languages and platforms: WSGI, PSGI, Rack, Lua WSAPI, CGI, PHP, Go ...)

Gateways (implement load balancers, proxies and routers)

The Emperor (implements massive instances management and monitoring)

Loop engines (implement concurrency, components can be run in preforking, threaded, asynchronous/evented and green thread/coroutine modes. Various technologies are supported, including uGreen – uWSGI Green Threads, Greenlet, Stackless, The Gevent loop engine, Goroutines and Fibers)

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
   CustomOptions
   Vars
   Protocol
   AlarmSubsystem
   AttachingDaemons
   Signals
   Reload
   SharedArea
   InternalRouting
   OffloadSubsystem
   Glossary

Scaling with uWSGI
==================

.. toctree::
   :maxdepth: 1

   Emperor
   Broodlord
   Zerg
   DynamicApps

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

   Nagios
   SNMP
   PushingStats

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
