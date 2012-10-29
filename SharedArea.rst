SharedArea -- share data between workers
========================================

.. warning::

  SharedArea is a very low-level mechanism.
  For an easier-to-use alternative, see the :doc:`Caching<Caching>` and :doc:`Queue<Queue>` frameworks.

You can share data between workers (sessions, counters etc. etc.) by enabling the ``sharedarea`` (``-A``) option with the number of pages you want to allocate.

If you need an 8 KiB shared area on a system with 4 KiB pages, you would use ``sharedarea=2``.

The shared data area is then usable through the :ref:`uWSGI API<SharedAreaAPI>`.

This area is completely SMP safe as all operations are governed by a rw_lock.

.. warning::

  The shared area might not be supported under Python 3. It's unclear whether this is true.

.. TODO: Fix the above...