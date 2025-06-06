.. note::

  The project is in maintenance mode (only bugfixes and updates for new languages apis).
  Do not expect quick answers on github issues and/or pull requests (sorry for that)
  A big thanks to all of the users and contributors since 2009.
  
The uWSGI project
=================

The uWSGI project aims at developing a full stack for building hosting services.

Application servers (for various programming languages and protocols), proxies, process managers and monitors are all implemented
using a common api and a common configuration style.

Thanks to its pluggable architecture it can be extended to support more platforms and languages.

Currently, you can write plugins in C, C++ and Objective-C.

The "WSGI" part in the name is a tribute to the namesake Python standard, as it has been the first developed plugin for the project.

Versatility, performance, low-resource usage and reliability are the strengths of the project (and the only rules followed).

Included components (updated to latest stable release)
======================================================

The Core (implements configuration, processes management, sockets creation, monitoring, logging, shared memory areas, ipc, cluster membership and the :doc:`SubscriptionServer`)

Request plugins (implement application server interfaces for various languages and platforms: WSGI, PSGI, Rack, Lua WSAPI, CGI, PHP, Go ...)

Gateways (implement load balancers, proxies and routers)

The :doc:`Emperor <Emperor>` (implements massive instances management and monitoring)

Loop engines (implement events and concurrency, components can be run in preforking, threaded, asynchronous/evented and green thread/coroutine modes. Various technologies are supported, including uGreen, Greenlet, Stackless, :doc:`Gevent <Gevent>`, Coro::AnyEvent, :doc:`Tornado <Tornado>`, Goroutines and Fibers)

.. note::

  Contributors for documentation (in addition to code) are always welcome.


Quickstarts
===========

.. toctree::
   :maxdepth: 1

   WSGIquickstart
   PSGIquickstart
   RackQuickstart
   Snippets


Table of Contents
=================

.. toctree::
   :maxdepth: 1

   Download
   Install
   BuildSystem
   Management
   LanguagesAndPlatforms
   SupportedPlatforms
   WebServers
   FAQ
   ThingsToKnow
   Configuration
   FallbackConfig
   ConfigLogic
   Options
   CustomOptions
   ParsingOrder
   Vars
   Protocol
   AttachingDaemons
   MasterFIFO
   Inetd
   Upstart
   Systemd
   Circus
   Embed
   Logging
   LogFormat
   LogEncoders
   Hooks
   WorkerOverride
   Glossary
   ThirdPartyPlugins

Tutorials
=========

.. toctree::
   :maxdepth: 1

   tutorials/CachingCookbook
   tutorials/Django_and_nginx
   tutorials/dreamhost
   tutorials/heroku_python
   tutorials/heroku_ruby
   tutorials/ReliableFuse
   tutorials/DynamicProxying
   tutorials/GraphiteAndMetrics


Articles
========

.. toctree::
   :maxdepth: 1

   articles/SerializingAccept
   #articles/MassiveHostingWithEmperorAndNamespaces
   articles/TheArtOfGracefulReloading
   articles/FunWithPerlEyetoyRaspberrypi
   articles/OffloadingWebsocketsAndSSE
   articles/WSGIEnvBehaviour



uWSGI Subsystems
================

.. toctree::
   :maxdepth: 1

   AlarmSubsystem
   Caching
   WebCaching
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
   StaticFiles
   SNI
   GeoIP
   Transformations
   WebSockets
   Metrics
   Chunked

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
   FreeBSDJails
   ForkptyRouter
   TunTapRouter


Keeping an eye on your apps
===========================

.. toctree::
   :maxdepth: 1

   Nagios
   SNMP
   PushingStats
   Carbon
   StatsServer
   Metrics


Async and loop engines
======================

.. toctree::
   :maxdepth: 1

   Async
   Gevent
   Tornado
   uGreen
   asyncio



Web Server support
==================

.. toctree::
   :maxdepth: 1

   Apache
   Cherokee
   HTTP
   HTTPS
   SPDY
   Lighttpd
   Mongrel2
   Nginx
   OpenBSDhttpd


Language support
==================

.. toctree::
   :maxdepth: 2

   Python
   PyPy
   PHP
   Perl
   Ruby
   Lua
   JVM
   Mono
   CGI
   GCCGO
   Symcall
   XSLT
   SSI
   V8
   GridFS
   GlusterFS
   Rados

Other plugins
=============

.. toctree::
   :maxdepth: 1

   Pty
   SPNEGO
   LDAP


Broken/deprecated features
==========================

.. toctree::
   :maxdepth: 1

   Erlang
   ManagementFlag
   Go


Release Notes
=============

Stable releases
---------------

.. toctree::
   :maxdepth: 1

   Changelog-2.0.30
   Changelog-2.0.29
   Changelog-2.0.28
   Changelog-2.0.27
   Changelog-2.0.26
   Changelog-2.0.25.1
   Changelog-2.0.25
   Changelog-2.0.24
   Changelog-2.0.23
   Changelog-2.0.22
   Changelog-2.0.21
   Changelog-2.0.20
   Changelog-2.0.19.1
   Changelog-2.0.19
   Changelog-2.0.18
   Changelog-2.0.17.1
   Changelog-2.0.17
   Changelog-2.0.16
   Changelog-2.0.15
   Changelog-2.0.14 
   Changelog-2.0.13.1
   Changelog-2.0.13
   Changelog-2.0.12
   Changelog-2.0.11.2
   Changelog-2.0.11.1
   Changelog-2.0.11
   Changelog-2.0.10
   Changelog-2.0.9
   Changelog-2.0.8
   Changelog-2.0.7
   Changelog-2.0.6
   Changelog-2.0.5
   Changelog-2.0.4
   Changelog-2.0.3
   Changelog-2.0.2
   Changelog-2.0.1
   Changelog-2.0
   Changelog-1.9.21
   Changelog-1.9.20
   Changelog-1.9.19
   Changelog-1.9.18
   Changelog-1.9.17
   Changelog-1.9.16
   Changelog-1.9.15
   Changelog-1.9.14
   Changelog-1.9.13
   Changelog-1.9.12
   Changelog-1.9.11
   Changelog-1.9.10
   Changelog-1.9.9
   Changelog-1.9.8
   Changelog-1.9.7
   Changelog-1.9.6
   Changelog-1.9.5
   Changelog-1.9.4
   Changelog-1.9.3
   Changelog-1.9.2
   Changelog-1.9.1
   Changelog-1.9



Past Sponsors
=============

https://www.pythonanywhere.com/

https://lincolnloop.com/

https://yourlabs.io/oss

https://fili.com

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
