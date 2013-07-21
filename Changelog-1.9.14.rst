uWSGI 1.9.14
============

Changelog [20130721]


Bugfixes
********

- fixed python modifier1 management (was hardcoded to 0)
- fixed url decoding in http and http-socket (it now supports lowercase hex)
- more user-friendly error message for undeletable unix sockets
- fixed --http-auto-chunked in http 1.1 keepalive mode (André Cruz)
- fixed python wheel support (Fraser Nevett)
- fixed --safe-fd (was not correctly honoured by the Emperor)
- fixed ruby 2.x reloading
- improved support for OSX Tiger (yes, OSX 10.4)
- better computation of listen queue load
- fixed v8 build on OSX
- fixed pypy rpc
- improved chunked api performance
- fixed latin1 encoding with python3
- fixed --spooler-ordered (Roberto Leandrini)
- fixed php status line reported in request logs


New features
************

Ruby 1.9.x/2.x native threads support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ruby 1.9 (mri) introduced native threads support (very similar to the CPython ones, governed by a global lock named GVL).

For various reasons (check the comments on top of the source plugin) the ruby threads support in uWSGI has been implemented as a "loop engine plugin".

You need to build the "rbthreads" plugin (it is automatic when using the 'ruby2' build profile) and enable it with '--rbthreads'

The gem script has been extended, automatically selecting the 'ruby2' build profile when a ruby >= 1.9 is detected (this should make the life easier for Heroku users)

Rails4 is the first Ruby on Rails version supporting and blessing threads (in 3.x you need to explicitely enable support). You can use
multiple threads in Rails4 only when in "production" mode, otherwise your app will deadlock after the first request.

An example config:

.. code-block:: ini

   [uwsgi]
   plugins = rack,rbthreads
   master = true
   ; spawn 2 processes
   processes = 2
   ; spawn 8 threads
   threads = 8
   ; enable ruby threads
   rbthreads = true
   ; load the Rack app
   rack = config.ru
   ; bind to an http port
   http-socket = :9090
   http-socket-modifier1 = 7
   
it will generate a total of 16 threads

Filesystem monitoring interface (fsmon)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

uClibc support
^^^^^^^^^^^^^^

Lua 5.2 support
^^^^^^^^^^^^^^^

setscheme, setdocroot
^^^^^^^^^^^^^^^^^^^^^

sendfile, fastfile
^^^^^^^^^^^^^^^^^^

--reload-on-fd and --brutal-reload-on-fd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Spooler improvements
^^^^^^^^^^^^^^^^^^^^

Author: Roberto Leandrini

--emperor-nofollow
^^^^^^^^^^^^^^^^^^

daemontools envdir support
^^^^^^^^^^^^^^^^^^^^^^^^^^

xmldir improvements
^^^^^^^^^^^^^^^^^^^

Author: Guido Berhoerster


Breaking News !!!
*****************

Servlet 2.5 support development has just started. The plugin is present in the tree but it is unusable (it is an hardcoded
jsp engine). We expect a beta version after the summer. Obviously we shameless consider :doc:`JWSGI` a better approach than servlet for non-Enterprise people ;)

Availability
************
