uWSGI 1.9.11
============

Changelog [20130526]

Bugfixes
********

- fixed python3 stdout/stderr buffering
- fixed mule messages (@mulefunc is now reliable)
- fixed SCRIPT_NAME handling in dynamic mode
- fixed X-Sendfile with gzip static mode
- fixed cache item max size with custom blocksize
- fixed cache paths handling

New features
************

The new high-performance PyPy plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Credits: Maciej Fijalkowski

We are pleased to announce the availability of the new PyPy plugin.

PyPy team has been great in helping us. We hope the uWSGI integration (that exposed new challenges to the PyPy project)
will help PyPy becaming better and better.

Official docs: :doc:`PyPy`

Cron improvements
^^^^^^^^^^^^^^^^^

Credits: Łukasz Mierzwa

unique crons
------------

You can now avoid overlapping crons. The uWSGI master will track death of a single task, and until its death the same cron
will not be triggered:

.. code-block:: ini

   [uwsgi]
   unique-cron = -1 -1 -1 -1 -1 my_script.sh

cron2 syntax
------------

A keyval variant of the --cron option is now available:

.. code-block:: ini

   [uwsgi]
   cron2 = minute=39,hour=23,month=-1,week=-1,day=-1,unique=1,legion=foobar,harakiri=30
harakiri cron
-------------

When using the cron2 option you are allowed to set an harakiri for a cron task. Just add harakiri=n to the options

Support for GNU Hurd
^^^^^^^^^^^^^^^^^^^^

Debian GNU/Hurd has been recently released. uWSGI 1.9.11 can be built over it. Very few tests have been made.

The memory offload engine
^^^^^^^^^^^^^^^^^^^^^^^^^

Idea: Stefano Brentegani

When serving content from the cache, a worker could be blocked during transfer from memory to the socket.

A new offload engine named "memory" allows to offload memory transfers. The cache router automatically support it,
we will add support for more areas soon.

To enable it just add --offload-threads <n>

New Websockets chat example
^^^^^^^^^^^^^^^^^^^^^^^^^^^

An example websocket chat using redis have been added to the repository:

https://github.com/unbit/uwsgi/blob/master/tests/websockets_chat.py

Error routes
^^^^^^^^^^^^

You can now define a routing table to be executed as soon as you set the HTTP status code in your plugin.

This allows you to completely modify the response (this is useful for custom error codes)

All of the routing standard options are available (included labels) plus an optimized ``error-route-status``
mathing a specific HTTP status code:

.. code-block:: ini

   [uwsgi]
   error-route-status = 502 redirect:http://unbit.it

Support for corner case usage in wsgi.file_wrapper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Generally wsgi.file_wrapper callable expects a file-like object. PEP 333/3333 report a special pattern when the object
is not a file (call read() untile the object is consumed). uWSGI now supports this pattern (even if in a hacky way)

HTTP/HTTPS router keepalive improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Credits: André Cruz

When using --http-keepalive you can now hold the connection open even if the request has a body


The harakiri routing action
^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can now set a harakiri tmer for each request using internal routing:

.. code-block:: ini

   [uwsgi]
   ; set harakiri to 30 seconds for request starting with /slow
   route = ^/slow harakiri:30

RPC wrappers
^^^^^^^^^^^^

The rpc plugin has been extended to allows interoperation with other standards.

Currently an HTTP simple wrapper and the xmlrpc one are exposed.

The HTTP simple wrapper works by parsing the PATH_INFO.

A /foo/bar/test call will result in

uwsgi.rpc('foo', 'bar', 'test')

To enable HTTP simple mode just call/set the modifier2 to '2':

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   http-socket-modifier1 = 173
   http-socket-modifier2 = 2
   ; load the rpc code
   import = myrpcfuncs.py
   
or (to have more control)

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   route-run = uwsgi:,173,2
   ; load the rpc code
   import = myrpcfuncs.py


The xmlrpc wrapper works in the same way (but it uses the modifier2 '3'). It requires a libxml2-enabled build of uWSGI:

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   route-run = uwsgi:,173,3
   ; load the rpc code
   import = myrpcfuncs.py
   
just call it:

.. code-block:: python

   proxy = xmlrpclib.ServerProxy("http://localhost:9090')
   proxy.hello('foo','bar','test') 
   


   
you can combine multiple wrappers using routing:

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   ; /xml force xmlrpc wrapper
   route = ^/xml uwsgi:,173,3
   ; fallback to HTTP simple
   route-if-not = startswith:${PATH_INFO};/xml uwsgi:,173,2
   ; load the rpc code
   import = myrpcfuncs.py


Availability
************

uWSGI 1.9.11 will be available since 20130526 at:

http://projects.unbit.it/downloads/uwsgi-1.9.11.tar.gz
