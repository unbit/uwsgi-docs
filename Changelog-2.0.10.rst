uWSGI 2.0.10
============

[20150317]

Bugfixes
--------

* Don't lower security standards with gcc 4.9 (Riccardo Magliocchetti)
* Perl/PSGI make sure that at least two params are passed to xs_input_seek (Ivan Kruglov)
* Per/PSGI fixed multiple interpreters usage
* spooler: fixed scandir usage
* fixed exception handler arguments management
* fixed 'log-master' + 'daemonize2' disables all logging
* fixed http Range header management


New Features
------------

safeexec hook
**************

backported --emperor-wrapper-fallback and --emperor-wraper-override
*******************************************************************

added support for UNIX sockets to rsyslog
*****************************************


Availability
------------

You can download uWSGI 2.0.10 from

http://projects.unbit.it/downloads/uwsgi-2.0.10.tar.gz
