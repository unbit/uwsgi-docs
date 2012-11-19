JVM in the uWSGI server
=======================

.. toctree::

   JWSGI

.. note:: This documentation may be out of date.

Starting from 0.9.7-dev version, a plugin that embeds a Java Virtual Machine in uWSGI is available.

Its main purpose is to allow other plugins (languages) to communicate with Java classes. The first plugin to get JVM support will be Python.

This is the current list of functions that will be exposed:

* uwsgi.jvm.call_static_method("class","method", args, ...)
* uwsgi.jvm.call_method(object,"method", args, ...)
* uwsgi.jvm.string("string")
* uwsgi.jvm.integer(N)
* uwsgi.jvm.array(object, ...)

The ``pyjvm`` plugin is still at early stage of development. The JVM plugin will allow to map string, integers and array to other languages object (in a similar way to the Erlang one).

