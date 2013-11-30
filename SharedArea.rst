SharedArea -- share memory pages between uWSGI components
=========================================================

.. warning::

  SharedArea is a very low-level mechanism.
  For an easier-to-use alternative, see the :doc:`Caching<Caching>` and :doc:`Queue<Queue>` frameworks.
  
.. warning::

  This page refers to "new generation" sharedarea introduced in uWSGI 1.9.21, the older api is no more supported

The sharedarea subsystem allows you to shares pages of memory between your uWSGI componenets (workers, spoolers, mules...)
in a very fast (and safe) way.

Contrary to the higher level :doc:`Caching` sharedarea operations are way faster (a single copy instead of the double one required by caching) and offers
various optimizations for specific needs.

Each sharedarea (yes you can have multiple areas) has a size (generally specified in the number of pages), so if you need an 8 KiB shared area on a system with 4 KiB pages, you would use ``sharedarea=2``.


The sharedarea subsystem is fully threadsafe

Simple option VS keyval
***********************

The sharedarea subsystem exposes (for now) a single option: ``--sharedarea``

It takes two kind of arguments: the number of pages (simple approach) or a keyval arg for advanced tuning

The following keyval keys are available:

``pages`` set the number of pages

``file`` create the sharedarea from a file that will be mmap()'ed

``fd`` create the sharedarea from a file descriptor that will be mmap()'ed

``size`` mainly useful with the ``fd`` and ``ptr`` keys to specify the size of the map (can be used as a shortcut for avoiding to compute the ``pages`` value too)

``ptr`` directly map the area to the specified memory pointer
