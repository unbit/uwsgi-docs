Scaling SSL connections (uWSGI 1.5-dev)
=======================================

Distributing SSL servers in a cluster is an hard topic.
The biggest problem is sharing SSL sessions between different nodes.

The problem is amplified in non-blocking servers due to OpenSSL limits in the way sessions are managed.

For example, you cannot share sessions in a memcached servers and access them in a non-blocking way.

A common solution (compromise ?) til now has been using a single ssl terminator balancing request to multiple non-encrypted backends.

The solution works, but obviously does not scale.

Starting from uWSGI 1.5-dev an implementation (based on the stud project) of distributed caching has been added.

Step 1: using the uWSGI cache for storing SSL sessions
******************************************************

You can configure the SSL subsystem of uWSGI to use the shared cache. The SSL sessions timeout will
be ethe expire value of the cache item. In that way the cache sweeper (managed by the master) will destroy sessions
in respect of it

.. code-block:: ini

   [uwsgi]
   ; spawn the master process (it will run the cache sweeper thread)
   master = true
   ; store upto 20k sessions
   cache = 20000
   ; 4k are enough for ssl sessions
   cache-blocksize = 4096
   ; force the ssl subsystem to use the uWSGI cache as session storage
   ssl-sessions-use-cache = true
   ; set sessions timeout
   ssl-sessions-timeout = 300
   ; spawn an https router
   https = 192.168.173.1:8443,foobar.crt,foobar.key
   ; spawn 8 processes for the https router (all sharing the same sessions cache)
   http-processes = 8
   ; add a bunch of uwsgi nodes
   http-to = 192.168.173.2:3031
   http-to = 192.168.173.3:3031
   http-to = 192.168.173.4:3031
   ; add stats
   stats = 127.0.0.1:5001



