uWSGI Go support (1.4-dev)
==========================

Starting from uWSGI 1.4-dev you can host Go web applications in your uWSGI stack.

You can download Go from here:

http://golang.org/

currently only Linux i386/x86_64 and OSX are supported.

For OSX support, you need a go version > than 1.0.3 or you will need to aply that patch:

http://code.google.com/p/go/source/detail?r=62b7ebe62958


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
