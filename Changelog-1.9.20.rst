uWSGI 1.9.20
============

First round of deprecations and removals for 2.0
************************************************

- The Go plugin is now considere "broken" and has been moved away from the 'plugins' directory. The new blessed way for running Go apps in uWSGI is using the :doc:`GCCGO` plugin

- The --auto-snapshot option has been removed, advanced management of instances now happens via :doc:`MasterFifo`

- The matheval support has been removed, while a generic 'matheval' plugin (for internal routing) is available (but not compiled in by default)

- The 'erlang' and 'pyerl' plugins are broken and has been moved out of the 'plugins' directory. Erlang support will be completely rewritten after 2.0 release

Bugfixes
********

New features
************

Availability
************
