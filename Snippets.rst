Snippets
========

This is a collection of some of the most "fun" uses of uWSGI features.

X-Sendfile emulation
--------------------

Even if your frontend proxy/webserver does not support X-Sendfile (or cannot access your static resources) you can emulate
it using uWSGI's internal offloading (your process/thread will delegate the actual static file serving to offload threads).

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_static plugin (compiled in by default in monolithic profiles)
   plugins = router_static
   ; spawn 2 offload threads
   offload-threads = 2
   ; files under /private can be safely served
   static-safe = /private
   ; collect the X-Sendfile response header as X_SENDFILE var
   collect-header = X-Sendfile X_SENDFILE
   ; if X_SENDFILE is not empty, pass its value to the "static" routing action (it will automatically use offloading if available)
   response-route-if-not = empty:${X_SENDFILE} static:${X_SENDFILE}
   

Force HTTPS
-----------

This will force HTTPS for the whole site.

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   
And this only for ``/admin``

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route = ^/admin goto:https
   ; stop the chain
   route-run = last:
   
   route-label = https
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   
Eventually you may want to send HSTS (HTTP Strict Transport Security) header too.

.. code-block:: ini

   [uwsgi]
   ...
   ; load router_redirect plugin (compiled in by default in monolithic profiles)
   plugins = router_redirect
   route-if-not = equal:${HTTPS};on redirect-permanent:https://${HTTP_HOST}${REQUEST_URI}
   route-if = equal:${HTTPS};on addheader:Strict-Transport-Security: max-age=31536000
   
   
Python Auto-reloading (DEVELOPMENT ONLY!)
-----------------------------------------

In production you can monitor file/directory changes for triggering reloads (touch-reload, fs-reload...).

During development having a monitor for all of the loaded/used python modules can be handy. But please use it only during development.

The check is done by a thread that scans the modules list with the specified frequency:

.. code-block:: ini

   [uwsgi]
   ...
   py-autoreload = 2
   
will check for python modules changes every 2 seconds and eventually restart the instance.

And again:

.. warning:: Use this only in development.


Full-Stack CGI setup
--------------------

This example spawned from a uWSGI mainling-list thread.

We have static files in /var/www and cgis in /var/cgi. Cgi will be accessed using the /cgi-bin
mountpoint. So /var/cgi/foo.lua will be run on request to /cgi-bin/foo.lua

.. code-block:: ini

   [uwsgi]
   workdir = /var
   ipaddress = 0.0.0.0
 
   ; start an http router on port 8080
   http = %(ipaddress):8080
   ; enable the stats server on port 9191
   stats = 127.0.0.1:9191
   ; spawn 2 threads in 4 processes (concurrency level: 8)
   processes = 4
   threads = 2
   ; drop privileges
   uid = nobody
   gid = nogroup
   
   ; serve static files in /var/www
   static-index = index.html
   static-index = index.htm
   check-static = %(workdir)/www
   
   ; skip serving static files ending with .lua
   static-skip-ext = .lua

   ; route requests to the CGI plugin
   http-modifier1 = 9
   ; map /cgi-bin requests to /var/cgi
   cgi = /cgi-bin=%(workdir)/cgi
   ; only .lua script can be executed
   cgi-allowed-ext = .lua
   ; .lua files are executed with the 'lua' command (it avoids the need of giving execute permission to files)
   cgi-helper = .lua=lua
   ; search for index.lua if a directory is requested
   cgi-index = index.lua
   
   
Multiple flask apps in different mountpoints
--------------------------------------------

Let's write three flask apps:

.. code-block:: py

   #app1.py
   from flask import Flask
   app = Flask(__name__)

   @app.route("/")
   def hello():
       return "Hello World! i am app1"
       

.. code-block:: py

   #app2.py
   from flask import Flask
   app = Flask(__name__)

   @app.route("/")
   def hello():
       return "Hello World! i am app2"
       
       
.. code-block:: py

   #app3.py
   from flask import Flask
   app = Flask(__name__)

   @app.route("/")
   def hello():
       return "Hello World! i am app3"

each will be mounted respectively in /app1, /app2, /app3

To mount an application with a specific "key" in uWSGI, you use the --mount option:

```
--mount <mountpoint>=<app>
```

in our case we want to mount 3 python apps, each keyed with what will be the WSGI SCRIPT_NAME variable:

.. code-block :: ini
   
   [uwsgi]
   plugin = python
   mount = /app1=app1.py
   mount = /app2=app2.py
   mount = /app3=app3.py
   ; generally flask apps expose the 'app' callable instead of 'application'
   callable = app

   ; tell uWSGI to rewrite PATH_INFO and SCRIPT_NAME according to mount-points
   manage-script-name = true

   ; bind to a socket
   socket = /var/run/uwsgi.sock



now directly point your webserver.proxy to the instance socket (without doing additional configurations)

Note: by default every app is loaded in a new python interpreter (that means a pretty-well isolated namespace for each app).
If you want all of the app to be loaded in the same python vm, use the --single-interpreter option.

Another note: you may find reference to an obscure "modifier1 30" trick. It is deprecated and extremely ugly. uWSGI is able to rewrite request variables in lot of advanced ways

Final note: by default, the first loaded app is mounted as the "default one". That app will be served when no mountpoint matches.


rbenv on OSX (should work on other platforms too)
-------------------------------------------------

install rbenv

.. code-block:: sh

   brew update
   brew install rbenv ruby-build
   
(do not set the magic line in .bash_profile as described in the classic howto, as we want to not clobber the environment, and allow uWSGI to get rid of it)

get a uWSGI tarball and build the 'nolang' version (it is a monolithic one without language plugins compiled in)

.. code-block:: sh

   wget http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
   tar zxvf uwsgi-latest.tar.gz
   cd uwsgi-xxx
   make nolang
   
now start installing the ruby versions you need

.. code-block:: sh

   rbenv install 1.9.3-p551
   rbenv install 2.1.5
   
and install the gems you need (sinatra in this case):

.. code-block:: sh

   # set the current ruby env
   rbenv local 1.9.3-p551
   # get the path of the gem binary
   rbenv which gem
   # /Users/roberta/.rbenv/versions/1.9.3-p551/bin/gem
   /Users/roberta/.rbenv/versions/1.9.3-p551/bin/gem install sinatra
   # from the uwsgi sources directory, build the rack plugin for 1.9.3-p551, naming it rack_193_plugin.so
   # the trick here is changing PATH to find the right ruby binary during the build procedure
   PATH=/Users/roberta/.rbenv/versions/1.9.3-p551/bin:$PATH ./uwsgi --build-plugin "plugins/rack rack_193"
   # set ruby 2.1.5
   rbenv local 2.1.5
   rbenv which gem
   # /Users/roberta/.rbenv/versions/2.1.5/bin/gem
   /Users/roberta/.rbenv/versions/2.1.5/bin/gem install sinatra
   PATH=/Users/roberta/.rbenv/versions/2.1.5/bin:$PATH ./uwsgi --build-plugin "plugins/rack rack_215"
   
now to switch from one ruby to another, just change the plugin:

.. code-block:: ini

   [uwsgi]
   plugin = rack_193
   rack = config.ru
   http-socket = :9090
   
or 

.. code-block:: ini

   [uwsgi]
   plugin = rack_215
   rack = config.ru
   http-socket = :9090

ensure plugins are stored in the current working directory, or set the plugins-dir directive or specify them with absolute path like

.. code-block:: ini

   [uwsgi]
   plugin = /foobar/rack_215_plugin.so
   rack = config.ru
   http-socket = :9090
