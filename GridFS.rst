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
   ; force management of the SCRIPT_NAME variable
   manage-script-name = true

.. code-block:: sh

    curl -D /dev/stdout http://localhost:9090/myfile.txt
    curl -D /dev/stdout http://localhost:9090/foo/myfile.txt
    curl -D /dev/stdout http://localhost:9090/bar/myfile.txt

each request will map to a different gridfs server

Replica sets
************

If you are using MonogDB/GridFS in production environments, it is very probably you are using a replica set.

You can use replica set in your uWSGI config with this syntax:

<replica>server1,server2,serverN...

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   gridfs-mount = server=rs0/ubuntu64.local\,raring64.local\,mrspurr-2.local,db=test

pay attention to the backslashes used to escape the server list.

Prefixes
********

As well as removing the initial slash, you may need to prefix each item name:

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   gridfs-mount = server=rs0/ubuntu64.local\,raring64.local\,mrspurr-2.local,db=test,prefix=/foobar___

A request for /test.txt will be mapped to /foobar___/test.txt

while 

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   gridfs-mount = server=rs0/ubuntu64.local\,raring64.local\,mrspurr-2.local,db=test,prefix=/foobar___,skip_slash=1

will map to /foobar___test.txt

Mime types and filenames
************************

By default the mime type of the file is derived from the filename stored in GridFS. This filename could not map to the effectively
requested uri or you may not want to set a content_type for you response (or allows other system to set it).

If you want to disable mime type generation just add no_mime=1 to your options:


.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   gridfs-mount = server=ubuntu64.local,db=test,skip_slash=1,no_mime=1

If you want your response to set the filename using the original value (the one stored in GridFS) add orig_filename=1

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   gridfs-mount = server=ubuntu64.local,db=test,skip_slash=1,no_mime=1,orig_filename=1

Timeouts
********

You can set the timeout of the low-level mongodb operations adding timeout=N to the gridfs options:

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   ; set a 3 seconds timeout
   gridfs-mount = server=ubuntu64.local,db=test,skip_slash=1,timeout=3

MD5 and ETag headers
********************

GridFS stores an MD5 hash of each file.

You can add such info to your response headers both as ETag (md5 in hex format) or Content-MD5 (in base64).

Use etag=1 for adding ETag header and md5=1 for adding Content-MD5.

You can add both headers to the response:

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   ; set a 3 seconds timeout
   gridfs-mount = server=ubuntu64.local,db=test,skip_slash=1,timeout=3,etag=1,md5=1

Multithreading
**************

The plugin is fully threadsafe, so consider using multiple threads for improving concurrency:

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 25
   ; set a 3 seconds timeout
   gridfs-mount = server=ubuntu64.local,db=test,skip_slash=1,timeout=3,etag=1,md5=1
   master = true
   processes = 2
   threads = 8

This will spawn 2 processes (monitored by the master) with 8 threads each (for a total of 16 threads)

Combining with Nginx
********************

This is not different from the other plugins:

.. code-block:: c

   location / {
       include uwsgi_params;
       uwsgi_pass 127.0.0.1:3031;
       uwsgi_modifier1 25;
   }

just be sure to set the uwsgi_modifier1 value.

.. code-block:: ini

   [uwsgi]
   socket = 127.0.0.1:3031
   gridfs-mount = server=ubuntu64.local,db=test,skip_slash=1,timeout=3,etag=1,md5=1
   master = true
   processes = 2
   threads = 8

The 'gridfs' internal routing action
************************************

Notes
*****

