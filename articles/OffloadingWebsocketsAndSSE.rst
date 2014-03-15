Offloading Websockets and Server-Sent Events AKA "Combine them with Django safely"
==================================================================================

Author: Roberto De Ioris
Date: 20140315

Disclaimer
----------

This article shows a pretty advanced way for combining websockets (or sse) apps with Django in a "safe way".

In my opinion the Python web-oriented world is facing a communication/marketing problem: There is a huge number of people
running heavily blocking apps (like Django) on non-blocking technologies (like gevent) only because someone told them it is cool and will solve all of their scaling issues.

This is completely WRONG, DANEGROUS and EVIL, you cannot mix blocking apps with non-blocking engines, even a single, ultra-tiny blocking part
can potentially destroy your whole stack. As i have already said dozens of time, if your app is 99.9999999% non-blocking, it is still blocking.

And no, monkey patching on your Django app is not magic. Unless you are using pretty-customized database adapters, tuned for working in a non-blocking way, you are doing wrong.

At the cost of looking a huber-asshole, i strongly suggest you to completely ignore people suggesting you to move your Django app to gevent, eventlet, tornado or whatever, without warning you about
the hundreds of problems you may encounter.

Having said that, i love gevent, it is probably the best (with perl's Coro::AnyEvent) supported loop engine in the uWSGI project. So in this article i will use gevent for managing websocket/sse traffic and plain multiprocessing for the Django part.

If this last sentence looks a nonsense to you, you probably do not know what uWSGI offloading is...


uWSGI offloading
----------------

The concept is not a new thing, or a uWSGI specific one. Projects like nodejs or twisted use it by ages.

Immagine this simple WSGI app:

.. code-block:: python

   def application(env, start_response):
       start_response('200 OK',[('Content-Type','text/plain')])
       f = open('/etc/services')
       # do not do it, if the file is 4GB it will allocate 4GB of memory !!!
       yield f.read()

it will simply returns the content of /etc/services. It is a pretty tiny file, so in few milliseconds your process will be ready to process another request.

What if /etc/services is 4 gigabytes ? Your process (or thread) will be blocked for various seconds (even minutes), and will not be able to manage another request
until the file is completely transferred.

Would not be cool if you can tell to another thread to send the file for you, so you will be able to manage another request ?

Offloading is exactly this: it will give you one ore more threads for doing simple and slow task for you. Which kind of tasks ? All of those that can be managed
in a non-blocking way, so a single thread can manage thousand of transfer for you.

You can see it as the DMA engine in your computer, your CPU will program the DMA to tranfer memory from a controller to the RAM, and then will be freed to accomplish another task whie the DMA works in background.

To enable offloading in uWSGI you only need to add the ``--offload-threads <n>`` option, where <n> is the number of threads per-process to spawn. (generally a single thread will be more than enough, but if you want to use/abuse your multiple cpu cores feel free to increase it)

Once offloading is enabled, uWSGI will automatically use it whenever it detects that an operation can be offloaded safely.

In the python/WSGI case the use of wsgi.file_wrapper will be offloaded automatically, as well as when you use the uWSGI proxy features for passing requests to other server speaking the uwsgi or HTTP protocol.

A cool example (showed even in the Snippets page of uWSGI docs) is implementing a offload-powered X-Sendfile feature:

.. code-block:: ini

   [uwsgi]
   ; load router_static plugin (compiled in by default in monolithic profiles)
   plugins = router_static
   
   ; spawn 2 offload threads
   offload-threads = 2
   
   ; files under /private can be safely served
   static-safe = /private
   
   ; collect the X-Sendfile response header as X_SENDFILE var
   collect-header = X-Sendfile X_SENDFILE
   
   ; if X_SENDFILE is not empty, pass its value to the "static" routing action (it will automatically use offloading if available)
   response-route-if-not = empty:${X_SENDFILE} static:${X_SENDFILE}

  ; now the classic options
  plugins = python  (compiled in by default if you installed uWSGI via pip)
  ; bind to HTTP port 8080
  http-socket = :8080
  ; load a simple wsgi-app
  wsgi-file = myapp.py
  
  
now in our app we can X-Sendfile to send static files without blocking:

.. code-block:: python

   def application(env, start_response):
       start_response('200 OK',[('X-Sendfile','/etc/services')])
       return []
