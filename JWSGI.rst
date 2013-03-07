The JWSGI interface
===================

.. note:: JWSGI is not a standard. Yet. If you like JWSGI, why not send an RFC to the uWSGI mailing list. We have no interest in a standard, but who knows...

JWSGI is a port of the WSGI/PSGI/Rack way of thinking for Java.

If, for some obscure reason, you'd feel like developing apps with JVM languages and you don't feel like deploying a huge servlet stack, JWSGI should be up your alley.

It is a very simple protocol where you call a public method that takes a ``HashMap`` as its sole argument.
This HashMap contains CGI style variables and ``jwsgi.input`` containing a Java InputStream object.

The function has to returns an array of 3 Objects:

status (java/lang/Integer) Example '200'

headers (HashMap) Example {"Content-type": "text/html", "Server": "uWSGI", "Foo": ["one","two"]}

body (can be a String, an array of String, a File or an InputStream object)

Example
-------

A simple JWSGI app looks like this:

.. code-block:: java

   import java.util.*;
   public class MyApp {

       public static Object[] application(HashMap env) {

           int status = 200;

           HashMap<String,Object> headers = new HashMap<String,Object>();
           headers.put("Content-type", "text/html");
           // a response header can have multiple values
           String[] servers = {"uWSGI", "Unbit"};
           headers.put("Server", servers);

           String body = "<h1>Hello World</h1>" + env.get("REQUEST_URI");

           Object[] response = { status, headers, body };

           return response;
       }
   }



How to use it ?
***************


1. Compile your class with ``javac``.

   .. code-block:: sh

      javac MyApp.java

4. Run uWSGI and specify the method to run (in the form class:method)

   .. code-block:: sh

      ./uwsgi --socket /tmp/uwsgi.socket --plugins jvm,jwsgi --jwsgi MyApp:application --threads 40

this will run a JWSGI application on UNIX socket /tmp/uwsgi.socket with 40 threads


Reading request body
********************

The jwsgi.input item is an uwsgi.RequestBody object (subclass of java/io/InputStream). You can use it to access the request body

.. code-block:: java

   import java.util.*;
   public class MyApp {

       public static Object[] application(HashMap env) {

           int status = 200;

           HashMap<String,Object> headers = new HashMap<String,Object>();
           headers.put("Content-type", "text/plain");

           int body_len = Integer.parseInt((String) env.get("CONTENT_LENGTH"));
           byte[] chunk = new byte[body_len];

           uwsgi.RequestBody input = (uwsgi.RequestBody) env.get("jwsgi.input");

           int len = input.read(chunk);

           System.out.println("read " + len + " bytes");

           String body = new String(chunk, 0, len);

           Object[] response = { status, headers, body };

           return response;
       }
   }

Pay attention to the use of read(byte[]) instead of the classical (and the only required by the InputStream specs) read().

The read() one (no arguments) read one byte at time, while the second one is more efficient (it reads in chunk). 

JWSGI and Groovy
****************

Being very low-level the JWSGI standard can be used as-is in other languages running on the JVM.

As an example this is a Hello World groovy example:

.. code-block:: groovy

   static def Object[] application(java.util.HashMap env) {
        def headers = ["Content-Type":"text/html", "Server":"uWSGI"]
        return [200, headers, "<h1>Hello World</h1"]
   }

and another one serving a static file

.. code-block:: groovy

   static def Object[] application(java.util.HashMap env) {
        def headers = ["Content-Type":"text/plain", "Server":"uWSGI"]
        return [200, headers, new File("/etc/services")]
   }

The second approach is really efficient as it will abuse uWSGI internal facilities (for example if you have offloading enabled, your thread will be suddenly freed)

To load groovy code remember to compile it:

.. code-block:: sh

   groovyc Foobar.groovy

then you can run it

.. code-block:: sh

   ./uwsgi --socket /tmp/uwsgi.socket --plugins jvm,jwsgi --jwsgi Foobar:application --threads 40
