uWSGI 2.0.1
===========

Changelog [20140209]

Bugfixes and improvements
*************************

- due to a wrong prototype declaration, building uWSGI without SSL resulted in a compilation bug. The issue has been fixed.
- a race condition preventing usage of a massive number of threads in the PyPy plugin has been fixed
- check for heartbeat status only if heartbeat subsystem has been enabled
- improved heartbeat code to support various corner cases
- improved psgi.input to support offset in read()
- fixed (and simplified) perl stacktrace usage
- fixed sni secured subscription
- CGI plugin does not require anymore that Status header is the first one (Andjelko Horvat)
- fixed CPython mule_msg_get timeout parsing
- allows embedding of config files via absolute paths
- fixed symcall rpc
- fixed a memory leak in CPython spooler api (xiaost)
- The --no-orphans hardening has been brought back (currently Linux-only)
- improved dotsplit router mode to reduce DOS risk
- sub-Emperor are now loyal by default
- fixed non-shared ruby 1.8.7 support
- fixed harakiri CPython tracebacker
- request vars are now correctly exposed by the stats server
- support log-master for logfile-chown
- improved legion reload
- fixed tuntap netmask
- fixed busyness plugin without metrics subsystem

New features
************

uWSGI 2.0 is a LTS branch, so do not expect too much new features. 2.0.1 is the first maintainance release, so you still get a bunch of them
(mainly features not complete in 2.0)


Perl native Spooler support
---------------------------

Perl finally got full support for the Spooler subsystem. In 2.0 we added server support, in 2.0.1 we completed client support too.

--alarm-backlog
---------------

Raise the specified alarm when the listen queue is full

--close-on-exec2
----------------

simple notifications subsystem
------------------------------

pid namespace for daemons (Linux only)
--------------------------------------

Resubscriptions
---------------

filesystem monitor api
----------------------

support for yajl 1.0
--------------------

2.0 added support yajl JSON parser (version 2). 2.0.1 added support for 1.0 too

for-readline
------------

a config-logic iterator that yield file lines:

.. code-block:: ini

   [uwsgi]
   for-readline = /etc/myenvs
     env = %(_)
   end-for =

%i and %j magic vars
--------------------

%i -> returns the inode of the currently parsed file

%j -> returns hex representation of 32bit djb33x hashing of the currently parsed absolute filename

--inject-before and --inject-after
----------------------------------

--http-server-name-as-http-host
-------------------------------

Some Ruby/Rack middleware make a questionable check on SERVER_NAME/HTTP_HOST matching.

This flag allow the http router to map SERVER_NAME to HTTP_HOST automatically instead of instructing your uWSGI instances to do it.

better Emperor's Ragnarok (shutdown procedure)
----------------------------------------------

The 'Ragnarok' is the Emperor phase executed when you ask him to shutdown.

Before 2.0.1, this procedure simply send KILL to vassals to brutally destroy them.

The new Ragnarok is way more benevolent, asking vassals to gracefully shutdown.

The Emperor tolerance for vassals not shutting down can be tuned with --reload-mercy (default 30 seconds)

PyPy paste support
------------------

Two new options for PyPy plugin have been added for paste support:

--pypy-paste <config>

--pypy-ini-paste <ini>

they both maps 1:1 to the CPython variants, but contrary to it they automatically fix logging

Availability
************
