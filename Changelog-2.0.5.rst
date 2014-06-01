uWSGI 2.0.5
===========

Changelog [20140601]

Bugfixes
--------

- fixed support for repeated headers in lua plugin (Credits: tizoc)
- fixed support for embedding config in OpenBSD and NetBSD
- various fixes in the curl-based plugins (Credits: Yu Zhao)
- fixed milliseconds-based waits
- fixed sharedarea poller
- fixed stats server json escaper
- fixed fastcgi parser and implemented eof management (Credits:  Jeff Trawick)
- improved fast on-demand mode
- exclude avg_rt computation for static files
- fixed variables support in uwsgi internal router
- fixed websockets + keepalive ordering
- disable SIGPIPE management in corutines-based loop-engines
- fixed 64bit sharedarea management in 32bit systems
- honour chmod/chown-socket in fd0 mode
- hack for avoiding Safari iOS to make mess with keepalive
- fixed log setup when both --logto and --log2 (Credits: Łukasz Mierzwa)
- fixed mule_get_msg EAGAIN
- signal_pidfile returns the right error code
- fixed asyncio on OSX


New features
------------

graceful reload of mule processes (Credits: Paul Egan)
******************************************************

SIGHUP is now sent to mules instead of directly killing them. You are free to trap/catch the signal
in the code. If a mule does not die in the allowed "mercy time" (--mule-reload-mercy, default 60 seconds), SIGKILL will be sent.

return routing action (Credits: Yu Zhao)
****************************************

The new action will allow users to write simplified "break" clause.

For example, "return:403" is equivalent to "break:403 Forbidden",
with response body "Forbidden".

The response body is quite useful for telling end users what goes wrong.

--emperor-no-blacklist
**********************

this new option, completely disables the blacklisting Emperor subsystem

Icecast2 protocol helpers
*************************

One of the upcoming unbit.com projects is a uWSGI based audio/video streaming server.

The plugin (should be released during europython 2014) already supports the Icecast2 protocol.

A bunch of patches have been added to the http router to support the icecast2 protocol.

For example the ``--http-manage-source`` option allows the HTTP router to honour SOURCE method requests, automatically placing them in raw mode.

--metrics-no-cores, --stats-no-cores, --stats-no-metrics
********************************************************

When you have hundreds (or thousands) of async cores, exposing metrics of them could be really slow.

Three new options have been added allowing you to disable the generation of core-related metrics and (eventually) their usage in the stats server.

sharedarea improvements
***********************

The sharedarea api continues to improve. Latest patches include support for mmapping device directly from the command line.

A funny way for testing it, is mapping the raspberrypi BCM2835 memory, the following example allows you to read the rpi system timer

.. code-block:: sh

   uwsgi --sharedarea file=/dev/mem,offset=0x20003000,size=4096 ...
   
now you can read the 64bit value from the first (zero-based) sharedarea:

.. code-block:: python

   # read 64bit from 0x20003004
   timer = uwsgi.sharedarea_read64(0, 0x04)
   
obviously, pay attention when accessing rpi memory, an error could crash the whole system !!!

UWSGI_GO_CHEAP_CODE
*******************

This exit code (15) can be raised by a worker to tell the master to not respawn it

PROXY1 support for the http router (Credits: bgglenn)
*****************************************************

The option ``--http-enable-proxy-protocol`` allows the HTTP router to understand PROXY1 protocol requests (like the ones made by haproxy or amazon elb)

reset_after_push for metrics (Credits: Babacar Tall)
****************************************************

This metric attribute ensure that the matric value is reset to 0 (or its hardcoded initial_value) evry time the metric is pushed to some external system (like carbon, or statsd)

setremoteaddr
*************

This routing action allows you to completely override the REMOTE_ADDR detected by protocol handlers:

.. code-block:: ini

   [uwsgi]
   ; treat all requests as local
   route-run = setremoteaddr:127.0.0.1

the resolve option
******************

There are uWSGI options (or plugins) that do not automatically resolves dns name to ip addresses. This option allows you to map
a placeholder to the dns resolution of a string:

.. code-block:: ini

   [uwsgi]
   ; place the dns resolution of 'example.com' in the 'myserver' placeholder
   resolve = myserver=example.com
   subscribe2 = server=%(myserver),key=foobar

Availability
-------------
