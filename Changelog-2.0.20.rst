uWSGI 2.0.20
============

20211006

Maintenance release

Special Note: this is the last version with GPL2+linking_exception license. Following versions will be under MIT.


Changes
-------

- Switch default python for build to python3 (Riccardo Magliocchetti)
- Add support for PHP 8 (Riccardo Magliocchetti)
- Drop support for PHP < 7 as it is EOL since end of 2018 (Riccardo Magliocchetti)
- Fix segfaults when using --wsgi-env-behavior=holy (Antonio Cuni)
- Replace uwsgi.h system includes in core and proto dirs for Bazel (Serge Bazanski)
- gevent: fix compilation with clang11 (László Károlyi)
- Fix Python 3.9 deprecations warnings (Riccardo Magliocchetti)
- Add trove classifier for Python 3.9 (Adrian)
- Fix message in Log SIGINT/SIGTERM triggered kill_them_all (Delena Malan)
- Support 7 in weekedays as an alias for sunday to match crontab behaviour (Riccardo Magliocchetti)
- Document http-timeout default of 60 seconds (Etienne H)
- Add option to override python sys.executable using py-executable config
- Allow specifying an iteration to uwsgi::add_rb_timer (Luciano Rocha)
- Allow to compile with Python versions with minor version with 2+ digits (Cyrille Pontvieux)
- Take into account new naming for LIBPL since python 3.6 (ilrico)
- Official support for Python 3.10

Availability
------------

You can download uWSGI 2.0.20 from https://projects.unbit.it/downloads/uwsgi-2.0.20.tar.gz
