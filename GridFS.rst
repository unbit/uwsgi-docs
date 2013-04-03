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

