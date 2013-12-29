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
- a tons of coverity-governed bugfixes made by Riccardo Magliocchetti

New features
************

--attach-daemon2
^^^^^^^^^^^^^^^^

this is a keyval based option for configuring external daemons.

Updated docs are: :doc:`AttachingDaemons`

Linux setns() support
^^^^^^^^^^^^^^^^^^^^^



"private" hooks
^^^^^^^^^^^^^^^

When uWSGI runs your hooks, it verbosely print the whole hook action line. This could be a security problem
in some scenario (for example when you run initial phases as root user but allows unprivileged access to logs).

Prefixing your action with a '!' will suppress full logging:

.. code-block:: ini

   [uwsgi]
   hook-asap = !exec:my_secret_command

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

uWSGI 2.0 has been released on 20131230 and can be downloaded from:

http://projects.unbit.it/downloads/uwsgi-2.0.tar.gz
