The uWSGI caching framework
===========================

.. note::

  This page is about "new-generation" cache introcued in uWSGI 1.9.
  For old-style cache (now simply named "web caching") check :doc:`WebCaching`

uWSGI includes a very fast all-in-memory, zero-ipc, SMP-safe, constantly-auto-optimizing, highly-tunable key-value store, named
as the "caching framework".

A single uWSGI instance can create an unlimited number of "caches" each one with different setup and purpose.

Creating a "cache"
******************

To create a cache you use the ``--cache2`` option. It takes a dictionary of arguments specifying the cache configuration.

To have a valid cache you to specify its name and the maximum number of items it can contains.

.. code-block:: sh

   uwsgi --cache2 name=mycache,items=100 --socket :3031

this will create a cache named "mycache" with a maximum of 100 items. Each item can be at most 64k.

Configuring the cache (how it works)
************************************

A uWSGI cache works like a filesystem. You have an area for storing keys (metadata) followed by a series of fixed size blocks
in which to store the content of each key.

Another memory area, the "hashtable" is allocated for fast search of keys.

When you request a key, it is firstly hashed over the hashtable. Each hash point to a key in the metadata area. Keys can be linked
to manage hash collisions. Each key has a reference to the block containing its value.

Single block (faster) VS bitmaps (slower)
*****************************************

In the standard configuration ("single block") a key can only map to a single block so if you have a blocksize of 64k, your items
can be at max 64k. That means, an object of 5k will consume 64k of memory.

The advantage of this approach is in its simplicity and speed. The system does not need to scan the memory for free blocks every time
you insert an object in the cache.

If you need a more versatile (but relatively slower) approach, you can enable the "bitmap" mode. Another memory area will be created
containing a map of all of the used and free blocks of the cache. When you insert an item the bitmap is scanned for contiguous free blocks.

Blocks must be contiguous, this could lead to a bit of fragmentation but it is not a big problem as on disk storage (and you can always tune
the blocksize to reduce it)

Persistent storage
******************

You can store cache data in a backing store file to implement persistence.

Thanks to mmap() this is almost transparent to the user.

Obviously do not rely on it for data safety (the disk sync is managed in async way), but only for performance purpose

Network access
**************

All of your caches can be accessed over the network. A request plugin named "cache" (modifier1 111) manages requests
done by external nodes. On a standard onolithic build of uWSGI the cache plugin is always enabled.

The cache plugin works in a full non-blocking way, and it is greenthreads/coroutine friendly so you can use technologies
like gevent or Coro::AnyEvent with it safely.

UDP sync
********

This technique has been inspired by the STUD project, using it for ssl sessions scaling (the same approach can be used with uWSGI SSL/HTTPS routers)

Basically whenever you set/update/delete an item from the cache, the operation is propagated to other remote nodes (via simple udp packets).

This is obviously non-synced so use it only for very specific purposes, like :doc:`SSLScaling`


