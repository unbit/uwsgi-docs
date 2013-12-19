Quickstart for ruby/Rack applications
=====================================

The following instructions will guide you through installing and running a ruby-based uWSGI distribution, aimed at running Rack apps.

Installing uWSGI with Ruby support
**********************************

To build uWSGI you need a c compiler (gcc and clang are supported) and the python binary (it will only run the uwsgiconfig.py script that will execute the various compilation steps). As we are building a uWSGI binary with ruby support we need ruby development headers too (ruby-dev package on debian-based distros)

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

As an example, the tutorial makes use of the 'http' and 'rack' plugins. If you are using a modular build be sure to load them with the ``--plugins http,rack`` option

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
   
Whit this command line we spawned an http proxy routing each request to a process (named the 'worker') that manages it and send back the response to the http router (that sends back to the client).

If you are asking yourself why spawning two processes, it is because this is the normal architecture you will use in production (a frontline webserver with a backend application server).

If you do not want to spawn the http proxy and directly force the worker to answer http requests just change the command line to

.. code-block:: sh

   uwsgi --http-socket :8080 --http-socket-modifier1 7 --rack app.ru
   
now you have a single process managing requests (but remember that directly exposing the application server to the public is generally dangerous and less versatile)

What is that '--http-modifier1 7' thing ???
*******************************************

uWSGI supports various languages and platforms. When the server receives a request it has to know where to 'route' it.

Each uWSGI plugin has an assigned number (the modifier), the ruby/rack one has the 7. So --http-modifier1 7 means "route to the rack plugin"

Albeit uWSGI has a more "human-friendly" :doc:`internal routing system <InternalRouting>` using modifiers is the fastest way, so, if possible always use them


Using a full webserver: nginx
*****************************

The supplied http router, is (yes, incredible) only a router. You can use it as a load balancer or a proxy, but if you need a full webserver (for efficiently serving static files or all of those task a webserver is good at), you can get rid of the uwsgi http router (remember to change --plugins http,rack to --plugins rack if you are using a modular build) and put your app behind nginx.

To communicate with nginx, uWSGI can use various protocol: http, uwsgi, fastcgi, scgi...

The most efficient one is the uwsgi one. Nginx includes uwsgi protocol support out of the box.

Run your rack application on a uwsgi socket:

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --rack app.ru

then add a location stanza in your nginx config


.. code-block:: c

   location / {
       include uwsgi_params;
       uwsgi_pass 127.0.0.1:3031;
       uwsgi_modifier1 7;
   }

Reload your nginx server, and it should start proxying requests to your uWSGI instance

Note that you do not need to configure uWSGI to set a specific modifier, nginx will do it using the ``uwsgi_modifier1 5;`` directive

Adding concurrency
******************

With the previous example you deployed a stack being able to serve a single request at time.

To increase concurrency you need to add more processes. If you hope there is a magic math formula to find the right number of processes
to spawn, lose it. You need to experiment and monitor your app to find the right value. Take in account every single process is a complete copy of your app, so memory should be taken in account.

To add more processes just use the `--processes <n>` option:

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --rack app.ru --processes 8
   
will spawn 8 processes.

Ruby 1.9/2.0 introduced an improved threads support and uWSGI supports it via the 'rbthreads' plugin. This plugin is automatically
build when you compile the uWSGI+ruby (>=1.9) monolithic binary.

To add more threads:

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --rack app.ru --rbthreads 4
   
or threads + processes

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --rack app.ru --processes --rbthreads 4
   
There are other (generally more advanced/complex) ways to increase concurrency (for example 'fibers'), but most of the time
you will end with plain old multiprocesses or multithreads models. (if you are interested you can check to uWSGI rack full docs)

Adding robustness: the Master process
*************************************

It is highly recommended to have the master process always running on productions apps.

It will constantly monitor your processes/threads and will add funny features like the :doc:`StatsServer`

To enable the master simply add --master

.. code-block:: sh

   uwsgi --socket 127.0.0.1:3031 --rack app.ru --processes 4 --master
   
Using config files
******************

uWSGI has literally hundreds of options (but generally you will not use more than a dozens of them). Dealing with them via command line is basically silly, so try to always use config files.
uWSGI supports various standards (xml, .ini, json, yaml...). Moving from one to another is pretty simple. The same options you can use via command line can be used
on config files simply removing the ``--`` prefix:

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   rack = app.ru
   processes = 4
   master = true
   
or xml:

