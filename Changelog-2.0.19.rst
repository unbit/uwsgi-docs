uWSGI 2.0.19
============

[UNRELEASED]

Maintenance release


Changes
-------

- Update travis to xenial (Terence D. Honles)
- Fix segfault in logsocket plugin (Riccardo Magliocchetti, #2010)
- Backport Coverity fixes from master (Riccardo Magliocchetti)
- Fix Python 3.7 warnings (Orivej Desh)
- Fix uwsgi.workers() leak in Python plugin (Arne Welzel, #2056)
- Backport redislog plugin 32-bit build fixes (Riccardo Magliocchetti, #1828)
- Fix stack overflow in core/rpc (Nicola Martino)
- Fix build with spaces in the path (Arne Welzel, #1939)
- Add missing initialization for zend_file_handle in php plugin (Arne Welzel)
- Build Python 3.7 and 3.8 plugins in CI (Arne Welzel)
- Add Trove classifiers for Python 3.7 and 3.8 (Hugo)
- Graceful shutdown for vassals (Sponsored by guppyltd.com)
- Improve yaml parsing with libyaml (Arne Welzel, #2097)
- Add smart-daemon2 option to notify daemon of master reloading (Eduardo Felipe Castegnaro)
- Do not chroot multiple times when root (Arne Welzel)
- Support io.BytesIO with wsgi.file_wrapper (Arne Welzel, #1126)
- Add websocket continuation frames support (Timi, #1350)
- Fix compilation with gevent 1.5.0 (Vytautas Liuolia)
- Fix PSGI plugin build with gcc 10 (Jorge Gallegos)
- Get rid of paste.script dependency in pypy/python plugins (Thomas De Schampheleire)
- Improve performance for santitizing file descriptors with cgi plugin (Natanael Copa, #2053)


Availability
------------

You can download uWSGI 2.0.19 from https://projects.unbit.it/downloads/uwsgi-2.0.19.tar.gz
