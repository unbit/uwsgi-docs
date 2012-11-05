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

**The last message from the build procedure reports the GOPATH you should use when building uWSGI Go apps (copy/remember/annotate that value somewhere).
If you already knows how Go import system works, feel free to copy uwsgi.a in your system-wide GOPATH.**

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

As you can note, the only differences from a standard net/http-based application are in the import "uwsgi" need, the instantiation
of the uwsgi.App struct ('class' if you like...) and the call of the uwsgi.Run function.

You can use the uwsgi.App instance to store global app-related values and to access the uWSGI api.

Building your first app
***********************

Now, supposing you have saved your app as helloworld.go, just run

.. code-block:: sh

   GOPATH=/home/foobar/uwsgi/plugins/go go build helloworld.go

change GOPATH to the value you got from the build procedure, or to the dir you have installed/copied uwsgi.a

If all goes well you will end with a 'helloworld' executable.

That executable is a full uWSGI server (yes, really).

.. code-block:: sh

   ./helloworld --http :8080 --http-modifier1 11

just point your browser to the port 8080 and check /one/ and /two/

You can start adding processes and a master as always

.. code-block:: sh

   ./helloworld --http :8080 --http-modifier1 11 --master --processes 8

Note: The modifier 11 is  officially assigned to go.

Going in production
*******************

In production environment you will probably puth a webserver/proxy in fron of your app.

So your nginx config will look like that::

   location / {
       include uwsgi_params;
       uwsgi_pass 127.0.0.1:3031;
       uwsgi_modifier1 11;
   }

while your uWSGI config will be something like that

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   master = true
   processes = 4

Finally simply run your app

.. code-block:: sh

   ./helloworld config.ini

Goroutines (currently Linux-only)
*********************************

Goroutines are very probably the most interesting feature of the Go platform.

A uWSGI loop engine for goroutines is automatically embedded in the uWSGI library whrn you
build with the go plugin.

To spawn goroutines in each uWSGI process just add goroutines = N option, where N is the number of goroutines to spawn

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   master = true
   processes = 4
   goroutines = 100

with that config you will spawn 100 goroutines for each uWSGI process, for a grand-total of 400 goroutines !!!

Goroutines, for the uWSGI-related part, maps to pthread, but you will be able to spawn coroutine-based tasks from your application.