.. code-block:: xml

   <uwsgi>
     <socket>127.0.0.1:3031</socket>
     <rack>app.ru</rack>
     <processes>4</processes>
     <master/>
   </uwsgi>
   
To run uWSGI using a config file, just specify it as argument:

.. code-block:: sh

   uwsgi yourconfig.ini
   
if for some reason your config cannot end with the expected extension (.ini, .xml, .yml, .js) you can force the binary to
use a specific parser in this way:

.. code-block:: sh

   uwsgi --ini yourconfig.foo
   
.. code-block:: sh

   uwsgi --xml yourconfig.foo

.. code-block:: sh

   uwsgi --yaml yourconfig.foo

and so on

You can even pipe configs (using the dash to force reading from stdin):

.. code-block:: sh

   ruby myjsonconfig_generator.rb | uwsgi --json -
   
The fork() problem when you spawn multiple processes
****************************************************

uWSGI is "perlish", there is nothing we can do to hide this thing. Most of its choices (starting from "There's more than one way to do it") cames from the perl world (and more generally from the UNIX sysadmins approaches).

Sometimes this approach could lead to unexpected behaviours when applied to other languages/platform.

One of the "problems" you can face when starting to learn uWSGI is its fork() usage.

By default uWSGI loads your application in the first spawned process and then fork() itself multiple times.

It means your app is loaded a single time and then copied.

While this approach speedups the start of the server, some application could have problems with this technique (expecially those initializing db connections
on startup, as the file descirptor of the connection will be inherited in the subprocesses)

If you are unsure about the brutal preforking used by uWSGI, just disable it with the ``--lazy-apps`` option. It will force uWSGI to completely load
your app one time per-worker

Deploying Sinatra
*****************

Let's forget about fork(), and back to funny things. This time we deploy a Sinatra application:

.. code-block:: rb

   require 'sinatra'

   get '/hi' do
     "Hello World"
   end

   run Sinatra::Application
   
save it as config.ru and run as seen before:

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   rack = config.ru
   master = true
   processes = 4
   lazy-apps = true
   
.. code-block:: sh

   uwsgi yourconf.ini
   
well maybe you have already noted that basically nothing changed from the previous app.ru examples.

That is because basically every modern Rack app exposes itself as a .ru file (generally called config.ru), so there is no need
for multiple options for loading application (like for example in the python/WSGI world)

Deploying RubyOnRails >= 3
**************************

Starting from 3.0, Rails is fully rack compliant, and exposes a config.ru file you can directly load (like we did with sinatra)

The only difference from sinatra is that your project has a specific layout/convention expecting your current working directory is the one containing the project, so le'ts add a chdir option:

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   rack = config.ru
   master = true
   processes = 4
   lazy-apps = true
   chdir = <path_to_your_rails_app>
   env = RAILS_ENV=production
   
.. code-block:: sh

   uwsgi yourconf.ini
   
in addition to chdir we have added the 'env' option that set the RAILS_ENV environment variable.

Starting from 4.0, Rails support multiple threads (only for ruby 2.0):

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   rack = config.ru
   master = true
   processes = 4
   rbthreads = 2
   lazy-apps = true
   chdir = <path_to_your_rails_app>
   env = RAILS_ENV=production

Deploying older RubyOnRails
***************************

Older Rails versions are not fully Rack-compliant. For such a reason a specific option is available in uWSGI to load older rails app (you will need the 'thin' gem too).

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   master = true
   processes = 4
   lazy-apps = true
   rails = <path_to_your_rails_app>
   env = RAILS_ENV=production
   
the 'rails' options must be specified instead of 'rack' passing the rails app directory as the argument

Bundler and RVM
***************

Bundler is the standard-de-facto ruby tool for managing dependancies. Basically you specify the gem needed by your app in the Gemfile text file and then you launch bundler to install them.

To allow uWSGI to honour bundler installations you only need to add:

.. code-block:: ini

   rbrequire = rubygems
   rbrequire = bundler/setup
   env = BUNDLE_GEMFILE=<path_to_your_Gemfile>

the first line is not required for ruby 1.9/2.x

Basically those lines force uWSGI to load the bundler engine and to use the Gemfile specified in the BUNDLE_GEMFILE environment variable.

When using Bundler (like modern frameworks do) your common deployment configuration will be:

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   rack = config.ru
   master = true
   processes = 4
   lazy-apps = true
   rbrequire = rubygems
   rbrequire = bundler/setup
   env = BUNDLE_GEMFILE=<path_to_your_Gemfile>
   
In addition to Bundler, RVM is another common tool.

It allows you to have multiple (independent) ruby installations (with their gemsets) on a single system.

