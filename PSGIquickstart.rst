Quickstart for perl/PSGI applications
=====================================


The following instructions will guide you through installing and running a perl-based uWSGI distribution, aimed at running PSGI apps.


Installing uWSGI with Perl support
**********************************

To build uWSGI you need a c compiler (gcc and clang are supported) and the python binary (it will only run the uwsgiconfig.py script that will execute the various
compilation steps). As we are building a uWSGI binary with perl support we need perl development headers too (libperl-dev package on debian-based distros)

You can build uWSGI manually:

.. code-block:: sh

   python uwsgiconfig.py --build psgi
   
that is the same as


.. code-block:: sh

   UWSGI_PROFILE=psgi make
   
or using the network installer:

.. code-block:: sh

   curl http://uwsgi.it/install | bash -s psgi /tmp/uwsgi
   
that will create a uWSGI binary in /tmp/uwsgi (feel free to change the path to whatever you want)

Note for distro packages
************************

You distribution very probably contains a uWSGI package set. Those uWSGI packages tend to be highly modulars, so in addition to the core you need to install
the required plugins. Plugins must be loaded in your configs. In the learning phase we strongly suggest to not use distribution packages to easily follow documentation and tutorials.

Once you feel confortable with the "uWSGI way" you can choose the best approach for your deployments.

Your first PSGI app
*******************

save it to a file named myapp.pl

.. code-block:: pl

   my $app = sub {
        my $env = shift;
        return [
                '200',
                [ 'Content-Type' => 'text/html' ],
                [ "<h1>Hello World</h1>" ],
        ];
   };

then run it via uWSGI in http mode:

.. code-block:: sh

   uwsgi --http :8080 --http-modifier1 5 --psgi myapp.pl

(remember to replace 'uwsgi' if it is not in your current $PATH)

or if you are using a modular build (like the one of your distro)

.. code-block:: sh

   uwsgi --plugins http,psgi --http :8080 --http-modifier1 5 --psgi myapp.pl

What is that '--http-modifier1 5' thing ???
*******************************************

uWSGI supports various languages and platform. When the server receives a request it has to know where to 'route' it.

Each uWSGI plugin has an assigned number (the modifier), the perl/psgi one has the 5. So --http-modifier1 5 means "route to the psgi plugin"

Albeit uWSGI has a more "human-friendly" :doc:`<InternalRouting>internal routing system` using modifiers is the fastest way, so, if possible always use them


Using a full webserver: nginx
*****************************

The supplied http router, is (yes, incredible) only a router. You can use it as a load balancer or a proxy, but if you need a full webserver (for efficiently serving static files or all of those task a webserver is good at), you can get rid of the uwsgi http router (remember to change --plugins http,psgi to --plugins psgi if you are using a modular build) and put your app behind nginx.

To communicate with nginx, uWSGI can use various protocol: http, uwsgi, fastcgi, scgi...

The most efficient one is the uwsgi one. Nginx includes uwsgi protocol support out of the box.

Run your psgi application on a uwsgi socket:

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --psgi myapp.pl

then add a location stanza in your nginx config


.. code-block:: c

   location / {
       include uwsgi_params;
       uwsgi_pass 127.0.0.1:3031;
       uwsgi_modifier1 5;
   }

Reload your nginx server, and it should start proxying requests to your uWSGI instance

Note that you do not need to configure uWSGI to set a specific modifier, nginx will do it using the ``uwsgi_modifier1 5;`` directive

Adding concurrency
******************

You can give concurrency to to your app via multiprocess,multithreading or various async modes.

To spawn additional processes use the --processes option

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --psgi myapp.pl --processes 4

To have additional threads use --threads

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --psgi myapp.pl --threads 8

Or both if you feel exotic

.. code-block::

   uwsgi --socket 127.0.0.1:3031 --psgi myapp.pl --threads 8 --processes 4
   
A very common non-blocking/coroutine library in the perl world is Coro::AnyEvent. uWSGI can use it (even combined with multiprocessing) simply including the ``coroae`` plugin.

To build a uWSGI binary with ``coroae`` support just run

.. code-block:: sh

   UWSGI_PROFILE=coroae make
   
or

.. code-block:: sh

   curl http://uwsgi.it/install | bash -s coroae /tmp/uwsgi
   
you will end with a uWSGI binary including both the ``psgi`` and ``coroae`` plugins.

Now run your application in Coro::AnyEvent mode:


.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --psgi myapp.pl --coroae 1000 --processes 4
   
it will run 4 processes each able to manage up to 1000 coroutines (or Coro microthreads).


Adding robustness: the Master process
*************************************

It is highly recommended to have the master process always running on productions apps.

It will constantly monitor your processes/threads and will add funny features like the :doc:`StatsServer`

To enable the master simply add --master

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --psgi myapp.pl --processes 4 --master


