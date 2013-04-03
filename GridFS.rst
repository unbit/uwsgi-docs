The GridFS plugin
=================

Starting with uWSGI 1.9.5 a "GridFS" plugin is available. It exports both a request handler and an internal routing function.

Its official modifier is '25'. The routing instruction is "gridfs"

The plugin is written in C++

Requirements and install
************************

To build the plugin you need the libmongoclient headers (and the c++ compiler). On a debian-like system you can do

.. code-block:: sh

   apt-get install mongodb-dev g++

A build profile for gridfs is available:

.. code-block:: sh

   UWSGI_PROFILE=gridfs make

Or you can build it as plugin:

.. code-block:: sh

   python uwsgiconfig.py --plugin plugins/gridfs


Standalone quickstart
*********************

This is a standalone config, that blindly maps PATH_INFO to items in the GridFS db named "test":

.. code-block:: ini

   [uwsgi]
   ; you can remove the plugin directive if you are using a uWSGI gridfs monolithic build
   plugin = gridfs
   ; bind to http port 9090
   http-socket = :9090
   ; force the modifier to be the 25th
   http-socket-modifier1 = 25
   ; map gridfs requests to the "test" db
   gridfs-mount = db=test

Supposing you have the myfile.txt file stored in the gridfs as "/myfile.txt", run

.. code-block:: sh

   curl -D /dev/stdout http://localhost:9090/myfile.txt

and you should be able to get it.

The initial slash problem
*************************

Generally the PATH_INFO is prefixed with a '/'. This could cause problems in gridfs path resolutions if you are not storing the items
with absolute path names. You can force the gridfs plugin to skip the first slash:

.. code-block:: ini

   [uwsgi]
   ; you can remove the plugin directive if you are using a uWSGI gridfs monolithic build
   plugin = gridfs
   ; bind to http port 9090
   http-socket = :9090
   ; force the modifier to be the 25th
   http-socket-modifier1 = 25
   ; map gridfs requests to the "test" db
   gridfs-mount = db=test,skip_slash=1

Now instead of searching for /myfile.txt it will search for "myfile.txt"

Multiple mountpoints (and servers)
**********************************

You can mount different gridfs databases under different SCRIPT_NAME (or UWSGI_APPID). If your webserver is able to correctly manage
the SCRIPT_NAME variable you do not need additional setup (other than --gridfs-mount) otherwise remember to add the --manage-script-name option

.. code-block:: ini

   [uwsgi]
   ; you can remove the plugin directive if you are using a uWSGI gridfs monolithic build
   plugin = gridfs
   ; bind to http port 9090
   http-socket = :9090
   ; force the modifier to be the 25th
   http-socket-modifier1 = 25
   ; map gridfs requests to the "test" db
   gridfs-mount = db=test,skip_slash=1
   ; map /foo to db "wolverine" on server 192.168.173.17:4040
   gridfs-mount = mountpoint=/foo,server=192.168.173.17:4040,db=wolverine
   ; map /bar to db "storm" on server 192.168.173.30:4040
   gridfs-mount = mountpoint=/bar,server=192.168.173.30:4040,db=storm
