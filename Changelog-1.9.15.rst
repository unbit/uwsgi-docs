uWSGI 1.9.15
============

Bugfixes
^^^^^^^^

* fixed jvm options hashmap (#364)
* fixed python3 wsgi.file_wrapper
* fixed python3 --catch-exceptions
* fixed type in pypy wsgi.input.read
* better symbol detection for pypy
* improved ruby libraries management on heroku
* fixed http-keepalive memleak
* fixed spooler body management under CPython



New features
^^^^^^^^^^^^

The PTY plugin
**************

strict mode
***********

fallback configs
****************

--perl-exec and --perl-exec-post-fork
*************************************

uwsgi.cache_keys([cache])
*************************

added `%(ftime)` to logformat
*****************************

--worker-exec2
**************

allow post_fork hook on general plugins
***************************************

--call hooks
************

init_func support for plugins, and --need-plugin variant
********************************************************

added commodity loader for the pecan framework
**********************************************

UWSGI_REMOVE_INCLUDES
*********************

router_expires
**************

announce Legion's death on reload/shutdown
******************************************

The GlusterFS plugin (beta)
***************************

--force-gateway
***************

preliminary python3 profiler (beta)
***********************************

file monitor support for OpenBSD,NetBSD,DragonFlyBSD
****************************************************



Availability
^^^^^^^^^^^^
