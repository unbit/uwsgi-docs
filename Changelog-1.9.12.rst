uWSGI 1.9.12
============

Work in progress, most of the following topics are under development

Bugfixes
^^^^^^^^

New Features
^^^^^^^^^^^^

Offloading big responses
************************

Take the following WSGI app:

.. code-block:: python

   def application(environ, start_response):
       start_response('200 OK', [('Content-Type', 'text/plain')])
       return 'u' * 100000000
       
it will generate about 100megs of data. 98% of the time the worker spent on the request was on the data transfer. As the whole response
is followed by the end of the request we can offload the data write to a thread and free the worker suddenly (so it will be able to handle a new request).

100megs are a huge value, but even 1MB can cause a dozen of poll()/write() syscalls that blocks your worker for a bunch of milliseconds

Thanks to the 'memory offload' facility added in 1.9.11 implementing it will be very easy.

Challenges:

how this will touch the translation subsystem ?

it will be cool to 'signal' big responses via the internal routing subsystem:

.. code-block:: ini

   [uwsgi]
   ...
   offload-threads = 8
   route = ^/bigxml offload:memory
   
The offload engine could be extended to support multiple instructions so we could enqueue response chunks built by a generator:

.. code-block:: python

   def application(environ, start_response):
       start_response('200 OK', [('Content-Type', 'text/plain')])
       for i in range(100000):
           yield 'u' * 1000

every yield will enqueue the memory chunk.

Problem: if too much chunks are enqueued memory usage could be a serious problem
