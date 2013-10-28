The Tornado loop engine
=======================

Supported suspend engines: ```greenlet```

Supported CPython versions: ```all of tornado supported versions```


The tornado loop engine allows you to integrate your uWSGI stack with the Tornado IOLoop class.

Basically every I/O operation of the server is mapped to a tornado IOLoop callback. Making RPC, remote caching, or simply writing responses
is managed by the Tornado engine.

As uWSGI is not written with a callback-based programming approach, integrating with those kind of libraries requires some form of "suspend" engine (green threads/coroutines)

Currently the only supported suspend engine is the "greenlet" one. Stackless python could work too (needs testing).

PyPy is currently not supported (albeit technically possibile thanks to continulets). Drop a mail to Unbit staff if you are interested.

Why ?
*****
The Tornado project includes a simple WSGI server by itself. In the same spirit of the Gevent plugin, the purpose of Loop engines is allowing external prejects
to use (and abuse) the uWSGI api, for better performance, versatility and (maybe the mosti mportant thing) resource usage.

All of the uWSGI subsystems are available (from caching to metrics) in your tornado apps, and the WSGI engine is the uWSGI one.


Installation
************

The tornado plugin is currently not built-in by default. To have both tornado and greenlet in a single binary you can do

.. code-block:: sh

UWSGI_EMBED_PLUGINS=tornado,greenlet pip install tornado greenlet uwsgi

Running it
**********

The ``--tornado`` option is exposed by the tornado plugin, allowing you to set optimal parameters:

.. code-block:: sh

   uwsgi --http-socket :9090 --wsgi-file myapp.py --tornado 100 --greenlet
   
this will run a uWSGI instance on http port 9090 using tornado as I/O (and time) management and greenlet as suspend engine

Integrating WSGI with the tornado api
*************************************

For the way WSGI works, dealing with callback based programming is pretty hard (if not impossible).

Thanks to greenlet we can suspend the execution of our WSGI callable until a tornado IOLoop event is available:

.. code-block:: py

   from tornado.httpclient import AsyncHTTPClient
   import greenlet
   import functools
   
   # this gives us access to the main IOLoop (the same used by uWSGI)
   from tornado.ioloop import IOLoop
   io_loop = IOLoop.instance()
   
   def handle_request(me, response):
       if response.error:
           print("Error:", response.error)
       else:
           me.result = response.body
           
    def application(e, sr):
        me = greenlet.getcurrent()
        http_client = AsyncHTTPClient()
        http_client.fetch("http://localhost:9191/services", functools.partial(handle_request, me))
        me.parent.switch()
        sr('200 OK', [('Content-Type','text/plain')])
        return me.result
