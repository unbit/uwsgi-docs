The uWSGI Caching Cookbook
==========================

This is a cookbook of various caching techniques using :doc:`InternalRouting` and :doc:`Caching`

The examples assume a modular uWSGI build. You can ignore the 'plugins' option, if you are using a monolithic build.

Let'start
*********

This is a simple perl/PSGI Dancer app we deploy on an http-socket with 4 processes

.. code-block:: pl

   use Dancer;

   get '/' => sub {
           "Hello World!"
   };

   dance;

This is the uWSGI config, pay attention to the log-micros directive. The objective of uWSGI in-memory caching is generating a response
in less than 1 millisecond (yes, this is true), so we want to get the response time logging in microseconds.

.. code-block:: ini

   [uwsgi]
   ; load the PSGI plugin as the default one
   plugins = 0:psgi
   ; load the Dancer app
   psgi = myapp.pl
   ; enable the master process
   master = true
   ; spawn 4 processes
   processes = 4
   ; bind an http socket to port 9090
   http-socket = :9090
   ; log response time with microseconds resolution
   log-micros = true


Run the uWSGI instance in your terminal and just make a bunch of requests to it

.. code-block:: sh

   curl -D /dev/stdout http://localhost:9090/

If all goes well you should see something similar in your uWSGI logs:

.. code-block:: sh

   [pid: 26586|app: 0|req: 1/1] 192.168.173.14 () {24 vars in 327 bytes} [Wed Apr 17 09:06:58 2013] GET / => generated 12 bytes in 3497 micros (HTTP/1.1 200) 4 headers in 126 bytes (0 switches on core 0)
   [pid: 26586|app: 0|req: 2/2] 192.168.173.14 () {24 vars in 327 bytes} [Wed Apr 17 09:07:14 2013] GET / => generated 12 bytes in 1134 micros (HTTP/1.1 200) 4 headers in 126 bytes (0 switches on core 0)
   [pid: 26586|app: 0|req: 3/3] 192.168.173.14 () {24 vars in 327 bytes} [Wed Apr 17 09:07:16 2013] GET / => generated 12 bytes in 1249 micros (HTTP/1.1 200) 4 headers in 126 bytes (0 switches on core 0)
   [pid: 26586|app: 0|req: 4/4] 192.168.173.14 () {24 vars in 327 bytes} [Wed Apr 17 09:07:17 2013] GET / => generated 12 bytes in 953 micros (HTTP/1.1 200) 4 headers in 126 bytes (0 switches on core 0)
   [pid: 26586|app: 0|req: 5/5] 192.168.173.14 () {24 vars in 327 bytes} [Wed Apr 17 09:07:18 2013] GET / => generated 12 bytes in 1016 micros (HTTP/1.1 200) 4 headers in 126 bytes (0 switches on core 0)


while curl will return:

.. code-block:: txt

   HTTP/1.1 200 OK
   Server: Perl Dancer 1.3112
   Content-Length: 12
   Content-Type: text/html
   X-Powered-By: Perl Dancer 1.3112

   Hello World!

The first request on a process took about 3 milliseconds (this is normal as lot of code is executed the first time), but the following run in about 1 millisecond).

Now we want to store the response in the uWSGI cache.

The first recipe
****************

We first create a uWSGI cache named 'mycache' with 100 slot of 64k (new options are at the end of the config) and at each request for '/' we search in it for a specific item
named 'myhome'.

This time we load the router_cache plugin too (it is builtin by default in monolithic servers)


.. code-block:: ini

   [uwsgi]
   ; load the PSGI plugin as the default one
   plugins = 0:psgi,router_cache
   ; load the Dancer app
   psgi = myapp.pl
   ; enable the master process
   master = true
   ; spawn 4 processes
   processes = 4
   ; bind an http socket to port 9090
   http-socket = :9090
   ; log response time with microseconds resolution
   log-micros = true

   ; create a cache with 100 items (default size per-item is 64k)
   cache2 = name=mycache,items=100
   ; at each request for / check for a 'myhome' item in the 'mycache' cache
   ; 'route' apply a regexp to the PATH_INFO request var
   route = ^/$ cache:key=myhome,name=mycache

restart uWSGI and re-run the previous test with curl. Sadly nothing will change. Why ?

Because you did not instructed uWSGI to store the plugin response in the cache. You need to use the cachestore routing action


.. code-block:: ini

   [uwsgi]
   ; load the PSGI plugin as the default one
   plugins = 0:psgi,router_cache
   ; load the Dancer app
   psgi = myapp.pl
   ; enable the master process
   master = true
   ; spawn 4 processes
   processes = 4
   ; bind an http socket to port 9090
   http-socket = :9090
   ; log response time with microseconds resolution
   log-micros = true

   ; create a cache with 100 items (default size per-item is 64k)
   cache2 = name=mycache,items=100
   ; at each request for / check for a 'myhome' item in the 'mycache' cache
   ; 'route' apply a regexp to the PATH_INFO request var
   route = ^/$ cache:key=myhome,name=mycache
   ; store each successfull request (200 http status code) for '/' in the 'myhome' item
   route = ^/$ cachestore:key=myhome,name=mycache

Now re-run the test, and you should see requests going down to a range of 100-300 microseconds (it depends on various factors, but you should gain at least 60% in response time)

Log line report -1 as the app id:

.. code-block:: sh

   [pid: 26703|app: -1|req: -1/2] 192.168.173.14 () {24 vars in 327 bytes} [Wed Apr 17 09:24:52 2013] GET / => generated 12 bytes in 122 micros (HTTP/1.1 200) 2 headers in 64 bytes (0 switches on core 0)

this is because when a response is served from the cache your app/plugin is not touched (in this case, no perl call is involved)

You will note less headers too:

.. code-block:: txt

   HTTP/1.1 200 OK
   Content-Type: text/html
   Content-Length: 12

   Hello World!

This is because only the body of a response is cached. By default the generated response is set as text/html but you can change it
or let the mime types engine do the work for you (see later)

Cache them all !!!
******************

We want to cache all of our requests. Some of them returns images and css, while the others are always text/html


.. code-block:: ini

   [uwsgi]
   ; load the PSGI plugin as the default one
   plugins = 0:psgi,router_cache
   ; load the Dancer app
   psgi = myapp.pl
   ; enable the master process
   master = true
   ; spawn 4 processes
   processes = 4
   ; bind an http socket to port 9090
   http-socket = :9090
   ; log response time with microseconds resolution
   log-micros = true

   ; create a cache with 100 items (default size per-item is 64k)
   cache2 = name=mycache,items=100
   ; load the mime types engine
   mime-file = /etc/mime.types

   ; at each request starting with /img check it in the cache
   route = ^/img/(.+) cache:key=/img/$1,name=mycache,mime=1

   ; at each request ending with .css check it in the cache
   route = \.css$ cache:key=${REQUEST_URI},name=mycache,content_type=text/css

   ; fallback to text/html all of the others request
   route = .* cache:key=${REQUEST_URI},name=mycache
   ; store each successfull request (200 http status code) in the 'mycache' cache using the REQUEST_URI as key
   route = ^/$ cachestore:key=${REQUEST_URI},name=mycache

