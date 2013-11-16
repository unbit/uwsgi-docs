The gccgo plugin
================

uWSGI 1.9.20 officially substituted the old :doc:`Go` plugin with a new one based on gccgo.

The usage of gccgo allows fore features and better integration with the uWSGI deployment styles.

A version of the gcc suite >= 4.8 is expected (and strongly suggested)

How it works
************

when the plugin is enabled a new go runtime is initialized after each fork()

if a main Go function is available in the process address space it will be executed in the Go runtime, otherwise to control
goes back to the uWSGI loop engine.

Building the plugin
*******************

The first app
*************


Shared libraries VS monolithic binaries
***************************************

Goroutines
**********

uWSGI API
*********

Notes
*****
