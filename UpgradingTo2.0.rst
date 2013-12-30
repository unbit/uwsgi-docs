Upgrading your 1.x uWSGI instances to 2.0
=========================================

The following notes are for users moving rrom 1.0, 1.2 and 1.4 to uWSGI 2.0.

Users of the 1.9 tree can skip this document as 2.0 is a "stabilized/freezed" 1.9

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

The new sharedarea
******************

SNI
***

Legion
******

Websockets api
**************

Hooks
*****

New plugin build system
***********************

Transformations
***************

Strict mode
***********

Linux namespaces and FreeBSD jails advanced support
***************************************************

The Metrics subsystem
*********************

64bit reponses for RPC
**********************
