Current Core Features
=====================

 * Written totally in C
 * Very fast (and simple) communication protocol for webservers integration (:doc:`Apache2`, :doc:`Nginx`, :doc:`Cherokee` and :doc:`Lighttpd` etc.)
 * Low memory footprint (thanks to evil premature optimizations)
 * Support for multiple application in the same process/domain
 * A master process manager that will allows you to automatically respawn processes and monitor the stack status. See :doc:`ProcessManagement`.
 * Support for multiple protocols (:doc:`uwsgi<Protocol>`), :doc:`HTTP`, :doc:`FastCGI` and :doc:`Mongrel2` available out of the box)
 * Preforking mode to improve concurrency
 * Address space and rss usage reports
 * Advanced logging (files, TCP, UDP, Redis, MongoDB, ZeroMQ...) see :doc:`Logging`)
 * Fast static file serving via `sendfile()` (where available)
 * Portability (tested on Linux 2.6/3.x, Solaris/!OpenSolaris/!OpenIndiana, OpenBSD, NetBSD, DragonflyBSD, FreeBSD >= 8.0, MacOSX, Nexenta, and Haiku), including strange architectures like SPARC64 or ARM.
 * Support for threads (configurable, available from 0.9.7-dev)
 * CGI mode for lazy users or ugly webservers
 * 'Harakiri mode' for self-healing
 * Vector based I/O to minimize syscall usage
 * Hot-add of applications. See :doc:`DynamicApps` and :doc:`uwsgi protocol variables<uWSGIVars>`
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
 * Graceful restart of worker processes and hot-plug substitution/upgrade of the uWSGI server using :doc:`Signals<uWSGISignals>`. See :doc:`uWSGIReload<uWSGIReload>`
 * A shared memory area to share data between workers/processes. See :doc:`SharedArea<SharedArea>`
 * An integrated :doc:`Spooler<Spooler>` for managing long running tasks and more generic (programmable) :doc:`Mule<Mules>` processes.
 * Message exchanging (via uwsgi protocol) for easy-implementation of distributed applications (look at ClusteredExamples)
 * Get statistics of all the workers using the EmbeddedModule
 * Integrated async/evented :doc:`proxy/load-balancer/router<FastRouter>`
 * Address space usage limiting (from version 0.9.5)
 * Automatically reload workers when a specific memory usage is reached
 * integrated :doc:`SNMP agent<UseSnmp>`, StatsServer and :doc:`Nagios` support (from version 0.9.5)
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