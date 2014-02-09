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
- fixed sni recured subscription
- CGI plugin does not require anymore that Status header is the first one (Andjelko Horvat)
- fixed CPython mule_msg_get timeout parsing
- allows embedding of config files via absolute paths
- fixed symcall rpc
- fixed a memory leak in CPython spooler api (xiaost)
- The --no-orphans hardening has been brought back (currently Linux-only)
- improved dotsplit router mode to reduce DOS risk
- sub-Emperor are now loyal by default
- fixed non-shared ruby 1.8.7 support
- fixed harakiri tracebacker
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

for-readline
------------

%i and %j magic vars
--------------------

--inject-before and --inject-after
----------------------------------

--http-server-name-as-http-host
-------------------------------

better Emperor's Ragnarok (shutdown procedure)
----------------------------------------------

PyPy paste support
------------------

Availability
************
