SharedArea -- share memory pages between uWSGI components
=========================================================

.. warning::

  SharedArea is a very low-level mechanism.
  For an easier-to-use alternative, see the :doc:`Caching<Caching>` and :doc:`Queue<Queue>` frameworks.
  
.. warning::

  This page refers to "new generation" sharedarea introduced in uWSGI 1.9.21, the older API is no more supported.

The sharedarea subsystem allows you to share pages of memory between your uWSGI components (workers, spoolers, mules, etc.)
in a very fast (and safe) way.

Contrary to the higher-level :doc:`caching framework<Caching>`, sharedarea operations are way faster (a single copy instead of the double, as required by caching) and offers
various optimizations for specific needs.

Each sharedarea (yes, you can have multiple areas) has a size (generally specified in the number of pages), so if you need an 8 KiB shared area on a system with 4 KiB pages, you would use ``sharedarea=2``.

The sharedarea subsystem is fully thread-safe.

Simple option VS keyval
***********************

The sharedarea subsystem exposes (for now) a single option: ``--sharedarea``.

It takes two kinds of arguments: the number of pages (simple approach) or a keyval arg (for advanced tuning).

The following keyval keys are available:

* ``pages`` -- set the number of pages
* ``file`` -- create the sharedarea from a file that will be ``mmap``\ ed
* ``fd`` -- create the sharedarea from a file descriptor that will be ``mmap``\ ed
* ``size`` -- mainly useful with the ``fd`` and ``ptr`` keys to specify the size of the map (can be used as a shortcut to avoid calculation of the ``pages`` value too)
* ``ptr`` -- directly map the area to the specified memory pointer.

The api
*******

The api is pretty big, the sharedarea will be the de-facto toy for writing highly optimized web-apps (expecially for embedded systems).

Most of the documented uses make sense on systems with slow cpus or very few memory

``sharedarea_read(id, pos[, len])`` read 'len' bytes from the specified sharedarea starting from offset 'pos'. If len is not specified the memory will be read til the end (starting from 'pos')

``sharedarea_write(id, pos, string)`` write the specified 'string' (it is language-dependent obviously) to the specified sharedarea at offset 'pos'

``sharedarea_read8|16|32|64(id, pos)`` read a signed integer (8, 16, 32 or 64 bit) from the specified position

``sharedarea_write8|16|32|64(id, pos)`` write a signed integer (8, 16, 32 or 64 bit) to the specified position

``sharedarea_inc8|16|32|64(id, pos)`` increment the signed integer (8, 16, 32 or 64 bit) at the specified position

``sharedarea_dec8|16|32|64(id, pos)`` decrement the signed integer (8, 16, 32 or 64 bit) at the specified position

``sharedarea_wait(id[, freq, timeout])`` wait for modifications to the specified shared area (see below)

Waiting for updates
*******************

One of the most powerful features of sharedareas (compared to caching) is 'waiting for updates'. You worker/thread/async_core can be suspended
until a sharedarea is modified

Technically a milliseconds-resolution timer is triggered, constantly checking for updates (the operation is very fast as the sharedarea object has an update counter, so we only need to check that value for changes)

Optional api
************

The following functions require specific features from the language, so not all of the language plugins are able to support them.

``sharedarea_readfast(id, pos, object, [, len])`` read 'len' bytes from the specified sharedarea starting from offset 'pos' to the specified object. If len is not specified the memory will be read til the end (starting from 'pos').
currently implemented only for perl.

Websockets integration api
**************************

Advanced usage (from C)
***********************
