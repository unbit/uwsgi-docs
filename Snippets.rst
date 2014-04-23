Snippets
========

This is a collection of some of the most "fun" uses of uWSGI features.

X-Sendfile emulation
--------------------

Even if your frontend proxy/webserver does not support X-Sendfile (or cannot access your static resources) you can emulate
it using uWSGI's internal offloading (your process/thread will delegate the actual static file serving to offload threads).

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_static plugin (compiled in by default in monolithic profiles)
   plugins = router_static
   ; spawn 2 offload threads
   offload-threads = 2
   ; files under /private can be safely served
   static-safe = /private
   ; collect the X-Sendfile response header as X_SENDFILE var
   collect-header = X-Sendfile X_SENDFILE
   ; if X_SENDFILE is not empty, pass its value to the "static" routing action (it will automatically use offloading if available)
   response-route-if-not = empty:${X_SENDFILE} static:${X_SENDFILE}
   

Force HTTPS
-----------

This will force HTTPS for the whole site.

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   
And this only for ``/admin``

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route = ^/admin goto:https
   ; stop the chain
   route-run = last:
   
   route-label = https
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   
Eventually you may want to send HSTS (HTTP Strict Transport Security) header too.

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   route-if = equal:${HTTPS};on addheader:Strict-Transport-Security: max-age=31536000
   
   
Python Auto-reloading (DEVELOPMENT ONLY!)
-----------------------------------------

In production you can monitor file/directory changes for triggering reloads (touch-reload, fs-reload...).

During development having a monitor for all of the loaded/used python modules can be handy. But please use it only during development.

The check is done by a thread that scans the modules list with the specified frequency:

.. code-block:: ini

   [uwsgi]
   ...
   py-autoreload = 2
   
will check for python modules changes every 2 seconds and eventually restart the instance.

And again:

.. warning:: Use this only in development.


Full-Stack CGI setup
--------------------

This example spawned from a uWSGI mainling-list thread.

We have static files in /var/www and cgis in /var/cgi. Cgi will be accessed using the /cgi-bin
mountpoint. So /var/cgi/foo.lua will be run on request to /cgi-bin/foo.lua

..code-block:: ini

   [uwsgi]
   workdir = /var
   ipaddress = 0.0.0.0
 
   ; start an http router on port 8080
   http = %(ipaddress):8080
   ; enable the stats server on port 9191
   stats = 127.0.0.1:9191
   ; spawn 2 threads in 4 processes (concurrency level: 8)
   processes = 4
   threads = 2
   ; drop privileges
   uid = nobody
   gid = nogroup
   
   ; serve static files in /var/www
   static-index = index.html
   static-index = index.htm
   check-static = %(workdir)/www
   
   ; skip serving static files ending with .lua
   static-skip-ext = .lua

   ; route requests to the CGI plugin
   http-modifier1 = 9
   ; map /cgi-bin requests to /var/cgi
   cgi = /cgi-bin=%(workdir)/cgi
   ; only .lua script can be executed
   cgi-allowed-ext = .lua
   ; .lua files are executed with the 'lua' command (it avoids the need of giving execute permission to files)
   cgi-helper = .lua=lua
   ; search for index.lua if a directory is requested
   cgi-index = index.lua
