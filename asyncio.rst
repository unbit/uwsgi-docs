The asyncio loop engine (CPython >= 3.4)
========================================

Status: EXPERIMENTAL, lot of implications, expecially in respect to the WSGI standard

The 'asyncio' plugin exposes a loop engine built on top of the 'asyncio' CPython api (https://docs.python.org/3.4/library/asyncio.html#module-asyncio)

As uWSGI is not callback-based, you need a suspend engine (currently only the 'greenlet' one is supported) to manage the WSGI callable.

Why not mapping the WSGI callable to a coroutine ?
==================================================

The reason is pretty simple, this would break WSGI in every possible way. For this reason each uWSGI core is mapped to a greenlet (running the WSGI callable).
This greenlet registers events and coroutines in the asyncio event loop.

Callback VS coroutines
======================

When starting playing with asyncio you may get confused between callback and coroutines.

The first ones are executed when a specific event raises (for example when a file descriptor is ready for read). They are basically standard functions executed
in the main greenlet (and eventually they can swithc back control to a specific uWSGI core).

Coroutines are more complex, they are pretty near to a greenlet, but internally they work on python frames instead of c stacks. From a python programmer point of view, coroutines are very special generators. Your WSGI callable can spawn coroutines.

Building uWSGI with asyncio support
===================================

An 'asyncio' build profile is available in the official source tree (it will build greenlet support too):

.. code-block:: sh

   CFLAGS="-I/usr/local/include/python3.4" make PYTHON=python3.4 asyncio
   
be sure to use python3.4 as the python version (or anything higher) and to add the greenlet include directory to CFLAGS (this could be not needed if you installed greenlet support from distro packages)


The first example: a simple callback
====================================

Let's start with a simple WSGI callable triggering a function after 2 seconds (after the callable has returned)

.. code-block:: python

   import asyncio
   
   def two_seconds_elapsed():
       print("Hello 2 seconds elapsed")
   
   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       asyncio.get_event_loop().call_later(2, two_seconds_elapsed)
       return [b"Hello World"]
       
Once called, the application function will register a callable in the asyncio event loop and then will return to the client.

After two seconds the event loop will run the function.

You can run the example with:

.. code-block:: sh

   uwsgi --asyncio 10 --http-socket :9090 --greenlet --wsgi-file app.py
   
(asyncio is a shortcut enabling 10 uWSGI async cores, so you can manage up to 10 concurrent requests with a single process)
   
But how to wait for a callback completion in the WSGI callable ? We can suspend our WSGI function using greenlets (remember our WSGI clalable is wrapped on a greenlet)

.. code-block:: python

   import asyncio
   import greenlet
   
   def two_seconds_elapsed(me):
       print("Hello 2 seconds elapsed")
       # back to WSGI  callable
       me.switch()
   
   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       myself = greenlet.getcurrent()
       asyncio.get_event_loop().call_later(2, two_seconds_elapsed, myself)
       # back to event loop
       myself.parent.switch()
       return [b"Hello World"]
       
And we can go even further abusing the uWSGI support for WSGI generators:

.. code-block:: python

   import asyncio
   import greenlet

   def two_seconds_elapsed(me):
       print("Hello 2 seconds elapsed")
       me.switch()

   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       myself = greenlet.getcurrent()
       asyncio.get_event_loop().call_later(2, two_seconds_elapsed, myself)
       myself.parent.switch()
       yield b"One"
       asyncio.get_event_loop().call_later(2, two_seconds_elapsed, myself)
       myself.parent.switch()
       yield b"Two"

Another example: Futures and coroutines
=======================================

You can spawn coroutines from your WSGI callable using the asyncio.Task facility:

.. code-block:: python

   import asyncio
   import greenlet

   @asyncio.coroutine
   def sleeping(me):
       yield from asyncio.sleep(2)
       # back to callable
       me.switch()


   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       myself = greenlet.getcurrent()
       # enqueue the coroutine
       asyncio.Task(sleeping(myself))
       # suspend to event loop
       myself.parent.switch()
       # back from event loop
       return [b"Hello World"]

thanks to Future we can even get results back from coroutines

.. code-block:: python

   import asyncio
   import greenlet

   @asyncio.coroutine
   def sleeping(me, f):
       yield from asyncio.sleep(2)
       f.set_result(b"Hello World")
       # back to callable
       me.switch()


   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       myself = greenlet.getcurrent()
       future = asyncio.Future()
       # enqueue the coroutine with a Future
       asyncio.Task(sleeping(myself, future))
       # suspend to event loop
       myself.parent.switch()
       # back from event loop
       return [future.result()]
       
       
and a more advanced example using the aiohttp module (rememebr to pip-install it)

.. code-block:: python

   import asyncio
   import greenlet
   import aiohttp

   @asyncio.coroutine
   def sleeping(me, f):
       yield from asyncio.sleep(2)
       response = yield from aiohttp.request('GET', 'http://python.org')
       body = yield from response.read_and_close()
       # body is a byterray !
       f.set_result(body)
       me.switch()


   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       myself = greenlet.getcurrent()
       future = asyncio.Future()
       asyncio.Task(sleeping(myself, future))
       myself.parent.switch()
       # this time we use yield, just for fun...
       yield bytes(future.result())

Status
======

The plugin is considered Experimental (currently the implications of asyncio with WSGI are unclear). In the future it could be built by default
when >= python3.4 is detected

While technically possible (more or less) mapping a WSGI callable to a python3 coroutine is not expected.

The plugin registers hooks for non blocking reads/writes and timers. This means you can use the uWSGI api with asyncio automagically. Check the https://github.com/unbit/uwsgi/blob/master/tests/websockets_chat_asyncio.py
example
