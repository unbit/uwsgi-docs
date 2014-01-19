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
   ; spawn 2 offload threads
   offload-threads = 2
   ; files under /private can be safely served
   static-safe = /private
   ; collect the X-Sendfile response header as X_SENDFILE var
   collect-header = X-Sendfile X_SENDFILE
   ; if X_SENDFILE is not empty, pass its value to the "static" routing action (it will automatically use offloading if available)
   response-route-if-not = empty:${X_SENDFILE} static:${X_SENDFILE}
   
