JVM in the uWSGI server (updated to 1.9)
========================================

Starting from uWSGI 1.9, you can have a full, thread-safe and versatile JVM embedded in the core.

All of the plugins can call JVM functions (written in java, jruby, jython, clojure, whatever the jvm support...) 
via the :doc:`RPC subsystem<RPC>` or using uWSGI :doc:`Signals`

The JVM plugin itself can implement request handlers to host JVM-based web applications. Currently JWSGI and Ring (Clojure)
apps are supported. A long-term goal is supporting servlet, but it will require heavy sponsorship and funding (feel free to ask
for more information about the project at info@unbit.it)

Building the JVM support
************************

First of all, be sure to have a full JDK distibution installed.

The uWSGI build system will try to detect common JDK setup (debian,ubuntu,centos, OSX...), but if it is not able
to find a JDK installation it will need infos from the user (see below).

To build the JVM plugin simply run:

.. code-block:: sh

   python uwsgiconfig --plugin plugins/jvm default

change 'default', if needed, with your alternative build profile. FOr example if you have a Perl/PSGI monolithic build
just run

.. code-block:: sh

   python uwsgiconfig --plugin plugins/jvm psgi

or for a fully-modular build

.. code-block:: sh

   python uwsgiconfig --plugin plugins/jvm core

If all goes well the jvm_plugin will be built.

If the build system cannot find a JDK installation you will ned to specify the path of the headers directory (the directory containing the jni.h file)
and the lib directory (the directory containing libjvm.so).

As an example, if jni.h is in /opt/java/includes and libjvm.so is in /opt/java/lib/jvm/i386, run the build system in that way:

.. code-block:: sh

   UWSGICONFIG_JVM_INCPATH=/opt/java/includes UWSGICONFIG_JVM_LIBPATH=/opt/java/lib/jvm/i386 python uwsgiconfig --plugin plugins/jvm


After a successfull build, you will get the path of the uwsgi.jar file.

That jarball containes classes to access the uWSGI api, and you should copy it in your CLASSPATH (or manually loading it from uWSGI)

Exposing functions via the RPC subsystem
****************************************

In this example we will export a "hello" java function (obviously returning a string) and we will call it
from a python WSGI application.

This is our base configuration (we assume a modular build)

.. code-block:: ini

   [uwsgi]
   plugins = python,jvm
   http = :9090
   wsgi-file = myapp.py
   jvm-classpath = /opt/uwsgi/lib/uwsgi.jar

The ``jvm-classpath`` is an option exported by the JVM plugin that allows you to add directories or jarfile to your classpath.

You can specify all of the ``jvm-classpath`` options you need

Here we are manually adding uwsgi.jar as we did not copied it in our CLASSPATH

This is our WSGI example script

.. code-block:: py

   import uwsgi
   
   def application(environ, start_response):
       start_response('200 OK', [('Content-Type','text/html')])
       yield "<h1>"
       yield uwsgi.call('hello')
       yield "</h1>"

here we use uwsgi.call (instead of uwsgi.rpc) as a shortcut (little performance gain in options parsing)

We now create our Foobar.java class (its main function will be run by uWSGI on startup)

.. code-block:: java

   public class Foobar {
      static void main() {

          // create an anonymous function
          uwsgi.RpcFunction rpc_func = new uwsgi.RpcFunction() { 
              public String function(String... args) {
                  return "Hello World";
              }
          };

          // register it in the uWSGI RPC subsystem
          uwsgi.register_rpc("hello", rpc_func);
      }
   }


The uwsgi.RpcFunction interface allows you to write uWSGI-compliant RPC functions

Now compile the Foobar.java file:

.. code-block:: sh

   javac Foobar.java

(eventually fix the classpath or pass the uwsgi.jar path with the -cp option)

You now have a Foobar.class that can be loaded by uWSGI

Let's complete the configuration

.. code-block:: ini

   [uwsgi]
   plugins = python,jvm
   http = :9090
   wsgi-file = myapp.py
   jvm-classpath = /opt/uwsgi/lib/uwsgi.jar
   jvm-main-class = Foobar

The last option (jvm-main-class) will load a java class and will execute its main() method.

