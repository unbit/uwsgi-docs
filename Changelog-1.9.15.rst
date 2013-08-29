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
* fixed unshare() usage of 'fs'



New features
^^^^^^^^^^^^

The PTY plugin
**************

strict mode
***********

one of the most common error when writing uWSGI config files, are typos in option names.

As you can add any option in uWSGI config files, the system will accept anythyng you will write even if it is not a real uWSGI option.

While this approach is very powerful and allow lot of funny hacks, it ca cause lot of headaches.

If you want to check all of your options in one step, you can now add the --strict option. Unknown options will trigger an error.

fallback configs
****************

--perl-exec and --perl-exec-post-fork
*************************************

uwsgi.cache_keys([cache])
*************************

added `%(ftime)` to logformat
*****************************

protect destruction of UNIX sockets when another instance binds them
********************************************************************

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

--cwd
*****

--add-gid
*********

Emperor and Linux namespaces improvements
*****************************************

Availability
^^^^^^^^^^^^
