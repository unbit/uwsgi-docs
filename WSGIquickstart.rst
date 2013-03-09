Quickstart for python/WSGI applications
=======================================

This quickstart will show you how to deploy simple WSGI applications and common frameworks

Installing uWSGI with python support
************************************

uWSGI is a (big) C application, so you need a c compiler (like the gcc or clang) and python development headers.

On a debian-based distro a

.. code-block:: sh

   apt-get install build-essential python-dev

will be enough

You have various ways to install uWSGI for python

via pip

.. code-block:: sh

   pip install uwsgi

using the network installer

.. code-block:: sh

   curl http://uwsgi.it/install | bash -s default /tmp/uwsgi

(this will install the uWSGI binary in /tmp/uwsgi, feel free to change it)

or simply downloading a source tarball and 'making' it

.. code-block:: sh

   wget http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
   tar zxvf uwsgi-latest.tar.gz
   cd <dir>
   make

after the build you will have a 'uwsgi' binary in the current directory

Installing via your package distribution is not covered (would be impossibile to make everyone happy), but all the general rules applies.

One thing you may want to take in account when testing this quickstart with distro supplied packages, is that very probably your distribution
has built uWSGI in modular way (every feature is a different plugin that must be loaded). To complete the quickstart
you have to add --plugin python,http to the first serie of example and --plugin python when the HTTP router is removed (it could make
no sense for you, just continue reading)

The first WSGI application
**************************

Let's start with the simple hello world example:

.. code-block:: python

   def application(env, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       return "Hello World"

save it as foobar.py

As you can see it is composed by a single python function. It is called "application" as this is the default function
that the uWSGI python loader will search for (but you can obviously customize it)

Deploy it on HTTP port 9090
***************************

Now start uwsgi to run an http server/router passing requests to your WSGI application:

.. code-block::

   uwsgi --http :9090 --wsgi-file foobar.py

That's all

Adding concurrency and monitoring
*********************************

The first tuning you would like to make is adding concurrency (by default uWSGI starts with a single process and a single thread)

You can add more processes with the ``--processes`` option or more threads with the ``--threads`` options (or you can have both).

.. code-block::

   uwsgi --http :9090 --wsgi-file foobar.py --processes 4 --threads 2

this will spawn 4 processes (each with 2 threads), a master process that will respawn your processes when they die and the HTTP router seen before.

One important task is monitoring. Understanding what is going on is vital in production deployment.

The stats subsystem allows you to export uWSGI internal statistics via json

.. code-block::

   uwsgi --http :9090 --wsgi-file foobar.py --processes 4 --threads 2 --stats :9191

make some request to your app and then telnet to the port 9191. You will get lot of funny infos.

There is a top-like tool for monitoring instances, named 'uwsgitop' (just pip install it)

Putting behind a full webserver
*******************************

Even if the uWSGI http router is solid and high-performance, you may want to put your application behind a fully capable webserver.

uWSGI natively speaks HTTP, FastCGI, SCGI and its specific protocol named "uwsgi" (yes, wrong naming choice).

The best performing protocol is obviously the uwsgi one, already supported by nginx and Cherokee (while various Apache modules are available).

A common nginx config is the following

.. code-block:: c

   location / {
       include uwsgi_params;
       uwsgi_pass 127.0.0.1:3031;
   }

this means, "pass every request to the server bound to port 3031 speaking the uwsgi protocol".

Now we can spawn uWSGI to natively speak the uwsgi protocol

.. code-block::

   uwsgi --socket 127.0.0.1:3031 --wsgi-file foobar.py --processes 4 --threads 2 --stats :9191

if you run ps aux you will see one process less. The http router has been removed as our "workers" (the processes assigned to uWGSI)
natively speak the uwsgi protocol.
