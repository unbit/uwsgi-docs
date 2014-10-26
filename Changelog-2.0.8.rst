uWSGI 2.0.8
===========

Note: this is the first version with disabled-by-default SSL3, if you need it, you can re-enable with --ssl-enable3 option

Bugfixes
--------

* fixed php SCRIPT_NAME usage when --php-app is in place
* allow "appendn" hook without second argument
* fix heap corruption in carbon plugin
* fix getifaddrs() memory management
* fixed tcsetattr() usage
* fixed kevent usage of return value
* ensure PSGI response headers are in the right format
* fixed attached daemons reload
* fixed SSL/TLS shutdown
* fixed mountpoints logic for path not ending with /
* fixed python3 support in spooler decorators (Adriano Di Luzio)

New Features
------------

RTSP and chunked input backports from 2.1 for the HTTP router
*************************************************************

The ``--http-manage-rtsp`` and ``--http-chunked-input` have been backported from 2.1 allowing the HTTP router
to detect RTSP and chunked requests automatically. This is useful for the upcoming https://github.com/unbit/uwsgi-realtime plugin

--hook-post-fork
****************

This custom hook allows you to call actions after each fork()

fallback to trollius for asyncio plugin
***************************************

If you build the asyncio plugin for python2, a fallback to the trollius module will be tried. This feature got basically zero coverage, so every report is welcome.

added sweep_on_full, clear_on_full and no_expire to --cache2
************************************************************

backported wait-for-fs/mountpoints from 2.1
*******************************************

improved the offload api (backport from 2.1)
********************************************

uWSGI 2.0.8 is compatible with the upcoming https://github.com/unbit/uwsgi-realtime plugin that allows the use of realtime features
(like websockets or audio/video streaming) using uWSGI offload engine + redis publish/subscribe

allows building external plugins as embedded
********************************************

automatically manage HTTP_X_FORWARDED_PROTO
*******************************************

Availability
------------

uWSGI 2.0.8 has been released on 20141026. Download it from:

http://projects.unbit.it/downloads/uwsgi-2.0.8.tar.gz
