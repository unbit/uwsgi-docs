Quickstart for python/WSGI applications
=======================================

This quickstart will show you how to deploy simple WSGI applications and common frameworks

Installing uWSGI with python support
************************************

uWSGI is a (big) C application, so you need a C compiler (like the gcc or clang) and python development headers.

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

.. code-block:: sh

   uwsgi --http :9090 --wsgi-file foobar.py

That's all

Adding concurrency and monitoring
*********************************

The first tuning you would like to make is adding concurrency (by default uWSGI starts with a single process and a single thread)

You can add more processes with the ``--processes`` option or more threads with the ``--threads`` options (or you can have both).

.. code-block:: sh

   uwsgi --http :9090 --wsgi-file foobar.py --processes 4 --threads 2

this will spawn 4 processes (each with 2 threads), a master process that will respawn your processes when they die and the HTTP router seen before.

One important task is monitoring. Understanding what is going on is vital in production deployment.

The stats subsystem allows you to export uWSGI internal statistics via json

.. code-block:: sh

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

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --wsgi-file foobar.py --processes 4 --threads 2 --stats :9191

if you run ps aux you will see one process less. The http router has been removed as our "workers" (the processes assigned to uWGSI)
natively speak the uwsgi protocol.

Automatically starting uWSGI on boot
************************************

If you think about writing some init.d script for spawning uWSGI, just sit down and realize that we are no more in 1995.

Each distribution has choosen its startup system (Upstart, SystemD...) and there are tons of process managers available (supervisord, god...).

uWSGI will integrate very well with all of them (we hope), but if you plan to deploy a big number of apps check the uWSGI :doc:`Emperor`
it is the dream of every devops.

Deploying Django
****************

Django is very probably the most used python web framework around. Deploying it is pretty easy (we continue our configuration with 4 processes with 2 threads each)

We suppose the django project is in /home/foobar/myproject

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --chdir /home/foobar/myproject/ --wsgi-file myproject/wsgi.py --processes 4 --threads 2 --stats :9191

with --chdir we move to a specific directory. In django this is required to correctly load modules.

if the file /home/foobar/myproject/myproject/wsgi.py (or whatever you have called your project) does not exist, you are very probably
using an old (<1.4) django version. In such a case you need a little bit more configuration.

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --chdir /home/foobar/myproject/ --pythonpath .. --env DJANGO_SETTINGS_MODULE=myproject.settings --module "django.core.handlers.wsgi.WSGIHandler()" --processes 4 --threads 2 --stats :9191

ARGH !!! what the hell is this ???

Yes, you are right, dealing with such long command lines is basically unpractical (and foolish). uWSGI supports various configuration styles.
In this quickstart we will use .ini files.

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   chdir = /home/foobar/myproject/
   pythonpath = ..
   env = DJANGO_SETTINGS_MODULE=myproject.settings
   module = "django.core.handlers.wsgi.WSGIHandler()"
   processes = 4
   threads = 2
   stats = :9191

...a lot better

Just run it

.. code-block:: sh

   uwsgi yourfile.ini

older (<1.4) Django releases need to set env, module and the pythonpath (note the .. that allows us to reach the myproject.settings module)


Deploying Flask
***************

Flask is another popular python web microframework

.. code-block:: python

   from flask import Flask

   app = Flask(__name__)

   @app.route('/')
   def index():
       return "<span style='color:red'>I am app 1</span>"

Flask exports its WSGI function (the one we called 'application' at the start of the page) as 'app', so we need to instruct uwsgi to use it

We still continue to use the 4 processes/2 threads and the uwsgi socket as the base

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --wsgi-file myflaskapp.py --callable app --processes 4 --threads 2 --stats :9191

the only addition is the --callable option.

Deploying Web2Py
****************

Again a popular choice. Unzip the web2py source distribution on a directory of choice and write a uWSGI config file

.. code-block:: ini

   [uwsgi]
   http = :9090
   chdir = path_to_web2py
   module = wsgihandler
   master = true
   processes = 8

this time we used again the HTTP router. Just go to port 9090 with your browser and you will see the web2py welcome page.

Click on the administartive interface and... OOOPS it does not work as it requires HTTPS.

Do not worry, the uWSGI router is HTTPS capable (be sure you have openssl development headers, eventually install them and rebuild uWSGI, the build system will automatically detect it)

First of all generate your key and certificate

.. code-block:: sh

   openssl genrsa -out foobar.key 2048
   openssl req -new -key foobar.key -out foobar.csr
   openssl x509 -req -days 365 -in foobar.csr -signkey foobar.key -out foobar.crt

you now have 2 files (well 3, counting the csr), foobar.key and foobar.crt. Change the uwsgi config

.. code-block:: ini

   [uwsgi]
   https = :9090,foobar.crt,foobar.key
   chdir = path_to_web2py
   module = wsgihandler
   master = true
   processes = 8

re-run uWSGI and connect with your browser to port 9090 using https://

A note on Python threads
************************

If you start uWSGI without threads, the python GIL will not be enabled, so threads generated by your application
will never run. You may not like that choice, but remember that uWSGI is a language independent server, so most of its choice
are for maintaining it "agnostic".

But do not worry, there are basically no choices made by the uWSGI developers that cannot be changed with an option.

If you want to maintain python threads support but without starting multiple threads for your application, just the --enable-threads option
(or enable-threads = true in ini style)

And now
*******

You should be already able to go in production with such few concepts, but uWSGI is an enormous project with hundreds of features
and configurations. If you want to be a better sysadmin, continue reading the full docs.
