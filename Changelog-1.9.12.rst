uWSGI 1.9.12
============

Work in progress, most of the following topics are under development

Bugfixes
^^^^^^^^

- offloading cache writes will return the correct status code and not 202
- you can now control the path of temporary files setting the TMPDIR environment variable (this fixes an old issue for users without control over /tmp)
- fixed a compilation error on amqp imperial monitor
- cron commands are correctly escaped when reported in the stats server
- fixed fastcgi parser corner-case bug with big uploads

New Features
^^^^^^^^^^^^

Offloading responses
********************

Take the following WSGI app:

.. code-block:: python

   def application(environ, start_response):
       start_response('200 OK', [('Content-Type', 'text/plain')])
       return ['u' * 100000000]
       
it will generate about 100megs of data. 98% of the time the worker spent on the request was on the data transfer. As the whole response
is followed by the end of the request we can offload the data write to a thread and free the worker suddenly (so it will be able to handle a new request).

100megs are a huge value, but even 1MB can cause a dozen of poll()/write() syscalls that blocks your worker for a bunch of milliseconds

Thanks to the 'memory offload' facility added in 1.9.11 implementing it has been very easy.

The offloading happens via the :doc:`Transformations`

.. code-block:: ini

   [uwsgi]
   socket = :3031
   wsgi-file = myapp.py
   ; offload all of the application writes
   route-run = offload:
   
By default the response is buffered to memory until it reaches 1MB size. After that it will be buffered to disk and the offload engine
will use sendfile().

You can set the limit (in bytes) after disk buffering passing an argument to the offload:

.. code-block:: ini

   [uwsgi]
   socket = :3031
   wsgi-file = myapp.py
   ; offload all of the application writes (buffer to disk after 1k)
   route-run = offload:1024
   
"offload" MUST BE the last transformation in the chain

.. code-block:: ini

   [uwsgi]
   socket = :3031
   wsgi-file = myapp.py
   ; gzip the response
   route-run = gzip:
   ; offload all of the application writes (buffer to disk after 1k)
   route-run = offload:1024
   
   
JWSGI and JVM improvements
**************************

JRuby integration

--touch-signal
**************

A new touch option has been added allowing the rise of a uwsgi signal when a file is touched:

.. code-block:: ini

   [uwsgi]
   ...
   ; raise signal 17 on /tmp/foobar modifications
   touch-signal = /tmp/foobar 17
   ...

the "pipe" offload engine
*************************

A new offload engine allowing transfer from a socket to the client has been added.

it will be automatically used in the new router_memacached and router_redis plugins


memcached router improvements
*****************************


You can now store responses in memcached (as you can already do with uWSGI caching)

.. code-block:: ini

   [uwsgi]
   ...
   route = ^/cacheme memcachedstore:addr=127.0.0.1:11211,key=${REQUEST_URI}
   route = ^/cacheme2 memcachedstore:addr=192.168.0.1:11211,key=${REQUEST_URI}foobar
   ...
   
obviously you can get them too

.. code-block:: ini

   [uwsgi]
   ...
   route-run = memcached:addr=127.0.0.1:11211,key=${REQUEST_URI}
   ...
   
The memcached router is now builtin in the default profiles

the new redis router
********************

Based on the memcached router, a redis router has been added. It works in the same way:


.. code-block:: ini

   [uwsgi]
   ...
   route = ^/cacheme redisstore:addr=127.0.0.1:6379,key=${REQUEST_URI}
   route = ^/cacheme2 redisstore:addr=192.168.0.1:6379,key=${REQUEST_URI}foobar
   ...
   
... and get the values

.. code-block:: ini

   [uwsgi]
   ...
   route-run = redis:addr=127.0.0.1:6379,key=${REQUEST_URI}
   ...

The redis router is builtin by default

Availability
^^^^^^^^^^^^

uWSGI 1.9.12 will be available since 20130605 at the following url

...
