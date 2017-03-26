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
- backported "don't clone $env->{'psgix.io'} on 'PSGI cancel'"
- added support for authentication in the redis logger
- added the spinningfifo action hook to the core
- fixed compilation with php 7.1 (Дамјан Георгиевски)
- correctly returns error code 22 in lazy_apps + master_mode
- fixed compilation for OpenSSL 1.1 (Riccardo Magliocchetti)
- Add a --skip-atexit-teardown option to skip perl/python teardown (Ævar Arnfjörð Bjarmason)

Availability
------------

You can download uWSGI 2.0.15 from https://projects.unbit.it/downloads/uwsgi-2.0.15.tar.gz
