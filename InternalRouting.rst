uWSGI internal routing
======================

``Updated to 1.9``

Since uWSGI 1.9, a programmable internal routing subsystem is available (older releases since 1.1 have a less featureful version).

You can use the internal routing subsystem to dynamically alter the way requests are handled. For example you can
use it to trigger a 301 redirect on specific URLs, or to serve content from the cache on specific conditions.

The internal routing subsystem is inspired by Apache's ``mod_rewrite`` and Linux's ``iptables`` command.

Please, before blasting it for being messy, not-elegant nor Turing-complete, remember that it must be FAST and only FAST.
If you need elegance and more complexity, do that (more slowly) in your code.

The internal routing table
**************************

The internal routing table is a sequence of ''rules'' executed one after another (forward jumps are allowed too).

Each rule is composed by a ''subject'', a ''condition'' and an ''action''

The ''condition'' is generally a PCRE regexp applied to the subject, if it matches the action is triggered. Subjects are request's variables.

Currently the following subjects are supported:

* ``host`` (check HTTP_HOST)
* ``uri`` (check REQUEST_URI)
* ``qs`` (check QUERY_STRING)
* ``remote-addr`` (check REMOTE_ADDR)
* ``referer`` (check HTTP_REFERER)
* ``user-agent`` (check HTTP_USER_AGENT)
* ``default`` (default subject, maps to PATH_INFO)

In addition to this, a pluggable system of lower-level conditions is available.

You can access this system using the ``--route-if`` option.

Currently the following checks are supported:

* ``exists`` (check if the subject exists in the filesystem)
* ``isfile`` (check if the subject is a file)
* ``isdir`` (check if the subject is a directory)
* ``isexec`` (check if the subject is an executable file)
* ``equal``/``isequal``/``eq``/``==`` (check if the subject is equal to the specified pattern)
* ``ishigherequal``/``>=``
* ``ishigher``/``>``
* ``islower``/``<``
* ``islowerequal``/``<=``
* ``startswith`` (check if the subject starts with the specified pattern)
* ``endswith`` (check if the subject ends with the specified pattern)
* ``regexp``/re (check if the subject matches the specified regexp)
* ``empty`` (check if the subject is empty)
* ``contains``

When a check requires a pattern (like with 'equal' or 'regexp') you split it from the subject with a semicolon:

.. code-block:: ini

   ; never matches
   route-if = equal:FOO;BAR log:never here
   ; matches
   route if = regexp:FOO;^F log:starts with F


Actions are the functions to run if a rule matches. This actions are exported by plugins and have a return value.

Action return values
********************

Each action has a return value which tells the routing engine what to do next.

The following return codes are supported:

* ``NEXT`` (continue to the next rule)
* ``CONTINUE`` (stop scanning the internal routing table and run the request)
* ``BREAK`` (stop scanning the internal routing table and close the request)
* ``GOTO x`` (go to rule ``x``)

When a rule does not match, ``NEXT`` is assumed.

The first example
*****************

.. code-block:: ini

   [uwsgi]
   route-user-agent = .*curl.* redirect:http://uwsgi.it
   route-remote-addr = ^127\.0\.0\.1$ break:403 Forbidden
   route = ^/test log:someone called /test
   route = \.php$ rewrite:/index.php
   route = .* addheader:Server: my uWSGI server
   route-host = ^localhost$ logvar:local=1
   route-uri = ^/foo/(.*)\.jpg$ cache:key=$1.jpg
   route-if = equal:${PATH_INFO};/bad break:500 Internal Server Error

The previous rules, build the following table:

* if the ``HTTP_USER_AGENT`` var contains 'curl' redirect the request to http://uwsgi.it (code 302, action returns BREAK)
* if ``REMOTE_ADDR`` is '127.0.0.1' returns a 403 Forbidden (action returns BREAK)
* if ``PATH_INFO`` starts with /test print the string 'someone called /test' in the logs (action returns NEXT)
* if ``PATH_INFO`` ends with '.php' rewrite it to /index.php (action returns NEXT)
* for all of the ``PATH_INFO`` add the HTTP header 'Server: my uWSGI server' to the response (action returns NEXT)
* if ``HTTP_HOST`` is localhost add the logvar 'local' setting it to '1'
* if ``REQUEST_URI`` starts with /foo and ends with .jpg get it from the uWSGI cache using the supplied key (built over regexp grouping) (action returns BREAK)
* if the ``PATH_INFO`` is equal to /bad throws a 500 error

Accessing request vars
**********************

In addition to PCRE placeholders/groups (using $1 to $9) you can access request variables (PATH_INFO, SCRIPT_NAME, REQUEST_METHOD...)
using the ${VAR} syntax.

