uWSGI 2.0.5
===========

Changelog [20140501]

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

graceful reload of mule processes


return routing action

--emperor-no-blacklist

Icecast2 protocol helpers

--metrics-no-cores, --stats-no-cores, --stats-no-metrics

sharedarea improvements

UWSGI_GO_CHEAP_CODE

PROXY1 support for the http router (Credits: bgglenn)


reset_after_push for metrics (Credits: Babacar Tall)

setremoteaddr

the resolve option
