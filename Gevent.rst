The Gevent loop engine
======================

`Gevent`_ is an amazing non-blocking Python network library built on top of ``libev`` and ``greenlet``.

Even if uWSGI supports Greenlet as suspend-resume/greenthread/coroutine library, it requires a lot of effort and code modifications to work with gevent.

The gevent plugin requires gevent 1.0.0 and :doc:`Async<Async>` mode.

.. _Gevent: http://www.gevent.org

Notes
-----

* The :doc:`SignalFramework` is fully working with Gevent mode. Each handler will be executed in a dedicated greenlet. Look at :file:`tests/ugevent.py` for an example.
* uWSGI multithread mode (``threads`` option) will not work with Gevent. Running Python threads in your apps is supported.
* Mixing uWSGI's Async API with gevent's is **EXPLICITLY FORBIDDEN**.
* Currently you cannot run uWSGI + gevent on more than one socket. If you need multiple sockets, simply spawn additional uWSGI instances.
* :doc:`Mongrel2<Mongrel2>` and its protocol handler are not supported.

Building the plugin
-------------------

A 'gevent' build profile can be found in the :file:`buildconf` directory.

.. code-block:: sh

  python uwsgiconfig --build gevent
  # or...
  UWSGI_PROFILE=gevent make
  # or...
  UWSGI_PROFILE=gevent pip install hg+http://projects.unbit.it/hg/uwsgi
  # or...
  python uwsgiconfig --plugin plugins/gevent # external plugin

Running uWSGI in gevent mode
----------------------------

.. code-block:: sh

  uwsgi --loop gevent --socket :3031 --module myapp --async 100
  # or if built as an external plugin,
  uwsgi --plugins gevent --loop gevent --socket :3031 --module myapp --async 100

Set the ``--async`` value to the maximum number of concurrent connections you want to accept.

A crazy example
---------------

This example shows how to sleep in a request, how to make asynchronous network requests and how to continue doing logic after a request has been closed.

.. code-block:: python

  import gevent
  import gevent.socket
  
  def bg_task():
      for i in range(1,10):
          print "background task", i
          gevent.sleep(2)
  
  def long_task():
      for i in range(1,10):
          print i
          gevent.sleep()
  
  def application(e, sr):
      sr('200 OK', [('Content-Type','text/html')])
      t = gevent.spawn(long_task)
      t.join()
      yield "sleeping for 3 seconds...<br/>"
      gevent.sleep(3)
      yield "done<br>"
      yield "getting some ips...<br/>"
      urls = ['www.google.com', 'www.example.com', 'www.python.org', 'projects.unbit.it']
      jobs = [gevent.spawn(gevent.socket.gethostbyname, url) for url in urls]
      gevent.joinall(jobs, timeout=2)
  
      for j in jobs:
          yield "ip = %s<br/>" % j.value
  
      gevent.spawn(bg_task) # this task will go on after request end

Streaming
---------

* If you're testing a WSGI application that generates a stream of data, you should know that ``curl`` by default buffers data until a newline. So make sure you either disable curl's buffering with ``-N`` or have regular newlines in your output.
* If you are using Nginx in front of uWSGI and wish to stream data from your app, you'll probably want to disable Nginx's buffering.
  
  .. code-block:: nginx
  
    uwsgi_buffering off;
