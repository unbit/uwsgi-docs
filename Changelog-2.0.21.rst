uWSGI 2.0.21
============

Released 20221024

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
- Cleanup usage of threading.current_thread (Hugo van Kemenade)
- Fix concurrency issues on build (Peter Law)
- Fix compilation on MacOS (Shachar Itzhaky)
- Fix segfault from gevent switch (Gavin Jeong)
- Fix php-app for PHP 8.1 (cuchac)
- make dev version PEP-0440 compliant (joshua.biagio)
- Add Python 3.11 support (Victor Stinner)
- Ensure to link against rt when statically linking the python plugin to libpython (Denis Dowling)
- Refactor CI to run tests in parallel (Nicola Martino)
- Add missing parens in plugins/coroae/uwsgiconfig.py (Eleksir)

Availability
------------

You can download uWSGI 2.0.21 from `here https://files.pythonhosted.org/packages/b3/8e/b4fb9f793745afd6afcc0d2443d5626132e5d3540de98f28a8b8f5c753f9/uwsgi-2.0.21.tar.gz`_
