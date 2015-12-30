uWSGI 2.0.12
============

[20151230]

Bugfixes
--------

- 'rpcvar' routing action correctly returns NEXT on empty response
- uwsgiconfig: fix handling of empty keys in python3 (Simone Basso)
- plugins/alarm_speech: fix AppKit spelling to support case-sensitive filesystems (Andrew Janke)
- Fix inheriting INET address 0.0.0.0 (INADA Naoki)
- core/xmlconf: correctly initialize libxml2 (Riccardo Magliocchetti)
- Pass LIBDIR to linker in python plugin (Borys Pierov)
- Platforms-related build fixes for pty, forkptyrouter and mono plugins (Jonas Smedegaard and Riccardo Magliocchetti)

New Features and Backports
--------------------------

The custom worker api
*********************

--wsgi-disable-file-wrapper
***************************

Official PHP 7 support
**********************

uwsgi.spooler_get_task api (Credits: Alexandre Bonnetain)
*********************************************************

--if-hostname-match (Credits: Alexandre Bonnetain)
**************************************************

Availability
------------
