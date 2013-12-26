uWSGI 2.0 (work in progress - updated to -rc1)
==============================================

Important changes
*****************

Dynamic options have been definitely removed as well as the broken_plugins directory

Bugfixes and improvements
*************************

- improved log rotation
- do not rely on unix signals to print request status during harakiri
- added magic vars for uid and gid
- various Lua fixes

New features
************

--attach-daemon2
^^^^^^^^^^^^^^^^

Linux setns() support
^^^^^^^^^^^^^^^^^^^^^

"private" hooks
^^^^^^^^^^^^^^^

Support for yajl library (JSON parser)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Perl spooler support
^^^^^^^^^^^^^^^^^^^^

Gateways can drop privileges
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Subscriptions-governed SNI contexts
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Availability
************