.. code-block:: ini

   [uwsgi]
   route-user-agent = .*curl.* redirect:http://uwsgi.it${REQUEST_URI}
   route-remote-addr = ^127\.0\.0\.1$ break:403 Forbidden for ip ${REMOTE_ADDR}

Accessing cookies
*****************

You can access a cookie value using the ${cookie[name]} syntax:

.. code-block:: ini

   [uwsgi]
   route = ^/foo log:${cookie[foobar]}

this will log the content of the 'foobar' cookie of the current request

Accessing query string items
****************************

You can access the value of the HTTP query string using the ${qs[name]} syntax:

.. code-block:: ini

   [uwsgi]
   route = ^/foo log:${qs[foobar]}

this will log the content of the 'foobar' item of the current request's query string

Pluggable routing variables
***************************

Both the cookie and qs vars, are so-called "routing vars". They are pluggable, so external plugins can
add new vars to add new features to your application. (Check the :doc:`GeoIP` plugin for an example of this.)

A number of embedded routing variables are also available.

* ``mime`` -- returns the mime type of the specified var: ${mime[REQUEST_URI]}
  
  .. code-block:: ini
  
     [uwsgi]
     route = ^/images/(.+) addvar:MYFILE=$1.jpg
     route = ^/images/ addheader:Content-Type: ${mime[MYFILE]}

* ``time`` -- returns time/date in various form. The only supported (for now) is time[unix] returning the epoch
* ``math`` -- requires matheval support. Example: math[CONTENT_LENGTH+1]
* ``base64`` -- encode the specified var in base64
* ``hex`` -- encode the specified var in hex
* ``uwsgi`` -- return internal uWSGI information, uwsgi[wid] and uwsgi[pid] are currently supported

Is --route-if not enough? Why --route-uri and friends?
******************************************************

This is a good question. You just need to always remember that uWSGI is about versatility and *performance*. Gaining cycles
is always good. The ``--route-if`` option, albeit versatile, cannot be optimized, all of its parts has to be recomputed at every request.
This is obviously very fast, but ``--route-uri`` option (and friends) can be pre-optimized (during startup) to directly map to the request memory areas, so if you can use them, you definitely should. :)

GOTO
****

Yes, the most controversial construct of the whole information technology industry (and history) is here. You can make forward (only forward!) jumps to specific points of the internal routing table. You can set labels to mark specific point of the table, or if you are brave (or foolish)
jump directly to a rule number (rule numbers are printed on server startup, but please use labels...)

.. code-block:: ini

   [uwsgi]

   route-host = ^localhost$ goto:localhost
   route-host = ^sid\.local$ goto:sid.local
   route = .* last:
  
   route-label = sid.local
   route-user-agent = .*curl.* redirect:http://uwsgi.it
   route-remote-addr = ^192\.168\..* break:403 Forbidden
   route = ^/test log:someone called /test
   route = \.php$ rewrite:/index.php
   route = .* addheader:Server: my sid.local server
   route = .* logvar:local=0
   route-uri = ^/foo/(.*)\.jpg$ cache:key=$1.jpg
   route = .* last:

   route-label = localhost
   route-user-agent = .*curl.* redirect:http://uwsgi.it
   route-remote-addr = ^127\.0\.0\.1$ break:403 Forbidden
   route = ^/test log:someone called /test
   route = \.php$ rewrite:/index.php
   route = .* addheader:Server: my uWSGI server
   route = .* logvar:local=1
   route-uri = ^/foo/(.*)\.jpg$ cache:key=$1.jpg
   route = .* last:

The example is like the previous one, but we make tiny differences between domains. Check the use of "last:", to interrupt the routing table scan.

Obviously (or not?) you can rewrite the first 2 rules as one:

.. code-block:: ini

   [uwsgi]

   route-host = (.*) goto:$1
   
The available actions
*********************

``continue``/``last``
^^^^^^^^^^^^^^^^^^^^^

Return value: ``CONTINUE``

Stop the scanning of the internal routing table and continue to the selected request handler.

``break``
^^^^^^^^^

Return value: ``BREAK``

Stop scanning the internal routing table and close the request. Can optionally returns the specified HTTP status code:

.. code-block:: ini

   [uwsgi]
   route = ^/notfound break:404 Not Found
   route = ^/bad break:
   route = ^/error break:500

``log``
^^^^^^^

Return value: ``NEXT``

Print the specified message in the logs.

.. code-block:: ini

   [uwsgi]
   route = ^/logme/(.) log:hey i am printing $1

``logvar``
^^^^^^^^^^

Return value: ``NEXT``

Add the specified logvar.

.. code-block:: ini

   [uwsgi]
   route = ^/logme/(.) logvar:item=$1

``goto``
^^^^^^^^

Return value: ``NEXT``

Make a forward jump to the specified label or rule position

