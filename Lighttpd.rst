Lighttpd support
================

.. note:: Lighttpd support is experimental.

The uwsgi handler for Lighttpd lives in the ``/lighttpd`` directory of the
uWSGI distribution.

Building the module
-------------------

First download the source of lighttpd and uncompress it. Copy the
``lighttpd/mod_uwsgi.c`` file from the uWSGI distribution into Lighttpd's
``/src`` directory. Add the following to the lighttpd ``src/Makefile.am``
file, after the accesslog block:

::

  lib_LTLIBRARIES += mod_uwsgi.la
  mod_uwsgi_la_SOURCES = mod_uwsgi.c
  mod_uwsgi_la_LDFLAGS = -module -export-dynamic -avoid-version -no-undefined
  mod_uwsgi_la_LIBADD = $(common_libadd)

Then launch

::

  autoreconf -fi

and as usual,

::

  ./configure && make && make install

Configuring Lighttpd
--------------------

Modify your configuration file:

::
  
  server.modules = (
    ...
    "mod_uwsgi",
    ...
  )

  # ...

  uwsgi.server = (
    "/pippo" => (( "host" => "192.168.173.15", "port" => 3033 )),
    "/" => (( "host" => "127.0.0.1", "port" => 3031 )),
  )

If you specify multiple hosts under the same virtual path/URI, load balancing
will be activated with the "Fair" algorithm.