We can now visit localhost:9090 and we should see the Hello World message

Registering signal handlers
***************************

In the same way as the RPC subsystem you can register signal handlers.

You will be able to call java functions on time events, file modifications, cron...

Our Sigbar.java

.. code-block:: java

   public class Sigbar {
      static void main() {

          // create an anonymous function
          uwsgi.SignalHandler sh = new uwsgi.SignalHandler() { 
              public void function(int signum) {
                  System.out.println("Hi, i am the signal " + signum);
              }
          };

          // register it in the uWSGI signal subsystem
          uwsgi.register_signal(17, "", sh);
      }
   }

uwsgi.SignalHandler is the interface for signal handlers.

Whenever signal 17 is rased, the corresponding java function will be run

Remember to compile the file, load it in uWSGI and to enable to master process (without it the signal subsystem will not work)


The fork() problem and multithreading
*************************************

The JVM is not fork() friendly. If you load a virtual machine in the master and then you fork() (like generally you do in other languages)
the children JVM will be broken (this is mainly because threads required by the JVM are not inherited).

For that reason a JVM for each worker, mule and spooler is spawned.

Fortunately enough, differently from the vast majority of other platforms, the JVM as a truly powerful multithreading support.

uWSGI supports it, so if you want to run one of the request handlers (JWSGI, clojure/Ring) just remember to spawn a number of threads with the --threads option

How it works
************

uWSGI embeds the JVM using the JNI interface. Sadly we cannot rely on JVM automatic garbage collector, so we have to manually
unreference all of the allocated object. This is not a problem from a performance and usage point of view, but makes the development of plugins
a bit more difficult (compared to other JNI-based products)

Fortunately the current api simplify that task a lot.

Passing options to the JVM
**************************

You can pass specific options to the JVM using the ``--jvm-opt`` option.

For example to limit the HEAP usage to 10 megabytes:

.. code-block:: ini

   [uwsgi]
   ...
   jvm-opt = -Xmx10m

Loading classes (without main method)
*************************************

We have already seen how to load classes and run their main() method on startup.

Often you will want to load classes only to add them to the JVM (allowing access to external modules needing them)

To load a class you can use ``--jvm-class``

.. code-block:: ini

   [uwsgi]
   ...
   jvm-class = Foobar
   jvm-class = org/unbit/Unbit

Remember class names must use the '/' format (not dot !!!). This rule applies to --jvm-main-class too.

Request handlers
****************

Albeit the Java (TM) world has its J2EE environment for deploying web applications, you may want to follow
a different approach (feel free to call it NO-Enterprise if you feel more cool).

The uWSGI project implements lot of features that are not part of J2EE (and does not implement lot of features that are a strong part of J2EE),
so you may find its approach best suited for your setup (or taste, or skills).

The JVM plugin exports an API for allow hooking web requests. This approach differs a bit from the uWSGI "classic one".

The JVM plugin register itself as the modifier1 with the value '8', but will look at the modifier2 value to know who of its request handlers
has to manage it.

For example the :doc:`Ring` plugin register itself in the JVM plugin as the modifier2 number '1'.

So to pass requests to it you need something like that:

.. code-block:: ini

   [uwsgi]
   http = :9090
   http-modifier1 = 8
   http-modifier2 = 1

or with nginx:

.. code-block:: c

   location / {
       include uwsgi_params;
       uwsgi_modifier1 8;
       uwsgi_modifier2 1;
       uwsgi_pass /tmp/uwsgi.socket;
   }


Currently there are 2 JVM request handlers available

:doc:`JWSGI`

:doc:`Ring` (for clojure)

As already said, there is the "idea" of developing a servlet request handler, but it requires sponsorhip (read: money)
as it will be a really big effort.

Notes
*****

You do not need special jars to use UNIX sockets, the JVM plugin has access to all of the uWSGI features.

You may be addicted to the log4j module. There is nothing wrong with it, but give a look at the uWSGI logging capabilities
(less resources needed, less configuration, and NO-Enterprise)

The uWSGI api access is still incomplete (will be updated after 1.9)

The JVM does not play well in environment with limited address space. Avoid using --limit-as if you load the JVM in your instances.