``addvar``
^^^^^^^^^^

Return value: ``NEXT``

Add the specified CGI (environment) variable to the request.

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) addvar:FOOVAR=prefix$1suffix

``addheader``
^^^^^^^^^^^^^

Return value: ``NEXT``

Add the specified HTTP header to the response.

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) addheader:Foo: Bar

``delheader``//``remheader``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return value: ``NEXT``

Remove the specified HTTP header from the response.


.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) delheader:Foo

``signal``
^^^^^^^^^^

Return value: ``NEXT``

Raise the specified uwsgi signal.

``send``
^^^^^^^^

Return value: ``NEXT``

Extremely advanced (and dangerous) function allowing you to add raw data to the response.

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) send:destroy the world

``send-crnl``
^^^^^^^^^^^^^

Return value: ``NEXT``

Extremely advanced (and dangerous) function allowing you to add raw data to the response, suffixed with \r\n.

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) send-crnl:HTTP/1.0 100 Continue

``redirect``/``redirect-302``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return value: ``BREAK``

Plugin: ``router_redirect``

Return a HTTP 302 Redirect to the specified URL.

``redirect-permanent``/``redirect-301``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Return value: ``BREAK``

Plugin: ``router_redirect``

Return a HTTP 301 Permanent Redirect to the specified URL.

``rewrite``
^^^^^^^^^^^

Return value: ``NEXT``

Plugin: ``router_rewrite``

A rewriting engine inspired by Apache mod_rewrite. Rebuild PATH_INFO and QUERY_STRING according to the specified rules before the request is dispatched to the request handler.

.. code-block:: ini

   [uwsgi]
   route-uri = ^/foo/(.*) rewrite:/index.php?page=$1.php

``rewrite-last``
^^^^^^^^^^^^^^^^

Alias for rewrite but with a return value of ``CONTINUE``, directly passing the request to the request handler next.

``uwsgi``
^^^^^^^^^

Return value: ``BREAK``

Plugin: ``router_uwsgi``

Rewrite the modifier1, modifier2 and optionally ``UWSGI_APPID`` values of a request or route the request to an external uwsgi server.

.. code-block:: ini

   [uwsgi]
   route = ^/psgi uwsgi:127.0.0.1:3031,5,0

This configuration routes all of the requests starting with ``/psgi`` to the uwsgi server running on 127.0.0.1:3031 setting modifier1 to 5 and modifier2 to 0.

If you only want to change the modifiers without routing the request to an external server, use the following syntax.

.. code-block:: ini

   [uwsgi]
   route = ^/psgi uwsgi:,5,0

To set a specific ``UWSGI_APPID`` value, append it.

.. code-block:: ini

   [uwsgi]
   route = ^/psgi uwsgi:127.0.0.1:3031,5,0,fooapp

The subrequest is async-friendly (engine like gevent, or ugreen are supported) and if offload threads are available they will be used.

``http``
^^^^^^^^

Return value: ``BREAK``

Plugin: ``router_http``

Route the request to an external HTTP server.

.. code-block:: ini

   [uwsgi]
   route = ^/zope http:127.0.0.1:8181

You can substitute an alternative Host header with the following syntax:

.. code-block:: ini

   [uwsgi]
   route = ^/zope http:127.0.0.1:8181,myzope.uwsgi.it

``static``
^^^^^^^^^^

Return value: ``BREAK``

Plugin: ``router_static``

Serve a static file from the specified physical path.

.. code-block:: ini

   [uwsgi]
   route = ^/logo static:/var/www/logo.png

``basicauth``
^^^^^^^^^^^^^

Return value: ``NEXT`` or ``BREAK 401`` on failed authentication

Plugin: ``router_basicauth``

Four syntaxes are supported.

* ``basicauth:realm,user:password`` – a simple user:password mapping
* ``basicauth:realm,user:`` – only authenticates username
* ``basicauth:realm,htpasswd`` – use a htpasswd-like file. All POSIX crypt() algorithms are supported. This is _not_ the same behavior as Apache’s traditional htpasswd files, so use the ``-d`` flag of the htpasswd utility to create compatible files.
* ``basicauth:realm,`` – Useful to cause a HTTP 401 response immediately. As routes are parsed top-bottom, you may want to raise that to avoid bypassing rules.

Example:

.. code-block:: ini

   [uwsgi]
   route = ^/foo basicauth-next:My Realm,foo:bar
   route = ^/foo basicauth:My Realm,foo2:bar2
   route = ^/bar basicauth:Another Realm,kratos:

Example: using basicauth for Trac

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
   route = ^/login basicauth-next:Trac Realm,pippo:pluto
   route = ^/login basicauth:Trac Realm,foo:bar

   ;high performance file serving
   static-map = /chrome/common=/usr/local/lib/python2.7/dist-packages/trac/htdocs

