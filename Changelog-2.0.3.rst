uWSGI 2.0.3
===========

Changelog 20140317

Bugfixes
********

* fixed spooler 'at' key usage
* fixed a memory and fd leak with on-demand Emperor sokets
* on __APPLE__ use LOG_NOTICE for syslog plugin
* fixed mongrel2 support
* hack for avoiding libmongoclient to crash on broken cursor
* log alarm is now a uwsgi_log)verbose() wrapper
* fixed tuntap router memory corruption
* Set ECDHE curve independently from DHE parameters (Hynek Schlawack)
* do not wait for a whole Emperor cycle before checking for each waitpid
* fix a regression with caller() not indicating the starting *.psgi program (Ævar Arnfjörð Bjarmason)

New features
************

Emperor SIGWINCH and SIGURG
---------------------------

Building plugins on-the-fly from git repositories
-------------------------------------------------

uwsgi.add_var(key, value)
-------------------------

'disableheaders' routing action
-------------------------------

Smarter Emperor on bad conditions
---------------------------------

Availability
************
