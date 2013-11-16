The gccgo plugin
================

uWSGI 1.9.20 officially substituted the old :doc:`Go` plugin with a new one based on gccgo.

The usage of gccgo allows more features and better integration with the uWSGI deployment styles.

A version of the gcc suite >= 4.8 is expected (and strongly suggested)

How it works
************

when the plugin is enabled a new go runtime is initialized after each fork()

if a main Go function is available in the process address space it will be executed in the Go runtime, otherwise to control
goes back to the uWSGI loop engine.

Why not plain go ?
******************

Unfortunately the standard go runtime is not (currently) embeddable and does not support compiling code as shared libraries.

Both are requisite for a meaningful uWSGI integration.

Starting from gcc 4.8.2 its libgo has been improved a lot and building shared libraries as well as initializing the C runtime works like a charm (even if it required a bit of not very elegant hacks)

Building the plugin
*******************

A build profile is available allowing you to build a uWSGI+gccgo binary ready to load go shared libraries:

.. code-block:: sh

   make gccgo

The first app
*************


Shared libraries VS monolithic binaries
***************************************

One of the Go selling point for lot of developers is the "static all-in-one binary approach".

Basically a go app does not have dependencies, so half of the common deployments problems automagically disappear.

The uWSGI-friendly way for hosting go apps is having a uWSGI binary loading a specific go app in the form of a library.

If this is not acceptable, you can build a single binary with both uWSGI and the go app.

There are two different approaches to it:

rebuilding from uWSGI sources every time
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

using libuwsgi.so
^^^^^^^^^^^^^^^^^

Goroutines
**********

Thanks to the new gcc split stack feature, goroutines are sanely (read: they do not require a full pthread) implemented in gccgo.

A loop engine mapping every uWSGI core to a goroutine is available in the plugin itself.

To start uWSGI in goroutines mode just add ``--goroutines <n>`` where <n> is the maximum number of concurrent goroutines to spawn.

Like :doc:`Gevent` uwsgi signal handlers are executed in a dedicated goroutine.

uWSGI API
*********

Unfortunately really few pieces of the uWSGI api have been ported to the gccgo plugin. More features will be added in time for uWSGI 2.0

Currently exposed api functions:

``uwsgi.CacheGet(string, string) string``

``uwsgi.RegisterSignal``

Notes
*****
