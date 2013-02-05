uWSGI asynchronous/nonblocking modes (updated to uWSGI 1.9)
===========================================================

.. warning::

  Beware! Async modes will not speedup your app, they are aimed at improving concurrency.
  Do not expect enabling some of the modes will work flawlessly, asynchronous/evented/nonblocking
  systems require app cooperation, so if your app is not developed following specific async engine rules
  you are doing wrong. Do not trust people suggesting you to blindly use async/evented/nonblocking systems !!!
 
Glossary
--------

uWSGI, following its modular approach, split async engines in two families:

Suspend/Resume engine
*********************

They simply implement coroutine/greenthreads techniques. They have no event engine, so you have to use
the one supplied by uWSGI. An Event engine is generally a library exporting primitives for platform-independent
non-blocking I/O (Examples are libevent, libev, libuv...). The uWSGI event engine is automatically enabled using
the ``--async <n>`` option

Currently the uWSGI distribution includes the following suspend/resume engines:

``uGreen`` Unbit greenthreads implementation (based on swapcontext() )

``Greenlet`` Python greenlet module

``Stackless`` Stackless python

``Fiber`` Ruby 1.9 fibers

Running the uWSGI async mode without a proper suspend/resume engine will raise a warning, sor for a minimal non-blocking app
you will need something like that:

.. code-block:: sh

   uwsgi --async 100 --ugreen --socket :3031

An important aspect of suspend/resume engines is that they can easily destroy your process if it is not aware of them.
Some of the language plugins (most-notably python) has hooks to cooperate flawlessly with coroutine/greenthreads. Other languages
may fail miserably. Always check the uWSGI mailinglist or irc channel for updated infos.

Older uWSGI releases supported an additional system: callbacks.

Callbacks is the approach used by popular systems like node.js. This approach requires HEAVY app cooperation, and for complex projects
like uWSGI dealing with this is basically impossible. For that reason, callback approach IS NOT SUPPORTED (even if technically
possible)

Loop engines
************

Loop engines are packages/libraries exporting both suspend/resume techniques and an event system. When loaded, they override
the way uWSGI manages connections and signal handlers (uWSGI-signals NOT POSIX signals !).

Currently uWSGI supports the following loop engines:

``Gevent`` (python, libev, greenlet)

``Coro::AnyEvent`` (perl, coro, anyevent)

Albeit they are generally used by a specific language, pure-C uWSGI plugins (like the CGI one) can use them without problems
to increase concurrency.

Async switches
--------------

To enable one of the async mode, you use the --async option (or some shortcut for it exported by loop engine plugins).

The argument of the --async option is the number of 'cores' to initialize. Each core can manage a single request, so the more core you
spawn, more requests you will be able to manage (and more memory you will use...). The job of the suspend/resume engines
is stopping the current request management and moving to another core, and eventually come back to the old one and so on.

Technically, cores ar simple memory structures holding request's data, but to give the user the illusion of a multithread system
we use that term.

The switch between cores needs app cooperation. There are various way to accomplish that, and generally if you are using
a loop engine, all is automagic (or require very little effort)

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

If you run the ``tests.cpubound_async`` app on a non-async server, it will block all processing, not accepting other requests until the heavy cycle of 10000 ``<h1>`` s is done.

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
