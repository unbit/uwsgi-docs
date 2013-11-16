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

Starting from gcc 4.8.2 its libgo has been improved a lot and building shared libraries as well as initializing the Go runtime works like a charm (even if it required a bit of not very elegant hacks)

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
   
If you get an error about gcc not able to resolve uwsgi symbols, just add -I<path_to_uwsgi_binary> to the command line (see below):

.. code-block:: sh

   gcc -fPIC -shared -I/usr/bin -o myapp.so myapp.go
   
now let's run it under uWSGI:

.. code-block:: sh

   uwsgi --http-socket :9090 --http-socket-modifier1 11 --go-load ./myapp.so
   
gccgo plugin register itself as modifier1 11, so always remember to set it

uwsgi.gox
*********

By default when building the gccgo profile, a uwsgi.gox file is created. This can be used when building
go apps using the uWSGI api, to resolve symbols. Take in account that if you add the directory containing the uwsgi binary (as seen before) to
the includes (-I path) path of gcc, the binary itself will be used for resolving symbols

Shared libraries VS monolithic binaries
***************************************

One of the Go selling point for lot of developers is the "static-all-in-one" binary approach.

Basically a go app does not have dependencies, so half of the common deployments problems automagically disappear.

The uWSGI-friendly way for hosting go apps is having a uWSGI binary loading a specific go app in the form of a library.

If this is not acceptable, you can build a single binary with both uWSGI and the go app:

.. code-block:: sh

   CFLAGS=-DUWSGI_GCCGO_MONOLITHIC UWSGI_ADDITIONAL_SOURCES=myapp.go UWSGI_PROFILE=gccgo make


Goroutines
**********

Thanks to the new gcc split stack feature, goroutines are sanely (read: they do not require a full pthread) implemented in gccgo.

A loop engine mapping every uWSGI core to a goroutine is available in the plugin itself.

To start uWSGI in goroutines mode just add ``--goroutines <n>`` where <n> is the maximum number of concurrent goroutines to spawn.

Like :doc:`Gevent` uwsgi signal handlers are executed in a dedicated goroutine.

In addition to this all of the blacking calls make use of the netpoll go api (this means you can run internal routing actions, included rpc, in a goroutine)

Options
*******

``--go-load <path>`` load the specified go shared library in the process address space

``--gccgo-load <path>`` alias for go-load

``--go-args <arg1> <arg2> <argN>`` set arguments passed to the virtual go command line

``--gccgo-args <arg1> <arg2> <argN>`` alias for go-args

``--goroutines <n>`` enable goroutines loop engine with the specified number of async cores

uWSGI API
*********

Unfortunately really few pieces of the uWSGI api have been ported to the gccgo plugin. More features will be added in time for uWSGI 2.0

Currently exposed api functions:

``uwsgi.CacheGet(key string, cache string) string``

``uwsgi.RegisterSignal(signum uint8, receiver string, handler func(uint8)) bool``

Notes
*****

Do not enable multithreading, it will not work and probably will never work

All of the uWSGI native features (like internal routing) work in goroutines mode, but do not expect languages (like python or perl) to work over them anytime soon.
