uWSGI 1.9.11
============

Changelog

Bugfixes
********

- fixed python3 stdout/stderr buffering
- fixed mule messages (@mulefunc is now reliable)
- fixed SCRIPT_NAME handling in dynamic mode

New features
************

The new high-performance PyPy plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

We are pleased to announce the availability of the new PyPy plugin.

PyPy team has been great in helping us. We hope the uWSGI integration (that exposed new challenges to the PyPy project)
will help PyPy becaming better and better.

Official docs: :doc:`PyPy`

Cron improvements
^^^^^^^^^^^^^^^^^

unique crons

cron2 syntax

harakiri cron

Support for GNU Hurd
^^^^^^^^^^^^^^^^^^^^

Error routes
^^^^^^^^^^^^

Support for corner case usage in wsgi.file_wrapper
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

HTTP/HTTPS router keepalive improvements
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

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
