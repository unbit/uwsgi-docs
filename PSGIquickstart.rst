Quickstart for perl/PSGI applications
=====================================


The following instructions will guide you through installing and running a perl-based uWSGI distribution, aimed at running PSGI apps.


Installing uWSGI with Perl support
**********************************

To build uWSGI you need a c compiler (gcc and clang are supported) and the python binary (it will only run the uwsgiconfig.py script that will run the various
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
   
that will create a uWSGI binary in /tmp/uwsgi (feel free to change to path to whatever you want)

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

uwsgi --http :8080 --http-modifier1 5 --psgi myapp.pl

(remember to replace 'uwsgi' if it is not in your current $PATH)

or if you are using a modular build (like the one of your distro)

uwsgi --plugins http,psgi --http :8080 --http-modifier1 5 --psgi myapp.pl

What is that '--http-modifier1 5' thing ???
*******************************************

uWSGI supports various languages and platform. When the server receives a request it has to know where to 'route' it.

Each uWSGI plugin has an assigned number (the modifier), the perl/psgi one has the 5. So --http-modifier1 5 means "route to the psgi plugin"

Albeit uWSGI has a more "human-friendly" :doc:`InternalRouting internal routing system` using modifiers is the fastest way, so, if possible always use them
