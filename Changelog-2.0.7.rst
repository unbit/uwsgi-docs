uWSGI 2.0.7
===========

Changelog [20140905]

Bugfixes
********

- fixed counters in statsd plugin (Joshua C. Forest)
- fixed caching in php plugin (Andrew Bevitt)
- fixed management of system users starting with a number
- fixed request body readline using memmove instead of memcpy (Andrew Wason)
- ignore "user" namespace in setns (still a source of problems)
- fixed Python3 rpc bytes/string mess (result: we support both)
- do not destroy the Emperor on failed mount hooks
- fixed symbol lookup error in the Mono plugin on OS X (Ventero)
- fixed fastcgi and scgi protocols error when out of buffer happens
- fixed solaris/smartos I/O management
- fixed 2 memory leaks in the rpc subsystem (Riccardo Magliocchetti)
- fixed raods plugin PUT method (Martin Mlynář)
- fixed multiple python mountpoints with multiple threads in cow mode
- stats UNIX socket is now deleted by vacuum
- fixed off-by-one corruption in cache LRU mode
- force single-cpu build in cygwin (Guido Notari)


New Features and improvements
*****************************

allow calling the spooler from every cpython context
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

At Europython 2014, Ultrabug (a uWSGI contributor and packager) asked for the possibility to spool tasks directly from a greenlet.

Done.

store_delete cache2 option
^^^^^^^^^^^^^^^^^^^^^^^^^^

Author: goir

The store_delete flag of the --cache2 option, allows you to force the cache engine to automatically remove an invalid
backing store file.

file logger rotation
^^^^^^^^^^^^^^^^^^^^

Author: Riccardo Magliocchetti

The `file` logger has been extended to allow the use of rotation (the same system used by the non-pluggable --logto):

https://github.com/unbit/uwsgi/commit/0324e5965c360dccfb873ffe351dec88ddab59c5

vassals plugin hooks
^^^^^^^^^^^^^^^^^^^^



Broodlord improvements
^^^^^^^^^^^^^^^^^^^^^^

Availability
************
