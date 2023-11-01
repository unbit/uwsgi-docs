uWSGI 2.0.23
============

Released 20231101

Maintenance release

Changes
-------

- Add support for Python 3.12 (Ralf Ertzinger)
- plugins/php: ini_entries is read-only since PHP 8.3 (Remi Collet)
- Silence glibc warnings against pthread robust mutex functions (Riccardo Magliocchetti)
- Fixup jvm library path detection (Riccardo Magliocchetti)
- Use sysconfig if distutils is not available (Steve Kowalik, Terence D. Honles, Riccardo Magliocchetti)


Availability
------------

You can download uWSGI 2.0.23 from https://files.pythonhosted.org/packages/79/73/b5def500729e134d1cb8dfc334e27fa2e9cfd4e639c1f60c6532d40edaed/uwsgi-2.0.23.tar.gz
