The Clojure/Ring JVM request handler
====================================

Thanks to the JVM pluging available from 1.9, Clojure web app can be run on uWSGI.

The supported webserver-gatway standard is Ring:

https://github.com/ring-clojure/ring

its full spec are available here:

https://github.com/ring-clojure/ring/blob/master/SPEC

A uWSGI build profile name "ring" is available for generating a monolithic build with the jvm plugin and the ring one.

From the uWSGI sources:

.. code-block:: sh

   UWSGI_PROFILE=ring make

The build system will try to detect your JDK installation based on various presets (for example on centos you can yum install 
java-1.6.0-openjdk.x86_64-devel or java-1.7.0-openjdk-devel.x86_64 or on debian/ubuntu openjdk-6-jdk and so on...)

OSX/X-Code default paths are searched too.

For more infos on the JVM plugin check :doc:`JVM`

After a successfull build you will have the uwsgi binary and a uwsgi.jar file that you should copy in your CLASSPATH (or just remember
to set it in the uwsgi configuration everytime).

Our first Ring app
******************

A basic clojure ring app could be the following (save it as myapp.clj):

.. code-block:: clojure

   (ns myapp)

   (defn handler [req]
        {:status 200
         :headers { "Content-Type" "text/plain" , "Server" "uWSGI" }
         :body (str "<h1>The requested uri is " (get req :uri) "</h1>")
        }
   )

The code defines a new namespace called 'myapp', in which the 'handler' function is the Ring entry point (the function called at each web request)

We can now build a configuration serving that app on the HTTP router on port 9090 (call it config.ini):

.. code-block:: ini

   [uwsgi]
   http = :9090
   http-modifier1 = 8
   http-modifier2 = 1

   jvm-classpath = plugins/jvm/uwsgi.jar
   jvm-classpath = ../.lein/self-installs/leiningen-2.0.0-standalone.jar

   clojure-load = myapp.clj
   ring-app = myapp:handler

run uWSGI:

.. code-block:: sh

   ./uwsgi config.ini

now connect to port 9090 and you should see the app response.

As you can note we have manually added to our classpath uwsgi.jar and the leiningen standalone jar (it includes the whole clojure distribution).

Obviously if you do not want to use leiningen, just add the clojure jar to your classpath

The ``clojure-load`` load a clojure script in the JVM (very similar to what ``jvm-class`` do with the basic jvm plugin).

The ``ring-app`` option specify the class/namespace in which to search for the ring function entry point.

In our case the function is in the 'myapp' namespace and it is called 'handler' (you can understand that the syntax is namespace:function)

Using Leiningen
***************

Concurrency
***********

Notes
*****
