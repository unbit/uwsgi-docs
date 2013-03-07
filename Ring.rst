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

Pay attention to the modifier config. The JVM plugin register itself as the 8 one, while the ring plugin register itself to the JVM parent-one as '1' (that you set as the modifier2)

Using Leiningen
***************

Leiningen is a great tool for managing clojure projects. If you use clojure, you are very probably a Leiningen user.

One of the great advantages of leiningen is the easy generation of single jar distribution. That means you can deploy a whole app
with a single file.

Let's create a new helloworld ring application with lein

.. code-block:: sh

   lein new helloworld

move it to the just created 'helloworld' directory and edit the project.clj file

.. code-block:: clojure

   (defproject helloworld "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.4.0"]])

we want to add the ring-core package to our dependancies (it contains a set of classes/modules to simplify the writing of ring apps) and obviously we need to change description and url:

.. code-block:: clojure

   (defproject helloworld "0.1.0-SNAPSHOT"
  :description "My second uWSGI ring app"
  :url "https://uwsgi-docs.readthedocs.org/en/latest/Ring.html"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[org.clojure/clojure "1.4.0"] [ring/ring-core "1.2.0-beta1"]])

save it and run

.. code-block:: sh

   lein repl

this will install all of the jar we need and will move us to the clojure console (just exit from it for now)

Now we want to write our ring app, just edit the file src/helloworld/core.clj and place the following content in it:

.. code-block:: clojure

   (ns helloworld.core
    (:use ring.util.response))

   (defn handler [request]
    (-> (response "Hello World")
    (content-type "text/plain")))


then edit (again) project.clj again to instruct leiningen on which namespaces to build:

.. code-block:: clojure

   (defproject helloworld "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}

  :aot [helloworld.core]

  :dependencies [[org.clojure/clojure "1.4.0"] [ring/ring-core "1.2.0-beta1"]])


as you can see we have added helloworld.core in the :aot keyword

Now let's compile our code:

.. code-block:: sh

   lein compile

and build the full jar (the uberjar):

.. code-block:: sh

   lein uberjar

if all goes well you should see a message like that at the end of the procedure:

.. code-block:: sh

   Created /home/unbit/helloworld/target/helloworld-0.1.0-SNAPSHOT-standalone.jar

annotate the path somewhere and let's configure uWSGI to run our application

.. code-block:: ini

   [uwsgi]
   http = :9090
   http-modifier1 = 8
   http-modifier2 = 1

   jvm-classpath = plugins/jvm/uwsgi.jar
   jvm-classpath = /home/unbit/helloworld/target/helloworld-0.1.0-SNAPSHOT-standalone.jar

   jvm-class = helloworld/core__init

   ring-app = helloworld.core:handler

This time we do not load clojure code, but directly a JVM class.

Pay attention, when you specify a JVM class you have to use the '/' form, not that dot one !!!

The __init suffix is automatically added by the system when your app is compiled.

The ``ring-app`` set the entry point to the helloworld.core namespace and the function 'handler'.

We can access that namespace as we have loaded it with ``jvm-class``

Concurrency
***********

As all of the JVM plugin request handlers, multithreading is the best way to achieve concurrency.

Threads in the JVM are really solid, do not be afraid to use them (even if you can spawn multiple processes too)

.. code-block:: ini

   [uwsgi]
   http = :9090
   http-modifier1 = 8
   http-modifier2 = 1

   jvm-classpath = plugins/jvm/uwsgi.jar
   jvm-classpath = /home/unbit/helloworld/target/helloworld-0.1.0-SNAPSHOT-standalone.jar

   jvm-class = helloworld/core__init

   ring-app = helloworld.core:handler

   master = true
   processes = 4
   threads = 8

this setup will spawn 4 uWSGI processes (workers) with 8 threads each (for a total of 32 threads)

Notes and status
****************

A shortcut option allowing to load compiled code and specifying the ring app would be cool

As the :doc:`JWSGI` handler, all of the uWSGI performance features are automatically used (like when sending static files
or buffering input)

The plugin has been realized with the cooperation (and the ideas) of Mingli Yuan
