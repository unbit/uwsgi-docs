uWSGI Go support (1.4-dev)
==========================

Starting from uWSGI 1.4-dev you can host Go web applications in your uWSGI stack.

You can download Go from here:

http://golang.org/

currently only Linux i386/x86_64 and OSX are supported.

For OSX support, you need a go version > than 1.0.3 or you will need to aply that patch:

http://code.google.com/p/go/source/detail?r=62b7ebe62958

goroutines are supported (currently) ony on Linux i386/x86_64


Building uWSGI with Go support
******************************

As always you can build Go support as an embedded component or as a plugin.

The main difference with the others setup is that this time we will build a uwsgi library
and not a uwsgi binary. This library will be used by a Go package named uwsgi.go you can link with your apps.

Do not be afraid, you are lucky, as in the uWSGI distribution there is already a build profile to make a completely
(monolithic) distribution with Go support embedded.

At the end of the build procedure you will have a libuwsgi.so shared library and a uwsgi.a Go package.

To build uWSGI+go just run (from uWSGI sources directory)

.. code-block:: sh

   UWSGI_PROFILE=go make

or (if python is not in your system path, or you need to use a specific python version)

.. code-block:: sh

   python uwsgiconfig.py --build go


(obviously you can substitute 'python' with your needed path)

At the end of the build procedure you will have a libuwsgi.so file (copy or link it to a library directory
like /usr/local/lib or /usr/lib and eventually run ldconfig if needed) and a uwsgi.a file in a subdirectory
(based on your arch/os) in plugins/go/pkg.

The last message from the build procedure reports the GOPATH you should use when building uWSGI Go apps (copy/remember/anottate that value somewhere).
If you already knows how Go import system works, feel free to copy uwsgi.a in your system-wide GOPATH.

Writing the first Go application
********************************

By default the uWSGI Go plugin supports the http.DefaultServeMux handler, so if you are already
using such system, running apps in uWSGI should be extremely simple

.. code-block:: go

   package main

   import (
           "uwsgi"
           "net/http"
           "fmt"
   )

   func oneHandler(w http.ResponseWriter, r *http.Request) {
           fmt.Fprintf(w, "<h1>One</h1>")
   }


   func twoHandler(w http.ResponseWriter, r *http.Request) {
           fmt.Fprintf(w, "<h2>Two</h2>")
   }

   func main() {
           http.HandleFunc("/one/", oneHandler)
           http.HandleFunc("/two/", twoHandler)
           var u uwsgi.App
           uwsgi.Run(&u)
   }

