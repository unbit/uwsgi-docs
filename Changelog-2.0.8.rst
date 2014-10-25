uWSGI 2.0.8
===========

Note: this is the first version with disabled-by-default SSL3

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

--hook-post-fork
****************

fallback to trollius for asyncio plugin
***************************************

added sweep_on_full, clear_on_full and no_expire to --cache2
************************************************************

backported wait-for-fs/mountpoints from 2.1
*******************************************

improved the offload api (backport from 2.1)
********************************************

allows building external plugins as embedded
********************************************

automatically manage HTTP_X_FORWARDED_PROTO
*******************************************

Availability
------------
