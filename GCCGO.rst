The gccgo plugin
================

uWSGI 1.9.20 officially substituted the old :doc:`Go` plugin with a new one based on gccgo.

The usage of gccgo allows more features and better integration with the uWSGI deployment styles.

A version of the gcc suite >= 4.8 is expected (and strongly suggested)

How it works
************

when the plugin is enabled a new go runtime is initialized after each fork()

if a ``main`` Go function is available in the process address space it will be executed in the Go runtime, otherwise the control
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

You do not need to change the way you write webapps in Go. The net/http package can be used flawlessly:

.. code-block:: go

   package main

   import "uwsgi"
   import "net/http"
   import "fmt"



   func viewHandler(w http.ResponseWriter, r *http.Request) {
        fmt.Fprintf(w, "<h1>Hello World</h1>")
   }

   func main() {
        http.HandleFunc("/view/", viewHandler)
        uwsgi.Run()
   }

The only difference is in calling uwsgi.Run() instead of initializing the http go server

To build the code as shared library simply run:

.. code-block:: sh

   gcc -fPIC -shared -o myapp.so myapp.go
   
now let's run it under uWSGI:

.. code-block:: sh

   uwsgi --http-socket :9090 --http-socket-modifier1 11 --go-load ./myapp.so
   
gccgo plugin register itself as modifier1 11, so always remember to set it

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
