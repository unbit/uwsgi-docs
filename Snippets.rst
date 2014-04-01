Snippets
========

This is a collection of the most "funny" uses of uWSGI features


X-Sendfile emulation
--------------------

Even if your frontend proxy/webserver does not support X-Sendfile (or cannot access your static resources) you can emulate
it using offloading (your process/thread will delegate the static file serving to offload threads

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

this will force HTTPS for the whole site

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   
and this for /admin

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
   
   
Eventually you may want to send HSTS (HTTP Strict Transport Security) header too

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   route-if = equal:${HTTPS};on addheader:Strict-Transport-Security: max-age=31536000
   
   
Python Auto-reloading (DEVELOPMENT-ONLY !!!)
--------------------------------------------

In production you can monitor file/directory changes for triggering reloads (touch-reload, fs-reload...).

During development having a monitor for all of the loaded/used python modules can be handy. But please use it only during development.

The check is done by a thread that scans the modules list with the specified frequency:

.. code-block:: ini

   [uwsgi]
   ...
   py-autoreload = 2
   
will check for python modules changes every 2 seconds and eventually restart the instance.

Hey, use it only in development...