``basicauth-next``
^^^^^^^^^^^^^^^^^^

same as ``basicauth`` but returns ``NEXT`` on failed authentication.

``ldapauth``
^^^^^^^^^^^^

Return value: ``NEXT`` or ``BREAK 401`` on failed authentication

Plugin: ``ldap``

This auth router is part of the LDAP plugin, so it has to be loaded in order for this to be available. 
It's like the basicauth router, but uses an LDAP server for authentication, syntax: ``ldapauth:realm,options``

Available options:

* ``url`` - LDAP server URI (required)
* ``binddn`` - DN used for binding. Required if the LDAP server does not allow anonymous searches.
* ``bindpw`` - password for the ``binddn`` user.
* ``basedn`` - base DN used when searching for users (required)
* ``filter`` - filter used when searching for users (default is "(objectClass=*)")
* ``attr`` - LDAP attribute that holds user login (default is "uid")
* ``loglevel`` - 0 - don't log any binds, 1 - log authentication errors, 2 - log both successful and failed binds

Example:

.. code-block:: ini

   route = ^/protected ldapauth:LDAP auth realm,url=ldap://ldap.domain.com;basedn=ou=users,dc=domain;binddn=uid=proxy,ou=users,dc=domain;bindpw=password;loglevel=1;filter=(objectClass=posixAccount)

``ldapauth-next``
^^^^^^^^^^^^^^^^^

Same as ldapauth but returns ``NEXT`` on failed authentication.

``cache``
^^^^^^^^^

Return value: ``BREAK``

Plugin: ``router_cache``

``cachestore``/``cache-store``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``cachevar``
^^^^^^^^^^^^

``cacheset``
^^^^^^^^^^^^

``memcached``
^^^^^^^^^^^^^

``rpc``
^^^^^^^

The "rpc" routing instruction allows you to call uWSGI RPC functions directly from the routing subsystem and forward their output to the client.

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   route = ^/foo addheader:Content-Type: text/html
   route = ^/foo rpc:hello ${REQUEST_URI} ${HTTP_USER_AGENT}
   route = ^/bar/(.+)$ rpc:test $1 ${REMOTE_ADDR} uWSGI %V
   route = ^/pippo/(.+)$ rpc:test@127.0.0.1:4141 $1 ${REMOTE_ADDR} uWSGI %V
   import = funcs.py



``call``
^^^^^^^^^

Plugin: ``rpc``


``rpcret``
^^^^^^^^^

Plugin: ``rpc``

`rpcret` calls the specified rpc function and uses its return value as the action return code (next, continue, goto, etc)


``rpcblob``//``rpcnext``
^^^^^^^^^^^^^^^^^^^^^^^^

Plugin: ``rpc``

`rpcnext/rpcblob` calls the specified RPC function, sends the response to the client and continues to the next rule.


``rpcraw``
^^^^^^^^^

Plugin: ``rpc``


``access``
^^^^^^^^^^

``spnego``
^^^^^^^^^^

In development...

``radius``
^^^^^^^^^^

In development...

``xslt``
^^^^^^^^

.. seealso:: :doc:`XSLT`

ssi
^^^

.. seealso:: :doc:`SSI`

gridfs
^^^^^^

.. seealso:: :doc:`GridFS`

``donotlog``
^^^^^^^^^


``chdir``
^^^^^^^^^


``setapp``
^^^^^^^^^


``setuser``
^^^^^^^^^


``sethome``
^^^^^^^^^


``setfile``
^^^^^^^^^


``setscriptname``
^^^^^^^^^


``setprocname``
^^^^^^^^^


``alarm``
^^^^^^^^^


``flush``
^^^^^^^^^


``fixcl``
^^^^^^^^^


``cgi``
^^^^^^^^^

Plugin: ``cgi``


``cgihelper``
^^^^^^^^^

Plugin: ``cgi``


``access``
^^^^^^^^^

Plugin: ``router_access``


``cache-continue``
^^^^^^^^^

Plugin: ``router_cache``


``cachevar``
^^^^^^^^^

Plugin: ``router_cache``


``cacheinc``
^^^^^^^^^

Plugin: ``router_cache``


``cachedec``
^^^^^^^^^

Plugin: ``router_cache``


``cachemul``
^^^^^^^^^

Plugin: ``router_cache``


``cachediv``
^^^^^^^^^

Plugin: ``router_cache``


``proxyhttp``
^^^^^^^^^

Plugin: ``router_http``


``memcached``
^^^^^^^^^

Plugin: ``router_memcached``


``memcached-continue``
^^^^^^^^^

Plugin: ``router_memcached``


``proxyuwsgi``
^^^^^^^^^

Plugin: ``router_uwsgi``