To instruct uWSGI to use the gemset of a specific rvm version just use the `--gemset` option:

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   rack = config.ru
   master = true
   processes = 4
   lazy-apps = true
   rbrequire = rubygems
   rbrequire = bundler/setup
   env = BUNDLE_GEMFILE=<path_to_your_Gemfile>
   gemset = ruby-2.0@foobar
   
just pay attention you need a uWSGI binary (or a plugin if you are using a modular build) for every ruby version (ruby version, not gemset !!!)

If you are interested this is a list of commands to build a uWSGI core + 1 one plugin for every ruby version installed in rvm:

.. code-block:: sh

   # build the core
   make nolang
   # build plugin for 1.8.7
   rvm use 1.8.7
   ./uwsgi --build-plugin "plugins/rack rack187"
   # build for 1.9.2
   rvm use 1.9.2
   ./uwsgi --build-plugin "plugins/rack rack192"
   # and so on...
   
then if you want to use ruby 1.9.2 with the @oops gemset:

.. code-block:: ini

   [uwsgi]
   plugins = ruby192
   socket = 127.0.0.1:3031
   rack = config.ru
   master = true
   processes = 4
   lazy-apps = true
   rbrequire = rubygems
   rbrequire = bundler/setup
   env = BUNDLE_GEMFILE=<path_to_your_Gemfile>
   gemset = ruby-1.9.2@oops

Automatically starting uWSGI on boot
************************************

If you are thinking about writing some init.d script for spawning uWSGI, just sit (and calm) down and check if your system does not offer you a better (more modern) approach.

Each distribution has choosen its startup system (:doc:`Upstart<Upstart>`, :doc:`SystemD`...) and there are tons of process managers available (supervisord, god...).

uWSGI will integrate very well with all of them (we hope), but if you plan to deploy a big number of apps check the uWSGI :doc:`Emperor<Emperor>`
it is the dream of every devops.

Security and availability
*************************

ALWAYS avoid running your uWSGI instances as root. You can drop privileges using the uid and gid options

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   uid = foo
   gid = bar
   chdir = path_toyour_app
   rack = app.ru
   master = true
   processes = 8


A common problem with webapp deployment is "stuck requests". All of your threads/workers are stuck blocked on a request and your app cannot accept more of them.

To avoid that problem you can set an ``harakiri`` timer. It is a monitor (managed by the master process) that will destroy processes stuck for more than the specified number of seconds

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   uid = foo
   gid = bar
   chdir = path_toyour_app
   rack = app.ru
   master = true
   processes = 8
   harakiri = 30

will destroy workers blocked for more than 30 seconds. Choose carefully the harakiri value !!!

In addition to this, since uWSGI 1.9, the stats server exports the whole set of request variables, so you can see (in realtime) what your instance is doing (for each worker, thread or async core)

Enabling the stats server is easy:

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   uid = foo
   gid = bar
   chdir = path_toyour_app
   rack = app.ru
   master = true
   processes = 8
   harakiri = 30
   stats = 127.0.0.1:5000
   
just bind it to an address (UNIX or TCP) and just connect (you can use telnet too) to it to receive a JSON representation of your instance.

The ``uwsgitop`` application (you can find it in the official github repository) is an example of using the stats server to have a top-like realtime monitoring tool (with colors !!!)

Memory usage
************

Low memory usage is one of the selling point of the whole uWSGI project.

Unfortunately being aggressive with memory by default could (read well: could) lead to some performance problem.

By default the uWSGI rack plugin, calls the ruby GC after every request. If you want to reduce this rate just add the ``--rb-gc-freq <n>`` option, where n is the number of requests after the GC is called.

If you plan to make benchmarks of uWSGI (or compare it with other solutions) take in account its use of GC.

Ruby can be a memory devourer, so we prefer to be aggressive with memory by default instead of making hello-world benchmarkers happy.

Offloading
**********

:doc:`OffloadSubsystem` allows you to free your workers as soon as possible when some specific pattern matches and can be delegated
to a pure-c thread. Examples are sending static file from the filesystem, transferring data from the network to the client and so on.

Offloading is very complex, but its use is transparent to the end user. If you want to try just add --offload-threads <n> where <n> is the number of threads to spawn (one for cpu is a good value).

When offload threads are enabled, all of the parts that can be optimized will be automatically detected


And now
*******

You should already be able to go in production with such few concepts, but uWSGI is an enormous project with hundreds of features
and configurations. If you want to be a better sysadmin, continue reading the full docs.
