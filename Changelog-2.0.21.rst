uWSGI 2.0.21
============

Released UNRELEASED

Maintenance release

Changes
-------

- Add PY_SSIZE_T_CLEAN define for Python 3.10 support (Thea Flowers)
- Fix PHP 8 missing arginfo warnings (Дамјан Георгиевски)
- Do not collide with the builtin compile function in uwsgiconfig.py (Jonathan Rosser)
- add uwsgi fork hooks to update internal interpreter state in python plugin (Tahir Butt)
- Properly call `.close()` as mandated by WSGI specs in python plugin (Florian Apolloner)
- Fix compilation with PHP 8.1 (Riccardo Magliocchetti)
- Fix memory corruption for uwsgi_cache_* in php plugin (aszlig)

Availability
------------

You can download uWSGI 2.0.21 from https://projects.unbit.it/downloads/uwsgi-2.0.21.tar.gz
