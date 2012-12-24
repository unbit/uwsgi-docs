The JWSGI interface
===================

.. note:: JWSGI is not a standard. Yet. If you like JWSGI, why not send an RFC to the uWSGI mailing list. We have no interest in a standard, but who knows...

JWSGI is a port of the WSGI/PSGI/Rack way of thinking for Java.

If, for some obscure reason, you'd feel like developing apps with JVM languages and you don't feel like deploying a huge servlet stack, JWSGI should be up your alley.

It is a very simple (and admittedly raw) protocol where you call a public method that takes a ``Hashtable`` as its sole argument.
This Hashtable contains CGI style variables and ``jwsgi.input`` containing a Java FileDescriptor that you can use with ``java.io``.

Example
-------

A simple JWSGI app looks like this:

.. code-block:: java

	import java.util.Hashtable;
	import java.util.ArrayList;

	public class utest {

	    public static Object[] jwsgi(Hashtable env) {

	        String status = "200 Ok";

	        ArrayList<Object> headers = new ArrayList<Object>();

	        String[] header = {"Content-type", "text/html"};
	        headers.add(header);
	        String[] header2 = {"Server", "uWSGI"};
	        headers.add(header2);

	        String body = "<h1>Hello World</h1>" + env.get("REQUEST_URI");

	        Object[] response = {status, headers, body};

	        return response;
	    }
	}

And to consume HTTP body content,

.. code-block:: java

	public static Object[] jwsgi(Hashtable env) throws java.io.IOException {

            if (env.containsKey("CONTENT_LENGTH")) {
                    String s = (String) env.get("CONTENT_LENGTH");
                    if (s.length() > 0) {
                            Integer cl = Integer.parseInt( s );
                            FileInputStream f = new FileInputStream( (FileDescriptor) env.get("jwsgi.input") );
                            byte[] b = new byte[cl];

                            if (f.read(b) > 0) {
                                    String postdata = new String(b);
                                    System.out.println( postdata );
                            }
                    }
            }

            String status = "200 Ok";

            ArrayList<Object> headers = new ArrayList<Object>();

            String[] header = { "Content-type", "text/html" } ;
            headers.add(header);
            String[] header2 = { "Server", "uWSGI" } ;
            headers.add(header2);



            String body = "<form method=\"POST\"><input type=\"text\" name=\"nome\"/><input type=\"submit\" value=\"send\" /></form>" + env.get("REQUEST_URI");

            Object[] response = { status, headers, body };

            return response;
    }


How to use it?
--------------

The procedure to run JWSGI is still sort of messy. You have to build both the JVM and the JWSGI plugins. Modifier 8 has been assigned to the JWSGI interface, so remember to edit your webserver
configuration accordingly.

1. Edit ``plugins/jvm/uwsgiplugin.py`` to set ``JVM_INCPATH`` and ``JVM_LIBPATH`` to their right values. What the right values are is system dependent. Search for ``jni.h`` and ``libjvm.so``.
   Do the same for ``plugins/jwsgi/uwsgiplugin.py``.

2. Build!

   .. code-block:: sh

      python uwsgiconfig.py --build core
      python uwsgiconfig.py --plugin plugins/jvm core
      python uwsgiconfig.py --plugin plugins/jwsgi core

3. Compile your class with ``javac``.

   .. code-block:: sh

      javac utest.java

4. Run uWSGI and load the utest class.

   .. code-block:: sh

      ./uwsgi -s :3031 --plugins jvm,jwsgi --jvm-main-class utest -M -p 4 -m

Important Notes
---------------

* The jwsgi method must be called ``jwsgi``. This will be fixed soon.
* The jwsgi plugin may leaks memory at every request. We are still evaluating if memory management must be managed in the jvm plugin, or in the jwsgi one. Recently a patch had been merged for this issue, but only was tested on Ubuntu 12.0.4 and Oracle JDK 7.
* Threading will be a core component of the JVM plugin in the future. Expect an update soon.
