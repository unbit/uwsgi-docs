Scaling SSL connections (uWSGI 1.5-dev)
=======================================

Distributing SSL servers in a cluster is an hard topic.
The biggest problem is sharing SSL sessions between different nodes.

The problem is amplified in non-blocking servers due to OpenSSL limits in the way sessions are managed.

For example, you cannot share sessions in a memcached servers and access them in a non-blocking way.

A common solution (compromise ?) til now has been using a single ssl terminator balancing request to multiple non-encrypted backends.

The solution works, but obviously does not scale.

Starting from uWSGI 1.5-dev an implementation (based on the stud project) of distributed caching has been added.

Setup 1: using the uWSGI cache for storing SSL sessions
******************************************************

You can configure the SSL subsystem of uWSGI to use the shared cache. The SSL sessions timeout will
be ethe expire value of the cache item. In that way the cache sweeper (managed by the master) will destroy sessions
in respect of it

.. code-block:: ini

   [uwsgi]
   ; spawn the master process (it will run the cache sweeper thread)
   master = true
   ; store upto 20k sessions
   cache = 20000
   ; 4k are enough for ssl sessions
   cache-blocksize = 4096
   ; force the ssl subsystem to use the uWSGI cache as session storage
   ssl-sessions-use-cache = true
   ; set sessions timeout
   ssl-sessions-timeout = 300
   ; spawn an https router
   https = 192.168.173.1:8443,foobar.crt,foobar.key
   ; spawn 8 processes for the https router (all sharing the same sessions cache)
   http-processes = 8
   ; add a bunch of uwsgi nodes
   http-to = 192.168.173.10:3031
   http-to = 192.168.173.11:3031
   http-to = 192.168.173.12:3031
   ; add stats
   stats = 127.0.0.1:5001

Now starts blasting your https router and telnet to the port 5001. Under the "cache" object of the json
output you should see the values "items" and "hits" increasing. The value "miss" is increased every time a session is not found
in the cache. It is a good metric of SSL performance users can expect.


Setup 2: synchronize caches of different HTTPS routers
******************************************************

The objective is to sync each new session in all of the caches. To accomplish that you have to spawn a special thread
(the cache-udp-server) in each instance and list all of the remote server that must be synchronized.

A pure-tcp load balancer (like HAProxy or the uWSGI rawrouter) can be used to load balance between the various https routers.

(a rawrouter config)

.. code-block:: ini

   [uwsgi]
   master = true
   rawrouter = 192.168.173.99:443
   rawrouter-to = 192.168.173.1:8443
   rawrouter-to = 192.168.173.2:8443
   rawrouter-to = 192.168.173.3:8443
   
Now you can configure the first node (the new options are at the end of the .ini config)

.. code-block:: ini

   [uwsgi]
   ; spawn the master process (it will run the cache sweeper thread)
   master = true
   ; store upto 20k sessions
   cache = 20000
   ; 4k are enough for ssl sessions
   cache-blocksize = 4096
   ; force the ssl subsystem to use the uWSGI cache as session storage
   ssl-sessions-use-cache = true
   ; set sessions timeout
   ssl-sessions-timeout = 300
   ; spawn an https router
   https = 192.168.173.1:8443,foobar.crt,foobar.key
   ; spawn 8 processes for the https router (all sharing the same sessions cache)
   http-processes = 8
   ; add a bunch of uwsgi nodes
   http-to = 192.168.173.10:3031
   http-to = 192.168.173.11:3031
   http-to = 192.168.173.12:3031
   ; add stats
   stats = 127.0.0.1:5001
   
   ; spawn the cache-udp-server
   cache-udp-server = 192.168.173.1:7171
   ; propagate updates to the other nodes
   cache-udp-node = 192.168.173.2:7171
   cache-udp-node = 192.168.173.3:7171


and the others two...

.. code-block:: ini

   [uwsgi]
   ; spawn the master process (it will run the cache sweeper thread)
   master = true
   ; store upto 20k sessions
   cache = 20000
   ; 4k are enough for ssl sessions
   cache-blocksize = 4096
   ; force the ssl subsystem to use the uWSGI cache as session storage
   ssl-sessions-use-cache = true
   ; set sessions timeout
   ssl-sessions-timeout = 300
   ; spawn an https router
   https = 192.168.173.2:8443,foobar.crt,foobar.key
   ; spawn 8 processes for the https router (all sharing the same sessions cache)
   http-processes = 8
   ; add a bunch of uwsgi nodes
   http-to = 192.168.173.10:3031
   http-to = 192.168.173.11:3031
   http-to = 192.168.173.12:3031
   ; add stats
   stats = 127.0.0.1:5001
   
   ; spawn the cache-udp-server
   cache-udp-server = 192.168.173.2:7171
   ; propagate updates to the other nodes
   cache-udp-node = 192.168.173.1:7171
   cache-udp-node = 192.168.173.3:7171

.. code-block:: ini

   [uwsgi]
   ; spawn the master process (it will run the cache sweeper thread)
   master = true
   ; store upto 20k sessions
   cache = 20000
   ; 4k are enough for ssl sessions
   cache-blocksize = 4096
   ; force the ssl subsystem to use the uWSGI cache as session storage
   ssl-sessions-use-cache = true
   ; set sessions timeout
   ssl-sessions-timeout = 300
   ; spawn an https router
   https = 192.168.173.3:8443,foobar.crt,foobar.key
   ; spawn 8 processes for the https router (all sharing the same sessions cache)
   http-processes = 8
   ; add a bunch of uwsgi nodes
   http-to = 192.168.173.10:3031
   http-to = 192.168.173.11:3031
   http-to = 192.168.173.12:3031
   ; add stats
   stats = 127.0.0.1:5001
   
   ; spawn the cache-udp-server
   cache-udp-server = 192.168.173.3:7171
   ; propagate updates to the other nodes
   cache-udp-node = 192.168.173.1:7171
   cache-udp-node = 192.168.173.2:7171


Start smashing the rawrouter (remember to use a client supporting ssl sessions, like your browser) and get cache statistics
from the stats server of each https node. If the count of "hits" is a lot higher than the "miss" value the system is working well
and your load is distributed and in high performance mode.


Notes
*****

If you do not want to manually configure the cache udp nodes you can use multicast (if your network supports it)

.. code-block:: ini

   [uwsgi]
   ...
   cache-udp-server = 225.1.1.1:7171
   cache-udp-node = 225.1.1.1:7171

A new gateway server is in development, named the 'udprepeater'. It will basically forward all of the udp
packets it receive to the subscribed backend nodes. It will allows you to maintain the zero-config style of the subscription system
(basically you only need to configure a single cache udp node pointing to the udprepeater)