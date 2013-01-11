The uWSGI project
=================

The uWSGI project aims at developing a full stack for building (and hosting) clustered/distributed network applications.

Mainly targeted at the web and its standards, it has been successfully used in a lot of different contexts.

Thanks to its pluggable architecture it can be extended without limits to support more platforms and languages. Currently, you can write plugins in C, C++ and Objective-C.

The "WSGI" part in the name is a tribute to the namesake Python standard, as it has been the first developed plugin for the project.

Versatility, performance, low-resource usage and reliability are the strengths of the project (and the only rules followed).

Included components (updated to latest stable release)
======================================================

The Core (implements configuration, processes management, sockets creation, monitoring, logging, shared memory areas, ipc, cluster membership and the SubscriptionSystem)

Request plugins (implement application server interfaces for various languages and platforms: WSGI, PSGI, Rack, Lua WSAPI, CGI, PHP, Go ...)

Gateways (implement load balancers, proxies and routers)

The :doc:`Emperor <Emperor>` (implements massive instances management and monitoring)

Loop engines (implement concurrency, components can be run in preforking, threaded, asynchronous/evented and green thread/coroutine modes. Various technologies are supported, including uGreen, Greenlet, Stackless, :doc:`Gevent <Gevent>`, Goroutines and Fibers)

.. note::

  With a large open source project such as uWSGI the code and the documentation may not always be in sync.
  The mailing list is the best source for help regarding uWSGI.


Table of Contents
=================

.. toctree::
   :maxdepth: 1

   Download
   Install
   Management
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
   AttachingDaemons
   ManagementFlag
   Inetd
   Upstart
   Embed
   Glossary

uWSGI Subsystems
================

.. toctree::
   :maxdepth: 1
   
   AlarmSubsystem
   Caching
   Cron
   Fastrouter
   InternalRouting
   Legion
   Locks
   Mules
   OffloadSubsystem
   Queue
   RPC
   SharedArea
   Signals
   Spooler
   SubscriptionServer



Scaling with uWSGI
==================

.. toctree::
   :maxdepth: 1

   Cheaper
   Emperor
   Broodlord
   Zerg
   DynamicApps
   SSLScaling

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
   Carbon
   StatsServer


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
