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


Availability
************
