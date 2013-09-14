uWSGI 1.9.16
============

Changelog [20130914]


Important change in the gevent plugin shutdown/reload procedure !!!
*******************************************************************

The shutdown/reload phase when in gevent mode has been changed to better integrate
with multithreaded (and multigreenlet) environments (most notably the newrelic agent).

Instead of "joining" the gevent hub, a new "dummy" greenlet is spawned and "joined".

During shutdown only the greenlets spawned by uWSGI are taken in account, and after all of them are destroyed
the process will exit. This is different from the old approach where the process wait for ALL the currently available greenlets
(and monkeypatched threads).

If you prefer the old behaviout just specify the option --gevent-wait-for-hub 


Bugfixes/Improvements
*********************

- fixed CPython reference counting bug in rpc and signal handlers
- improved smart-attach-daemon for slow processes
- follow Rack specifications for QUERY_STRING,SCRIPT_NAME,SERVER_NAME and SERVER_PORT
- report missing internal routing support (it is only a warning when libpcre is missing)
- better ipcsem support during shutdown and zerg mode (added --persistent-ipcsem as special case)
- fixed fastcgi bug exposed by apache mod_fastcgi
- do not call pre-jail hook on reload
- force linking with -lrt on solaris
- report thunder lock status
- allow custom priority in rsyslog plugin

New features
************

FreeBSD jails native support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

uWSGI got nativr FreeBSD jails support. Official documentation is here :doc:`FreeBSDJails`

The Rados plugin
^^^^^^^^^^^^^^^^

Author: Javier Guerra

Based on the :doc:`GlusterFS` plugin, a new one allowing access to Rados object storage is available:

 :doc:`Rados`

The TunTap router
^^^^^^^^^^^^^^^^^

Linux O_TMPFILE
^^^^^^^^^^^^^^^

Latest Linux kernel support a new operational mode for opening files: O_TMPFILE

this flag open a temporary file (read: unlinked) without any kind of race conditions.

This mode is automatically used if available (no options needed)

Linux pivot-root
^^^^^^^^^^^^^^^^

When dealing with Linux namespaces, changing the root filesystem is one of the main task.

chroot() is generally too simple, while pivot-root allows you more advanced setup

The syntax is ``--pivot-root <new_root> <old_root>``

Cheaper memlimit
^^^^^^^^^^^^^^^^

Log encoders
^^^^^^^^^^^^

There are dozens of log engines and storage system nowadays. The original uWSGI approach was developing a plugin for every engine.

While working with logstash and fluentd we realized that most of the logging pluging are reimplementations of teh same concept over and over again.

We followed an even more modular approach introducing log encoders:

:doc:`LogEncoders`

They are basically patterns you can apply to each logline

New "advanced" Hooks
^^^^^^^^^^^^^^^^^^^^

New mount/umount hooks
^^^^^^^^^^^^^^^^^^^^^^




Availability
************

uWSGI 1.9.16 has been released on September 14th 2013. You can download it from:

http://projects.unbit.it/downloads/uwsgi-1.9.16.tar.gz
