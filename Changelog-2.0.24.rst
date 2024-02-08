uWSGI 2.0.24
============

Released 20240208

Maintenance release

Changes
-------

- properly init cache for purge_lru (Alexandre Rossi)
- fix linking with php8 (Remi Collet)
- remove unused libraries to fix compilation (László Károlyi)
- fix function parameter type to avoid overflow in harakiri (Shai Bentov)
- fix socket queue stats for ipv6 (Riccardo Magliocchetti)
- fixup -Wformat-signedness warnings (Riccardo Magliocchetti)
- Avoid strncpy from null in pyloader (Ben Kallus)
- add clang to compile test matrix in ci (Riccardo Magliocchetti)

Availability
------------

You can download uWSGI 2.0.24 from https://files.pythonhosted.org/packages/1b/ed/136698c76722268569eac4e48ab90f3ced8b8035e414a8290cb935c40c16/uwsgi-2.0.24.tar.gz
