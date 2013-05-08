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

WebDav is one of the much requested features for the project. We now have a beta-quality plugin, already supporting
additional standards like the carddav:

https://github.com/unbit/uwsgi/blob/master/t/webdav/carddav.ini

The official modifier is 35, and to mount a simple directory as a webdav shares (for use with windows, gnome...) you only need to
specify the --webdav-mount option:

.. code-block:: ini

   [uwsgi]
   plugin = webdav
   http-socket = :9090
   http-socket-modifier1 = 35
   webdav-mount = /home/foobar

remember to protect shares:

.. code-block:: ini

   [uwsgi]
   plugin = webdav,router_basicauth
   http-socket = :9090
   http-socket-modifier1 = 35
   route-run = basicauth:CardDav uWSGI server,unbit:unbit
   webdav-mount = /home/foobar

WebDav attributes are stored as filesystem xattr, so be sure to use a filesystem supporting them (ext4, xfs, hfs+...)

LOCK/UNLOCK support is still incomplete

Official docs will be available soon.

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

Stackless, Greenlet and Fiber support have been updated to support new async features

The radius plugin
^^^^^^^^^^^^^^^^^

You can now authenticate over radius servers using the router_radius plugin:

.. code-block:: ini

   [uwsgi]
   plugin = webdav,router_radius
   http-socket = :9090
   http-socket-modifier1 = 35
   route-run = radius:realm=CardDav uWSGI server,server=127.0.0.1:1812
   webdav-mount = /home/foobar

The SPNEGO plugin
^^^^^^^^^^^^^^^^^

Another authentication backend, using SPNEGO (kerberos)

.. code-block:: ini

   [uwsgi]
   plugin = webdav,router_spnego
   http-socket = :9090
   http-socket-modifier1 = 35
   route-run = spnego:HTTP@localhost
   webdav-mount = /home/foobar

The plugin is beta quality as it leaks memory (it looks like a bug in MIT-kerberos) and Heimdal implementation does not work.

More reports are wellcomed

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


