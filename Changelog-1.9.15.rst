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

One of the most common error when writing uWSGI config files, are typos in option names.

As you can add any option in uWSGI config files, the system will accept anythyng you will write even if it is not a real uWSGI option.

While this approach is very powerful and allow lot of funny hacks, it can causes lot of headaches too.

If you want to check all of your options in one step, you can now add the --strict option. Unknown options will trigger a fatal error.

fallback configs
****************

Being very cheap (in term of resources) and supporting lot of operating system and architecture, uWSGI is heavily used in embedded systems.

One of the common feature in such a device is the "reset to factory defaults" feature.

uWSGI now natively support this kind of operation, thanks to the --fallback-config option.

If a uWSGI instance dies with exit(1) and a fallback-config is specified, the binary will be re-exec()'d with the new config as the only argument.

Let's see an example of a configuration with unbindable address (unprivileged user trying to bind to privileged port)

.. code-block:: ini

   [uwsgi]
   uid = 1000
   gid = 1000
   socket = :80
   
and a fallback one (bind to unprivileged port 8080)

.. code-block:: ini

   [uwsgi]
   uid = 1000
   gid = 1000
   socket = :8080
   
run it (as root, as we want to drop privileges):

.. code-block:: sh

   sudo uwsgi --ini wrong.ini --fallback-config right.ini
   
  
you will get in your logs:

.. code-block:: sh

   ...
   bind(): Permission denied [core/socket.c line 755]
   Thu Aug 29 07:26:26 2013 - !!! /Users/roberta/uwsgi/uwsgi (pid: 12833) exited with status 1 !!!
   Thu Aug 29 07:26:26 2013 - !!! Fallback config to right.ini !!!
   [uWSGI] getting INI configuration from right.ini
   *** Starting uWSGI 1.9.15-dev-4046f76 (64bit) on [Thu Aug 29 07:26:26 2013] ***
   ...

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
