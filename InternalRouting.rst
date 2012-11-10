uWSGI internal routing 
======================

Starting from tree 1.1, uWSGI contains an internal routing/rewrite subsystem.

Following the logging approach, new "routers" can be added as plugins.

These routers are included:

* ``uwsgi`` -- set modifiers and to eventually redirect requests to remote uWSGI servers
* ``redirect`` -- works very similarly to Apache's mod_rewrite, allowing you to quickly send HTTP redirects to clients without touching your app
* ``basicauth`` -- implements HTTP basic authentication
* ``http`` (since 1.3)
* ``rewrite`` (since 1.3)
* ``access`` (since 1.4)
* ``cache`` (since 1.4)

The internal router is configurable with:

.. code-block:: ini

  [uwsgi]
  route = <rule-regexp> <action> # define rule for PATH_INFO
  route-host = <rule-regexp> <action> # define rule for HTTP_HOST
  route-qs = <rule-regexp> <action> # define rule for QUERY_STRING
  route-uri = <rule-regexp> <action> # define rule for REQUEST_URI

The ``uwsgi`` router
--------------------

The uwsgi router has 2 syntaxes::

  uwsgi:,N1,N2

will set the specific modifiers, while

  uwsgi:addr,N1,N2

will forward the request to a remote uwsgi-speaking server.

Example: map requests ending with .cgi and .pl to the cgi plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ini
  
  [uwsgi]
  plugins = cgi
  socket = :3031
  cgi = /var/www/myscripts
  
  route = \.pl$ uwsgi:,9,0
  route = \.cgi$ uwsgi:,9,0

Example: forward requests starting with ``/foobar`` to a remote uwsgi server using the PSGI plugin
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: ini
  
  [uwsgi]
  socket = :3031
  route = ^/foobar uwsgi:192.168.173.9:3031,5,0

The ``redirect`` router
-----------------------

The redirect router allows you to send a HTTP 302 redirect. Doing it in uWSGI will be a lot faster than writing the rules in your app.

Regexp groups are supported. You can refer to groups using the Perl-like syntax $1, $2, $...

Example
^^^^^^^

.. code-block:: ini
  
  [uwsgi]
  socket = :3031
  
  route = uwsgi$ redirect:/UWSGI/wiki
  route = test redirect:http://example.com
  route = ^/foobar/(.+)/ redirect:http://unbit.it/$1


The ``basicauth`` router
------------------------

The ``basicauth`` router allows you to protect resources via HTTP Basic authentication.

Four syntaxes are supported:

* ``basicauth:realm,user:password`` -- a simple user:password mapping
* ``basicauth:realm,user:`` -- only authenticates username
* ``basicauth:realm,htpasswd`` -- use a ``htpasswd``-like file. All POSIX ``crypt()`` algorithms are supported. This is _not_ the same behavior as Apache's traditional htpasswd files, so use the ``-d`` flag of the ``htpasswd`` utility to create compatible files.
* ``basicauth:realm,`` -- Useful to cause a HTTP 401 response immediately. As routes are parsed top-bottom, you may want to raise that to avoid bypassing rules.

Example
^^^^^^^

.. code-block:: ini

  [uwsgi]  
  route = ^/foo basicauth:My Realm,foo:bar
  route = ^/foo basicauth:My Realm,foo2:bar2
  # The following rule is required as the last one will never match and an HTTP 401 would never be triggered
  route = ^/foo basicauth:My Realm,
  route = ^/bar basicauth:Another Realm,kratos:

Example: Using basicauth for Trac
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This will run Trac with 2 hardcoded users on HTTP port 9090.

.. code-block:: ini

  [uwsgi]
  ; load plugins (if required)
  plugins = python,router_basicauth
  
  ; bind to port 9090 using http protocol
  http-socket = :9090
  
  ; set trac instance path
  env = TRAC_ENV=myinstance
  ; load trac
  module = trac.web.main:dispatch_request
  
  ; trigger authentication on /login
  route = ^/login basicauth:Trac Realm,pippo:pluto
  route = ^/login basicauth:Trac Realm,foo:bar
  
  ;high performance file serving
  static-map = /chrome/common=/usr/local/lib/python2.7/dist-packages/trac/htdocs


The ``http`` router
-------------------

You can forward specific requests to an external http server

.. code-block:: ini

   [uwsgi]
   plugins = router_http
   route = ^/foobar http:127.0.0.1:4040
   route = ^/test http:192.168.173.3:3131

you can specify the Host header to ser

.. code-block:: ini

   [uwsgi]
   plugins = router_http
   route = ^/foobar http:127.0.0.1:4040,unbit.it
   route = ^/test http:192.168.173.3:3131,uwsgi.it

The http router supports `doc:offloading<OffloadSubsystem>`


The ``rewrite`` router
----------------------

.. note:: This router is undocumented.

The ``cache`` router
--------------------
