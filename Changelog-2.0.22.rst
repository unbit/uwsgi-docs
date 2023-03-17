uWSGI 2.0.22
============

Released unreleased

Maintenance release

Changes
-------

- Add graceful harakiri to give more slack to workers in order to do cleanup actions (Filipe Felisbino)
  The following options have been added:

  - `harakiri-graceful-timeout` to control the timeout for the worker to attempt a graceful shutdown
  - `harakiri-graceful-signal`, to choose which signal to use for graceful harakiri (default: SIGTERM)
  - `harakiri-graceful-queue-threshold` in order to trigger harakiri only when the listen queue crosses a threshold
- plugins/php: Fix PHP 8.2 compilation (Alexandre Rossi)
- plugins/python: Use "backslashreplace" on stderr initialization (Nicolas Evrard)

Availability
------------

You can download uWSGI 2.0.22 from 
