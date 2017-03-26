uWSGI 2.0.15
============

[20170326]

Maintenance release

Changes
-------

- workaround for the cheat allocator for avoiding crashes with newrelic
- avoid time overflow in request logs during (even minimal) clock skew
- fixed python logger with python3
- fixed catch-exceptions with python3
- backported dpn't clone $env->{'psgix.io'} on "PSGI cancel" 

Availability
------------

You can download uWSGI 2.0.15 from https://projects.unbit.it/downloads/uwsgi-2.0.15.tar.gz
