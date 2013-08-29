uWSGI 1.9.15
============

Changelog [20130829]

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

This new plugin allows you to generate pseudoterminals and attach them to your workers.

Pseudoterminals are then reachable via network (UNIX or TCP sockets).

You can use them for shared debugging or to have input channels on your webapps.

The plugin is in early stage of development (very few features) and it is not built in by default, but you can already male funny things like:

.. code-block:: ini

   [uwsgi]
   plugin = pty,rack
   ; generate a new pseudoterminal on port 5000 and map it to the first worker
   pty-socket = 127.0.0.1:5000
   
   ; classic options
   master = true
   processes = 2
   rack = myapp.ru
   socket = /tmp/uwsgi.socket
   
   ; run a ruby interactive console (will use the pseudoterminal)
   ; we use pry as it kick asses
   rbshell = require 'pry';binding.pry
   
now you can access the pseudoterminal with

.. code-block:: sh

   uwsgi --plugin pty --pty-connect 127.0.0.1:5000
   
you can run the client in various windows, it will be shared by all of the peers (all will access the same pseudoterminal).

We are sure new funny uses for it will popup pretty soon

preliminary documentation is available at :doc:`Pty`

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

This api function has been added to the python and pypy plugins. It allows you to iterate the keys of a local uWSGI cache.

It returns a list.

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

Every legion member will now announce its death as soon as a reload (or a shutdown) of the instance is triggered

The GlusterFS plugin (beta)
***************************

This new plugin make use ot the new glusterfs c api, avoiding the overhead of fuse when serving files stored on glusterfs servers.

The plugin supports the multiprocess and multithreades modes, while async modes are currently in beta.

Documentation is available: :doc:`GlusterFS`

--force-gateway
***************

all of the gateways (fastrouter, httprouter, rawrouter, sslrouter ...) has to be run under the master process.

By specifying --force-gateway, you will bypass this limit

preliminary python3 profiler (beta)
***********************************

The --profiler pycall/pyline profilers have been added to python3. They are beta quality (they leaks memory), but should be usable.

file monitor support for OpenBSD,NetBSD,DragonFlyBSD
****************************************************

Both --fs-reload and the @fmon decorator now work on this operating systems.

--cwd
*****

you can force the startup "current working directory" (used by --vacuum and the reloading subsystem) with this option.

It is useful in chroot setups where the binary executable change its place.

--add-gid
*********

This options allows you to add additional group ids to the current process. You can specify it multiple times.

Emperor and Linux namespaces improvements
*****************************************

Thanks to the cooperation with the pythonanywhere.com guys the Emperor has been improved for better Linux namespaces integration.

The --emperor-use-clone option allows you to use clone() instead of fork() for your vassal's spawn. In this way you can create the vassals
directly in a new namespace. The function takes the same parameters of the --unshare one

.. code-block:: sh

   uwsgi --emperor /etc/vassals --emperor-use-clone pid,uts
   
will create each vassal in a new pid and uts namespace

while

.. code-block:: sh

   uwsgi --emperor /etc/vassals --emperor-use-clone pid,uts,net,ipc,fs
   
will basically use all of the currently available namespaces.

Two new exec (and call) hooks are available:

--exec-as-emperor will run commands in the emperor soon after a vassal has been spawn (setting 4 env vars, UWSGI_VASSAL_CONFIG, UWSGI_VASSAL_PID, UWSGI_VASSAL_UID and UWSGI_VASSAL_GID)

--exec-as-vassal will run commands in the vassal just before calling exec() (so directly in the new namespaces)


--wait-for-interface
^^^^^^^^^^^^^^^^^^^^

As dealing with the Linux network namespace introduces lot of race conditions (expecially when working with virtual ethernets), this new option
allows you to pause an instance until a network interface is available.

This is useful when waiting for the emperor to move a veth to the vassal namespace, avoiding the vassal to run commands on the interface before is available


.. code-block:: ini

   [uwsgi]
   emperor = /etc/uwsgi/vassals
   emperor-use-clone = pid,net,fs,ipc,uts
   ; each vassal should have its veth pair, so the following commands should be improved
   exec-as-emperor = ip link del veth0
   exec-as-emperor = ip link add veth0 type veth peer name veth1
   ; do not use the $(UWSGI_VASSAL_PID) form, otherwise the config parser will expand it on startup !!!
   exec-as-emperor = ip link set veth1 netns $UWSGI_VASSAL_PID
   
.. code-block:: ini

   [uwsgi]
   ; suspend until the emperor attach veth1
   wait-for-interface = veth1
   ; the following hook will be run only after veth1 is available
   exec-as-root = sethostname vassal001
   exec-as-root = ifconfig lo up
   exec-as-root = ifconfig veth1 192.168.0.2
   uid = vassal001
   gid = vassal001
   socket = :3031
   ...


Availability
^^^^^^^^^^^^

uWSGI 1.9.15 has been released on August 29th 2013. You can download it from:

http://projects.unbit.it/downloads/uwsgi-1.9.15.tar.gz
