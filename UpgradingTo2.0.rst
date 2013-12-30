Upgrading your 1.x uWSGI instances to 2.0 (work in progress)
============================================================

The following notes are for users moving from 1.0, 1.2 and 1.4 to uWSGI 2.0.

Users of the 1.9 tree can skip this document as 2.0 is a "stabilized/freezed" 1.9

What's new
----------

License change
**************

uWSGI is GPL2 + linking exception instead of plain GPL2

this should address some legal issue with users compiling uWSGI as a library (libuwsgi.so) and loading non-gpl compatible plugins/libraries.


Non-blocking by default
***********************

All of the I/O of the uWSGI stack (from the core to the plugins) is now fully non-blocking.

No area in the whole stack is allowed to block (except your app obviously), and plugins must use the I/O api of uWSGI.

When you load loop engines like gevent or Coro::AnyEvent, the uWSGI internals are patched to support their specific non-blocking hooks.

What does it mean for app developers ?

Well, the most important aspect is that network congestions or kernel problems do not block your instances, bad behaving peers
are closed if they do not un-block in the socket-timeout interval (default 4 seconds)

Newer, Faster and better parsers
********************************

uWSGI 2.0 has support for pluggable protocols, the following protocols are supported and all of them have been updated
for better performance:

``uwsgi`` classic uwsgi parser, improved for reduced syscall usage

``http`` classic http parser, improved for reduced syscall usage (supports the PROXY1 protocol)

``https`` (new) support for native https

``fastcgi`` classic fastcgi parser, improved for reduced syscall usage

``scgi`` (new) support for SCGI

``suwsgi`` (new) secured uwsgi, uwsgi over ssl (supported by nginx 1.5)

``puwsgi`` (new) persistent uwsgi, uwsgi with persistent connections, supported only internally

``mongrel2`` classic zeromq/mongrel2 support, now it is exposed as a plugin

``raw`` (new) fake parser, allows you to write application directly working on file descriptors

The Master FIFO
***************

a signal-free new approach for managing your instances

http://uwsgi-docs.readthedocs.org/en/latest/MasterFIFO.html

New reloading ways
******************

uWSGI 2.0 introduce a blast of new ways for reloading instances.

An article is available: http://uwsgi-docs.readthedocs.org/en/latest/articles/TheArtOfGracefulReloading.html

The new generation caching subsystem
************************************

http://uwsgi-docs.readthedocs.org/en/latest/Caching.html

http://uwsgi-docs.readthedocs.org/en/latest/tutorials/CachingCookbook.html

The new sharedarea
******************

http://uwsgi-docs.readthedocs.org/en/latest/SharedArea.html

SNI
***

http://uwsgi-docs.readthedocs.org/en/latest/SNI.html

Legion
******

http://uwsgi-docs.readthedocs.org/en/latest/Legion.html

Websockets api
**************

http://uwsgi-docs.readthedocs.org/en/latest/WebSockets.html

Hooks
*****

http://uwsgi-docs.readthedocs.org/en/latest/Hooks.html

New plugin build system
***********************

It is pretty fun (and easy) to write uWSGI plugin, but (funny enough) the worst aspect was building them, as dealing with build profiles, cflags, ldflags and friends tend to lead to all sort of bugs and crashes.

A simplified (and saner) build system for external plugins have been added. Now you only need to call the uwsgi binary you want to build the plugin for:

.. code-block:: sh

   uwsgi --build-plugin <plugin>
   
where <plugin> is the directory where the plugin sources (ad the uwsgiplugin.py file) are stored.

A list of third party plugins is available:

http://uwsgi-docs.readthedocs.org/en/latest/ThirdPartyPlugins.html

Transformations
***************

http://uwsgi-docs.readthedocs.org/en/latest/Transformations.html

Strict mode
***********

while having the freedom of defining custom options in uWSGI config files is a handy features, sometimes typos will
bring you lot of headaches.

Adding --strict to your instance options will instruct uWSGI config parser to raise an error when not-available options have been specified.

If you are in trouble and want to be sure you did not have written wrong options, add --strict and retry


Linux namespaces and FreeBSD jails advanced support
***************************************************

http://uwsgi-docs.readthedocs.org/en/latest/Namespaces.html

http://uwsgi-docs.readthedocs.org/en/latest/FreeBSDJails.html

The Metrics subsystem
*********************

http://uwsgi-docs.readthedocs.org/en/latest/Metrics.html

http://uwsgi-docs.readthedocs.org/en/latest/tutorials/GraphiteAndMetrics.html

64bit reponses for RPC
**********************

CYGWIN support
**************

Yes, you can now build and run uWSGI on Windows systems :(

kFreeBSD support
****************

PyPy support
************

JVM support
***********

Mono support
************

V8 support
**********

Upgrading Notes
---------------

* snapshotting mode is no more available, check the new graceful reloading ways for better approaches

* mongrel2 support is no more built-in by default, you have to build the 'mongrel2' plugin to pair uWSGI with mongrel2

* ldap and sqlite support has been moved to two plugins, you need to load them for using their features

* dynamic options are no more, as well as the 'admin' plugin

* probes have been removed, the alarm framework presents better ways to monitor services

* the shared area api changed dramatically, check the new sharedarea docs
