The uWSGI caching framework
===========================

Caching is one of the key component of a successful webapp.

uWSGI includes an ultra-fast all-in-memory SMP-safe constantly-auto-optimizing caching framework.

The API exposes 6 functions for caching:

* :py:func:`uwsgi.cache_get`
* :py:func:`uwsgi.cache_set`
* :py:func:`uwsgi.cache_update` (since 0.9.8.4)
* :py:func:`uwsgi.cache_del`
* :py:func:`uwsgi.cache_exists`
* :py:func:`uwsgi.cache_clear`

The optional ``cache_server`` argument is a TCP/UNIX socket address.

To enable caching, allocate slots for your items using the ``cache`` option. The following command line would create a cache that can contain at most 1000 items.

.. code-block:: sh

   ./uwsgi --socket 127.0.0.1:3031 --module mysimpleapp --master --processes 4 --cache 1000

To use the cache in your application, 

.. code-block:: python

   uwsgi.cache_set("foo_key", "foo_value") # set a key
   value = uwsgi.cache_get("foo_key") # get a key.


Notes
-----

* ``key`` can be at most 2048 bytes -- that's probably not a problem for most apps.
* Values are put into fixed size blocks in memory. Every item will thus take the same amount of space. The block size is configurable.
* The uWSGI master process will constantly optimize your cache in a way that most requested items are always on the top of the stack. This is still being worked on, but the current implementation is already fast as all hell.
* Caching is completely thread/multiprocess/SMP safe. Writing and deletion will block, though.
* The cache can be accessed via network using the uwsgi protocol modifier 111.
  .. code-block:: py

     # Modifier2: 0: read, 1: write, 2: delete, 3: dict_based
     data = uwsgi.send_message("host", 111, 0, "foo_key")
     data = uwsgi.send_message("host", 111, 3, {"key":"foo_key"})


Persistent storage
------------------

You can store cache data in a backing store file to implement persistence. Simply add the ``cache-store <filename>`` option.
Every kernel will commit data to the disk at a different rate. You can set if/when to force this with ``cache-store-sync <n>``, where ``n`` is the number of master cycles to wait before each disk sync.

Cache sweeper
-------------

Since uWSGI 1.2, cache item expiration is managed by a thread in the :term:`master` process, to reduce the risk of deadlock. This thread can be disabled (making item expiry a no-op) with the ``cache-no-expire`` option.

The frequency of the cache sweeper thread can be set with ``cache-expire-freq <seconds>``. You can make the sweeper log the number of freed items with ``cache-report-freed-items``.

Directly accessing the cache from your web server
-------------------------------------------------

.. code-block:: nginx

   location / {
    uwsgi_pass 127.0.0.1:3031;
    uwsgi_modifier1 111;
    uwsgi_modifier2 3;
    uwsgi_param key $request_uri;
   }

That's it! Nginx would now get HTTP responses from a remote uwsgi protocol compliant server. Although honestly this is not very useful, as if you get a cache miss, you will see a blank page.

A better system, that will fallback to a real uwsgi request would be

.. code-block:: nginx

   location / {
     uwsgi_pass 192.168.173.3:3032;
     uwsgi_modifier1 111;
     uwsgi_modifier2 3;
     uwsgi_param key $request_uri;
     uwsgi_pass_request_headers off;
     error_page 502 504 = @real;
   }

   location @real {
     uwsgi_pass 192.168.173.3:3032;
     uwsgi_modifier1 0;
     uwsgi_modifier2 0;
     include uwsgi_params;
   }
   
Django cache backend
--------------------

If you are running Django, here's a ready-to-use cache backend. Copy the code to a file named :file:`uwsgicache.py`` and put it where your app can load it.

.. code-block:: py

   """uWSGI cache backend"""
   
   from django.core.cache.backends.base import BaseCache, InvalidCacheBackendError
   from django.utils.encoding import smart_unicode, smart_str
   
   try:
       import cPickle as pickle
   except ImportError:
       import pickle
   
   try:
       import uwsgi
   except:
       raise InvalidCacheBackendError("uWSGI cache backend requires you are running under it to have the 'uwsgi' module available")
   
   class UWSGICache(BaseCache):
       def __init__(self, server, params):
           BaseCache.__init__(self, params)
           self._cache = uwsgi
           self._server = server
   
       def exists(self, key):
           return self._cache.cache_exists(smart_str(key), self._server)
   
       def add(self, key, value, timeout=0):
           if self.exists(key):
               return False
           return self.set(key, value, timeout, self._server)
   
       def get(self, key, default=None):
           val = self._cache.cache_get(smart_str(key), self._server)
           if val is None:
               return default
           val = smart_str(val)
           return pickle.loads(val)
   
       def set(self, key, value, timeout=0):
           self._cache.cache_update(smart_str(key), pickle.dumps(value), timeout, self._server)
   
       def delete(self, key):
           self._cache.cache_del(smart_str(key), self._server)
   
       def close(self, **kwargs):
           pass
   
       def clear(self):
           pass
   
   # For backwards compatibility
   class CacheClass(UWSGICache):
       pass

Follow the Django `caching configuration`_ to add the middleware classes, and then configure your cache like this in your settings:

.. code-block:: py

   try:
       import uwsgi
       UWSGI = True
   except:
       UWSGI = False
   
   if UWSGI:
       CACHES = {
           'default': {
               'BACKEND': 'uwsgicache.UWSGICache',
               'OPTIONS': {
                   'MAX_ENTRIES': uwsgi.opt['cache']
               }
           }
       }

       # For Django older than 1.3:
       CACHE_BACKEND = "uwsgicache://" # a unix or tcp socket address, leave empty to use local uwsgi

.. _caching configuration: https://docs.djangoproject.com/en/dev/topics/cache/?from=olddocs#the-per-site-cache