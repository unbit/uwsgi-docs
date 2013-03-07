The Clojure/Ring JVM request handler
====================================

Thanks to the JVM pluging available from 1.9, Clojure web app can be run on uWSGI.

The supported webserver-gatway standard is Ring:

https://github.com/ring-clojure/ring

its full spec are available here:

https://github.com/ring-clojure/ring/blob/master/SPEC

A uWSGI build profile name "ring" is available for generating a monolithic build with the jvm plugin and the ring one.

From the uWSGI sources:

.. code-block:: sh

   UWSGI_PROFILE=ring make

The build system will try to detect your JDK installation based on various presets (for example on centos you can yum install 
java-1.6.0-openjdk.x86_64-devel or java-1.7.0-openjdk-devel.x86_64 or on debian/ubuntu 
