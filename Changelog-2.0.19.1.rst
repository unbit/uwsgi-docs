uWSGI 2.0.19.1
==============

Released 20200617

Bugfix release


Changes
-------

- Reverted CGI chunked encoding support (7dfe93d961cb83d16b02f18d450a63f3f019a27d), requires better backporting 
- Fixed bug with WSGI responses returning None (#2185, reported by Nico Berlee)


Availability
------------

You can download uWSGI 2.0.19.1 from https://projects.unbit.it/downloads/uwsgi-2.0.19.1.tar.gz
