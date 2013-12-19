Quickstart for ruby/Rack applications
=====================================

The following instructions will guide you through installing and running a ruby-based uWSGI distribution, aimed at running Rack apps.

Installing uWSGI with Ruby support
**********************************

To build uWSGI you need a c compiler (gcc and clang are supported) and the python binary (it will only run the uwsgiconfig.py script that will execute the various compilation steps). As we are building a uWSGI binary with ruby support we need ruby development headers too (uby-dev package on debian-based distros)

You can build uWSGI manually:

.. code-block:: sh

   make rack
   
that is the same as

.. code-block:: sh

   UWSGI_PROFILE=rack make
   
that is the same of

.. code-block:: sh

   make PROFILE=rack
  
and

.. code-block:: sh

   python uwsgiconfig.py --build rack
   
If you are lazy, you can download, build and install a uWSGI+ruby binary in a single shot:

.. code-block:: sh

   curl http://uwsgi.it/install | bash -s rack /tmp/uwsgi
   
Or, more ruby-friendly:

.. code-block:: sh

   gem install uwsgi
   
All of this methods build a "monolithic" uWSGI binary. The uWSGI project is composed by dozens of plugins, you can choose to build the server core and having a plugin for every feature (that you will load when needed), or you can
build a single binary with the features you need. This kind of builds are called 'monolithic'.

This quickstart assumes a monolithic binary (so you do not need to load plugins). If you prefer to use your package distributions (instead of building uWSGI from official sources), see below

Note for distro packages
************************

You distribution very probably contains a uWSGI package set. Those uWSGI packages tend to be highly modulars, so in addition to the core you need to install the required plugins. Plugins must be loaded in your configs. In the learning phase we strongly suggest to not use distribution packages to easily follow documentation and tutorials.

Once you feel confortable with the “uWSGI way” you can choose the best approach for your deployments.

As an example, the tutorial makes use of the 'http' and 'rack' plugins. If you are using a modular build be sure to load the with the ``--plugins http,rack`` option

Your first Rack app
*******************

Rack is the standard way for writing ruby web apps.

This is a standard Rack Hello world script (call it app.ru):

.. code-block:: rb

   class App

     def call(environ)
       [200, {'Content-Type' => 'text/html'}, ['Hello']]
     end
     
   end
   
   run App.new
   
The .ru extension stands for "rackup" that is the deployment tool included in the rack distribution. Rackup uses a little DSL, so to use it into uWSGI you need to install the rack gem:

.. code-block:: sh

   gem install rack
   
Now we are ready to deploy with uWSGI:

.. code-block:: sh

   uwsgi --http :8080 --http-modifier1 7 --rack app.ru

(remember to replace ‘uwsgi’ if it is not in your current $PATH)

or if you are using a modular build (like the one of your distro)

.. code-block:: sh

   uwsgi --plugins http,rack --http :8080 --http-modifier1 7 --rack app.ru
