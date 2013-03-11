Changelog-2.0
=============

This is a memo for what we plan to include in uWSGI 2.0 (LTS)

Metric subsystem
****************

think about persistent storage


Storage subsystem
*****************


Better Erlang integration
*************************

remove dependancies with libei

Corerouters backup nodes
************************

On-demand threading mode
************************

Instead of pre-spawning threads in each worker, just spawn a single one that will generate a new one
at each request.

Emperor binary patching
***********************

