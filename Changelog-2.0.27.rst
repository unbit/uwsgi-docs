uWSGI 2.0.27
============

Released 20240923

Maintenance release

Changes
-------

- pyuwsgi: avoid interleaving pywsgi threadstate (Anthony Sottile)
- Fix gracefully_kill_them_all with running requests (赵浩彬)
- Fix --catch-exceptions causing a segfault in Python 3.5+ (John Garland)
- plugins/php: Add support for uwsgi.disconnect() function (Joe)
- plugins/python: use PyOS_*Fork stable API functions on 3.7+ (Riccardo Magliocchetti)
- core/uwsgi: set enable threads by default (Riccardo Magliocchetti)
- plugins/python: fix compilation with Python 3.13 (Riccardo Magliocchetti, Ralf Ertzinger)
- use pipe in gracefully_kill() to stop worker loop (Inada Naoki)
- port pypy plugin to python3 (Alexandre Rossi)
- add some integrations tests (Alexandre Rossi)


Availability
------------

You can download uWSGI 2.0.27 from https://files.pythonhosted.org/packages/e1/46/fb08706bc5d922584a5aaed1f73e7a17313310aa34615c74406112ea04a6/uwsgi-2.0.27.tar.gz
