uWSGI 2.0.16
============

[20180210]

Maintenance release

Security
------

- [CVE-2018-6758] Stack-based buffer overflow in core/utils.c:uwsgi_expand_path()

Changes
-------

- Add new `millis` to logging format.
- Fix scale of sleeps in emperor.
- Support configuring the depth of SSL/TLS verification.
- Added new metric `total_time_running`.
- Back-ported HTTP/1.1 support from 2.1
- Add support for Brotli (.br) with `--static-gzip`
- FastRouter / HTTP Router can now have a 'fallback' key configured.
- HTTP Router now supports `post-buffer`, just like FastRouter.
- Fix support for IPv6 addresses.
- Fix handling of `env` in embedded dict in Python plugin (could cause segfaults in single thread mode).
- Mules can now return a result code to indicate success or failure.


Availability
------------

You can download uWSGI 2.0.16 from https://projects.unbit.it/downloads/uwsgi-2.0.16.tar.gz
