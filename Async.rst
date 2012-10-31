uWSGI asynchronous mode
=======================


.. toctree::
   :maxdepth: 1

   uGreen

.. warning::

  Beware! To gain any advantage of using Async mode, your app has to be developed in an async way.
  Otherwise Async mode won't help you at all, and may actually lead into all sorts of nasty problems.

Starting from version 0.9.5 uWSGI can be run in async mode. uWSGI is generally a preforking/threading server but some apps or plugins can get huge performance improvements when run by an async server.


Async switches
--------------

Asynchronous programming is a complex topic few programmer/users really understand. A lot of emphasis has been put on async servers as of late, and most users (falsely) think that async mode is *fast* by default.  THIS IS NOT TRUE.

If you run an app that has not been designed to be async-friendly on an async server you are, simply said, doing it wrong. In order to help users evaluate if async mode is a good choice for their particular app, uWSGI maintains a count of the "async switches" your app does.

Every time your app calls ``yield`` (or :py:func:`uwsgi.suspend`s the execution) the "async switches" counter is incremented. At the end of every request this counter is reported in the uWSGI log. If the value is 0 or 1, then do yourself a favor and don't use Async mode. Your app will run faster and safer in preforking mode.

But if the "async switches" counter is high, your app *could* benefit from async mode. But, nevertheless:

.. warning:: 

  If you are in doubt DO NOT USE ASYNC MODE.

Running uWSGI in Async mode
---------------------------


To start uWSGI in async mode pass the ``async`` option with the number of "async cores" you want.


.. code-block:: sh

  ./uwsgi --socket :3031 -w tests.cpubound_async --async 10

This will start uWSGI with 10 async cores. Each async core can manage a request, so with this setup you can accept 10 concurrent requests with only one process. You can also start more processes (with the ``processes`` option). Each one will have its pool of async cores.

When using :term:`harakiri` mode, every time an async core accepts a request the harakiri timer is reset. So even if a request blocks the async system, harakiri will save you.

The ``tests.cpubound_async`` app is included in the source distribution. It's very simple:

.. code-block:: python

  def application(env, start_response):
      start_response( '200 OK', [ ('Content-Type','text/html') ])
      for i in range(1,10000):
          yield "<h1>%s</h1>" % i

Every time the application calls ``yield`` from the response function, the execution of the app is stopped, and a new request or a previously suspended request on another async core will take over. This means the number of async core is the number of requests that can be queued.

If you run the ``tests.cpubound_async`` app on a non-async server, it will block all processing, not accepting other requests until the heavy cycle of 10000 ``<h1>``s is done.

Waiting for I/O
---------------

There is currently one specification on how to have WSGI apps manage IO in async mode: `<http://wsgi.readthedocs.org/en/latest/specifications/fdevent.html>`_.

uWSGI supports this standard (``x-wsgiorg.fdevent.readable``, ``x-wsgiorg.fdevent.writable``, and ``x-wsgiorg.fdevent.timeout``) but also exports 2 more advanced functions in its API:

* :py:func:`uwsgi.wait_fd_read`
* :py:func:`uwsgi.wait_fd_write`

These functions may be called in succession to wait for multiple file descriptors:


.. code-block:: python

  uwsgi.wait_fd_read(fd0)
  uwsgi.wait_fd_read(fd1)
  uwsgi.wait_fd_read(fd2)
  yield "" # Yield the app, let uWSGI do its magic
  print "fd %d is ready" % env['uwsgi.ready_fd']


Sleeping
--------

On occasion you might want to sleep in your app, for example to throttle bandwidth.

Instead of using the blocking ``time.sleep(N)`` function, use ``uwsgi.async_sleep(N)`` to yield control for N seconds.

.. seealso:: See :file:`tests/sleeping_async.py` for an example.

Suspend/Resume
--------------

Yielding from the WSGI callable is not very practical as most of the time your app is more advanced than a simple callable and formed of tons of functions and various levels of call depth.

Worry not! uWSGI's async mode can use a coroutine/greenthread approach to suspend an async request (to pass control to another one) in any part of your code. :py:func:`uwsgi.suspend` will stop the current request.

.. code-block:: python

  uwsgi.wait_fd_read(fd0)
  uwsgi.suspend()

You can suspend your async requests using various techniques.

* :doc:`uGreen` - built in by default.

  .. code-block:: sh

    ./uwsgi --async <n> --ugreen

* Greenlet (plugin, also requires the greenlet module for Python)

  .. code-block:: sh
   
    python uwsgiconfig.py --plugin plugins/greenlet
    ./uwsgi --plugin greenlet --async <n> --greenlet

* Stackless (plugin, requires to build uWSGI with Stackless Python instead of CPython)

  .. code-block:: sh
    
    python uwsgiconfig.py --plugin plugins/stackless
    ./uwsgi --plugin stackless --async <n> --stackless

Static files
------------

uWSGI's :py:func:`uwsgi.sendfile` (where available) implementation is async-friendly, so if you need to serve lots of static files, wrapped by Python code of some sort, Async mode is a good choice.

.. seealso:: See :file:`tests/fileserve_async.py` for an example.

Comet apps
----------

The current implementation lets you easily develop Comet_ style applications -- if you run uWSGI behind an async-friendly webserver that allows long-running requests.

.. _Comet: http://en.wikipedia.org/wiki/Comet_(programming)

Mixed-mode apps
---------------

Some apps could get advantages of async mode with certain specific requests.

To achieve this, you can spawn 2 instances of uWSGI, on different sockets, one set up for async mode, the other for preforking. Then, in your web server's configuration file, point each URI/mountpoint to whichever socket would be the most useful.

.. TODO: Could the FastRouters, etc. be used instead? This seems a little clunky.


Improvements/todo
-----------------

uWSGI's async mode does currently not support the read of POST data in async mode. This is not a big problem for most apps, but if your webserver handler does not do buffering of POST data (Apache doesn't), there might be some performance problems with big uploads. This will be fixed in future releases.

.. TODO: Has this been fixed already?