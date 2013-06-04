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

the "pipe" offload engine
*************************

memcached router improvements
*****************************

the new redis router
********************


Availability
^^^^^^^^^^^^
