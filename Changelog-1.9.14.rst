uWSGI 1.9.14
============

Changelog [20130720]


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


Breaking News !!!
*****************

Servlet 2.5 support development has just started. The plugin is present in the tree but it is unusable (it is an hardcoded
jsp engine). We expect a beta version after the summer. Obviously we shameless consider :doc:`JWSGI` a better approach than servlet for non-Enterprise people ;)

Availability
************
