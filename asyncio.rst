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

Coroutines are more complex, they are pretty near to a greenlet, but internally are really different. Your WSGI callable can spawn coroutines.

Futures and coroutines
======================

Callback example
================

