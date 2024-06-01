uWSGI 2.0.26
============

Released 20240601

Maintenance release

Changes
-------

- apache2/mod_proxy_uwsgi: let httpd handle CL/TE for non-http handlers CVE-2024-24795 (Eric Covener)
- remove race-condition over termination of uWSGI process when using need-app and lazy-apps (Hanan .T)
- fix 32-bit compilation with GCC14 (Rosen Penev)
- uwsgiconfig: get compiler version with -dumpfullversion (Riccardo Magliocchetti)
- Fix uwsgi_regexp_match() with pcre2 (Alexandre Rossi)


Availability
------------

You can download uWSGI 2.0.26 from https://files.pythonhosted.org/packages/3a/7a/4c910bdc9d32640ba89f8d1dc256872c2b5e64830759f7dc346815f5b3b1/uwsgi-2.0.26.tar.gz
