The uWSGI offloading subsystem (1.4-rc2)
========================================

Offloading is a way to optimize tiny tasks, delegating them to one or more threads.

This threads run such tasks in a non-blocking/evented way allowing a huge amount of concurrency.

Various component of the uWSGI stack has been made offload-friendly, and the long-term target is to allow
application-code to abuse it.


To start the offloading subsystem just add --offload-threads <n>, where <n> is the number of threads (per-worker) to spawn.
They are native threads, they are lock-free (no shared resources) and they are the best way to abuse your CPU cores.

The number of offloaded requests is accounted in the "offloaded_requests" metric of the stats subsystem.


Offloading static files
***********************

The first component made offload-aware has been the static file serving system.

When offload threads are available, the whole transfer of the file is delegated to one of those threads, freeing your worker
suddenly (so it will be ready to accept new requests)

Example:

.. code-block:: ini

   [uwsgi]
   socket = :3031
   check-static = /var/www
   offload-threads = 4

Offloading internal routing
***************************

The router_uwsgi and router_http plugins are offload-friendly.

You can route requests to external uwsgi/HTTP servers without being worried about having a blocked worker during
the response generation.

Example:

.. code-block:: ini

   [uwsgi]
   socket = :3031
   route = ^/foo http:127.0.0.1:8080
   route = ^/bar http:127.0.0.1:8181
   route = ^/node http:127.0.0.1:9090

The Future
**********

The offloading subsystem has a great potential.

Next step is allowing the user to "program" it via the uwsgi api.