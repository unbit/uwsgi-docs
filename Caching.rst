The uWSGI caching framework
===========================

.. note::

  This page is about "new-generation" cache introduced in uWSGI 1.9.
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


--cache2 options
****************

This is the list of all of the options (and their aliases) of ``--cache2``

name
^^^^

set the name of the cache (must be unique in an instance)

max-items || maxitems || items
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

set the maximum number of cache items

blocksize
^^^^^^^^^

set the size (in bytes) of a single block

blocks
^^^^^^

set the number of blocks in the cache. Useful only in bitmap mode, otherwise the block numbers is equal to
the maximum number of items.

hash
^^^^

set the hash algorithm used in the hahstable. Currently available "djb33x" (default) and "murmur2"

hashsize || hash_size
^^^^^^^^^^^^^^^^^^^^^

this is the size of the hashtable (in bytes). Generally 65536 (the default) is a good value. Change it only if you know what you are doing
(or if you have a lot of collissions in your cache)

keysize || key_size
^^^^^^^^^^^^^^^^^^^

set the maximum size of a key, in bytes (default 2048)

store
^^^^^

set the filename for the persistent storage (if it not exists, the system assumes an empty cache and the file will be created)

store_sync || storesync
^^^^^^^^^^^^^^^^^^^^^^^

set the number of seconds after which call msync() (to flush memory cache on disk when in persistent mode).

By default it is disabled leaving the job to the kernel.

node || nodes
^^^^^^^^^^^^^

a semicolon separated list of udp server that will receive udp cache updates

sync
^^^^

a semicolon separated list of uwsgi addresses at which the cache subsystem will connect to for getting a full dump
of the cache. It can be used for initial cache synchronization. The first node sending a valid dump will stop the procedure.

udp || udp_servers || udp_server || udpserver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

a semicolon separated list of udp addresses on which to bind the cache (waiting for udp updates)

bitmap
^^^^^^

set it to 1, to enable bitmap mode

Accessing the cache from your applications using the cache api
*************************************************************

You can obviously access the various cache in your instance (or the one on remote instances) using the cache api.

Currently the following functions are exposed (each language can name them a bit differently from the standard)

 * cache_get(key[,cache])
 * cache_set(key,value[,expires,cache])
 * cache_update(key,value[,expires,cache])
 * cache_exists(key[,cache])
 * cache_del(key[,cache])
 * cache_clear([cache])

If the language/platform calling the cache api differentiate between strings and bytes (like python3 and java) you have to
assumes that keys are string and values are bytes (or bytearray in the java way). Otherwise keys and values are both strings
(without specific encoding, as internally the cache values and keys are simple binary blobs)

The expires argument (default to 0) is the number of seconds after the object is no more valid (and will be removed by the cache sweeper, see below)

The cache argument is the so called "magic identifier".

Its syntax is the following:

cache[@node]

So to operate on the cache "mycache" you can simply set it as "mycache", while to operate on "yourcache" on the uWSGI server at 192.168.173.22 port 4040 the value will be
yourcache@192.168.173.22:4040

An empty cache value (the default) means the default cache (generally the first initialized).

All of the network operations are transparent and fully non-blocking (and threads/greenthreads friendly)


Web caching
***********

In its first incarnation the uWSGI caching framework was meant only for caching of web pages. That old system
has been rebuilt on top of the new one. It is now named as :doc:`WebCaching`
