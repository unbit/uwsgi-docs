Native HTTP support
===================


.. toctree::
   :maxdepth: 1

   HTTPS

HTTP sockets
------------

The ``http-socket <bind>`` option will make uWSGI natively speak HTTP.  If your
web server does not support the :doc:`uwsgi protocol <Protocol>` but is able to
speak to upstream HTTP proxies, or if you are using a service like Webfaction
or Heroku to host your application, you can use ``http-socket``.  If you plan
to expose your app to the world with uWSGI only, use the ``http`` option
instead, as the router/proxy/load-balancer will then be your shield.

The uWSGI HTTP/HTTPS router
---------------------------

uWSGI includes an HTTP/HTTPS router/proxy/load-balancer that can forward
requests to uWSGI workers.  The server can be used in two ways: embedded and
standalone.  In embedded mode, it will automatically spawn workers and setup
the communication socket. In standalone mode you have to specify the address of
a uwsgi socket to connect to.

Embedded mode::

  ./uwsgi --http 127.0.0.1:8080 --master --module mywsgiapp --processes 4

This will spawn a HTTP server on port 8080 that forwards requests to a pool of
4 uWSGI workers managed by the master process.

Standalone mode::

  ./uwsgi --master --http 127.0.0.1:8080 --http-to /tmp/uwsgi.sock

This will spawn a HTTP router (governed by a master for your safety) that will
forward requests to the uwsgi socket ``/tmp/uwsgi.sock``. You can bind to
multiple addresses/ports.

.. code-block:: ini

  [uwsgi]
  
  http = 0.0.0.0:8080
  http = 192.168.173.17:8181
  http = 127.0.0.1:9090
  
  master = true
  
  http-to = /tmp/uwsgi.sock

And load-balance to multiple nodes:

.. code-block:: ini

  [uwsgi]
  
  http = 0.0.0.0:8080
  http = 192.168.173.17:8181
  http = 127.0.0.1:9090
  
  master = true
  
  http-to = /tmp/uwsgi.sock
  http-to = 192.168.173.1:3031
  http-to = 192.168.173.2:3031
  http-to = 192.168.173.3:3031


* If you want to go massive (virtualhosting and zero-conf scaling) combine the
  HTTP router with the :doc:`SubscriptionServer`.
* You can make the HTTP server pass custom uwsgi variables to workers with the
  ``http-var KEY=VALUE`` option.
* You can use the ``http-modifier1`` option to pass a custom `modifier1` value
  to workers.

HTTPS support
-------------

see :doc:`HTTPS`

HTTP Keep-Alive
---------------

If your backends set the correct HTTP headers, you can use the
``http-keepalive`` option.  Your backends will need to set a valid
``Content-Length`` in each response or use chunked encoding. Simply setting
"Connection: close" is *not enough*.  Also remember to set "Connection:
Keep-Alive" in your response. You can automate that using the ``add-header
"Connection: Keep-Alive"`` option.

Can I use uWSGI's HTTP capabilities in production?
--------------------------------------------------

If you need a load balancer/proxy it can be a very good idea. It will
automatically find new uWSGI instances and can load balance in various ways.
If you want to use it as a real webserver you should take into account that
serving static files in uWSGI instances is possible, but not as good as using a
dedicated full-featured web server.  If you host static assets in the cloud or
on a CDN, using uWSGI's HTTP capabilities you can definitely avoid configuring
a full webserver.

.. note:: If you use Amazon's ELB (Elastic Load Balancer) in HTTP mode in
   front of uWSGI in HTTP mode, a valid ``Content-Length`` *must be set* by the
   backend.
