uWSGI 2.0.16
============

[20180210]

Maintenance release

Security
------



Changes
-------

- workaround for the holy allocator for avoiding crashes with newrelic (see Issues notes)
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
- fixed static file serving over https-socket

Availability
------------

You can download uWSGI 2.0.16 from https://projects.unbit.it/downloads/uwsgi-2.0.16.tar.gz
