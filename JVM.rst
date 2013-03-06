JVM in the uWSGI server (updated to 1.9)
========================================

.. toctree::

   Clojure/Ring
   JWSGI


Starting from uWSGI 1.9, you can have a full, thread-safe and versatile JVM embedded in the core.

All of the plugins can call JVM functions (written in java, jruby, jython, clojure, whatever the jvm support...) 
via the :doc:`RPC subsystem<RPC>` or using uWSGI :doc:`Signals`

The JVM plugin itself can implement request handlers to host JVM-based web applications. Currently JWSGI and Ring (Clojure)
apps are supported. A long-term goal is supporting servlet, but it will require heavy sponsorship and funding (feel free to ask
for more inforomation about the project at info@unbit.it)

Building the JVM support
************************

First of all, be sure to have a full JDK distibution installed.

The uWSGI build system will try to detect common JDK setup (debian,ubuntu,centos, OSX...), but if it is not able
to find a JDK installation it will need infos from the user (see below).

To build the JVM plugin simply run:

.. code-block:: sh

   python uwsgiconfig --plugin plugins/jvm default

change 'default', if needed, with your alternative build profile. FOr example if you have a Perl/PSGI monolithic build
just run

.. code-block:: sh

   python uwsgiconfig --plugin plugins/jvm psgi

or for a fully-modular build

.. code-block:: sh

   python uwsgiconfig --plugin plugins/jvm core

If all goes well the jvm_plugin will be built.

If the build system cannot find a JDK installation you will ned to specify the path of the headers directory (the directory containing the jni.h file)
and the lib directory (the directory containing libjvm.so).

As an example, if jni.h is in /opt/java/includes and libjvm.so is in /opt/java/lib/jvm/i386, run the build system in that way:

.. code-block:: sh

   UWSGICONFIG_JVM_INCPATH=/opt/java/includes UWSGICONFIG_JVM_LIBPATH=/opt/java/lib/jvm/i386 python uwsgiconfig --plugin plugins/jvm


After a successfull build, you will get the path of the uwsgi.jar file.

That jarball containes classes to access the uWSGI api, and you should copy it in your CLASSPATH (or manually loading it from uWSGI)

Exposing functions via the RPC subsystem
****************************************

In this example we will export a "hello" java function (obviously returning a string) and we will call it
from a python WSGI application.

This is our base configuration (we assume a modular build)

.. code-block:: ini

   [uwsgi]
   plugins = python,jvm
   http = :9090
   wsgi-file = myapp.py
   jvm-classpath = /opt/uwsgi/lib/uwsgi.jar

The ``jvm-classpath`` is an option exported by the JVM plugin that allows you to add directories or jarfile to your classpath.

You can specify all of the ``jvm-classpath`` options you need

Here we are manually adding uwsgi.jar as we did not copied it in our CLASSPATH

This is our WSGI example script

.. code-block:: py

   import uwsgi
   
   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       yield "<h1>"
       yield uwsgi.call('hello')
       yield "</h1>"

here we use uwsgi.call (instead of uwsgi.rpc) as a shortcut (little performance gain in options parsing)


