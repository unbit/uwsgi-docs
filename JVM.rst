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
