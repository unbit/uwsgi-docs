uWSGI 2.0.25
============

Released 20240413

Maintenance release

Changes
-------

- Update glusterfs io callback function signature for 6.0 (Ralf Ertzinger)
- Fix default values in help for min-worker-lifetime & legion-skew-tolerance (Thomas Riccardi)
- Fix build regression with gcc < 5 (Riccardo Magliocchetti)
- Add support for building against prcre2. This changes the regexp internal data
  structures (Alexandre Rossi)
- Allow the valgrind generator script to run with a different python version (Wynn Wilkes)
- Fix a potential error with not releasing the gil in uwsgi_python_rpc (Wynn Wilkes)
- Rework threading cancellation handling. This can fix issues with threading, missing
  atexit callbacks and whatnot. (Inada Naoki)

Availability
------------

You can download uWSGI 2.0.25 from https://files.pythonhosted.org/packages/c5/d6/72d625b5664468df51c5a082668b3f127cc0b154f7bb22763ac71b081d6a/uwsgi-2.0.25.tar.gz
