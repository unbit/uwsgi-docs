uWSGI 1.9.13
============

This is a work in progress

Bugfixes
^^^^^^^^

- Fixed a corner case bug when response offloading is enabled, but no request plugin is loaded
- Fixed harakiri routing when multiple rules are in place (return NEXT instead of CONTINUE)

New features
^^^^^^^^^^^^

PyPy performance and features improvents
****************************************

Chunked input api
*****************

Toward better third-party plugins management: the --dot-h option
****************************************************************

setmethod routing action
************************

UWSGI_INCLUDES
**************
