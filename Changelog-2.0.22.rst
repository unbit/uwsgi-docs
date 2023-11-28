uWSGI 2.0.22
============

Released 20230727

Maintenance release

Changes
-------

- Add graceful harakiri to give more slack to workers in order to do cleanup actions (Filipe Felisbino)
  The following options have been added:

  - `harakiri-graceful-timeout` to control the timeout for the worker to attempt a graceful shutdown
  - `harakiri-graceful-signal`, to choose which signal to use for graceful harakiri (default: SIGTERM)
  - `harakiri-queue-threshold` in order to trigger harakiri only when the listen queue crosses a threshold
- plugins/php: Fix PHP 8.2 compilation (Alexandre Rossi)
- plugins/python: Use "backslashreplace" on stderr initialization (Nicolas Evrard)
- Fix typo (Young Ziyi)
- Fix use after free with DEBUG (Alexandre Rossi)
- apache2/mod_proxy_uwsgi: stricter backend HTTP response parsing/validation (Eric Covener, via Freexian)
- ci: update to ubuntu 20.04 since 18.04 is unsupported (Riccardo Magliocchetti)
- plugins/rack: fix compilation with Ruby 3.1, this breaks compilation for Ruby < 2.x (Lalufu, Riccardo Magliocchetti)


Availability
------------

You can download uWSGI 2.0.22 from https://files.pythonhosted.org/packages/a7/4e/c4d5559b3504bb65175a759392b03cac04b8771e9a9b14811adf1151f02f/uwsgi-2.0.22.tar.gz
