uWSGI 1.9.9
===========

Changelog [20130507]

Special Warning !!!
*******************

The router_basicauth plugin has changed its default behaviour to return "break" if authorization fails.

The "basicauth-next" action, uses the old behaviour (returning "next")

This new approach should reduce security problems caused by wrong configurations

Bugfixes
********

* do not increment "tx" statistics counter for "unaccountable" plugins
* fixed --backtrace-depth
* fixed cache-sync parsing
* fixed mule farms initialization
* fixed multithreading bug when regexp conditional route is used
* fixed default-app usage in the psgi plugin
* fixed python dynamic mode + threads
* fixed error reporting in corerouter when retry is in place
* correctly report harakiri condition for gateways

New Features
************

The WebDav plugin
^^^^^^^^^^^^^^^^^

Support for Go 1.1 (more or less, sad news for go users...)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Albeit you can successfully embed go 1.1 apps in uWSGI, go 1.1 will be completely fork() unsafe.

That means you are not able to use multiprocessing, the master, mules and so on.

Basically half of the uWSGI features will be no more usable in go apps.

Things could change in the future, but currently our objective is better integration with the gccgo project.

Go 1.0.x will continue to be supported (unless gccgo shows itself as a better alternative)

More to come soon.

Improved async modes
^^^^^^^^^^^^^^^^^^^^

The radius plugin
^^^^^^^^^^^^^^^^^

The SPNEGO plugin
^^^^^^^^^^^^^^^^^

The ldap authenticator
^^^^^^^^^^^^^^^^^^^^^^

New internal routing features
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Removed the GOON action

setscriptname

donotlog

route-if regexp

Gevent atexit hook
^^^^^^^^^^^^^^^^^^


Streaming transformations
^^^^^^^^^^^^^^^^^^^^^^^^^

The xattr plugin
^^^^^^^^^^^^^^^^

The airbrake plugin
^^^^^^^^^^^^^^^^^^^

Legion Daemons
^^^^^^^^^^^^^^

No, it is not a blackmetal band, it is a new feature of :doc:`Legion` allowing you to run external processes
only when an instance is a lord:

--touch-exec
^^^^^^^^^^^^


Math for cache
^^^^^^^^^^^^^^


Availability
************


