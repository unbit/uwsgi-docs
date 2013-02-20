uWSGI internal routing
======================

``Updated to 1.9``

Since uWSGI 1.9, a programmable internal routing subsystem is available (older releases have it, but with lot less features)

You can use the internal routing subsystem to dinamically alter the way requests are handled. For example you can
use it to trigger a 301 redirect on specific urls, or to serve content from the cache on specific conditions.

The internal routing subsystem is inspired by Apache mod_rewrite and Linux iptables command.

Please, before blasting it for being messy, not-elegant nor turing-complete, remember that it must be FAST and only FAST.
If you need elegance, do that (slowly) in your code.

The internal routing table
**************************

The internal routing table is a sequence of ''rules'' executed one after another (forward jumps are allowed too).

Each rule is composed by a ''subject'', a ''condition'' and an ''action''

The ''condition'' is a PCRE regexp applied to the subject, if it matches the action is triggered. Subjects are request's variables.

Currently the following subjects are supported:

* host (check HTTP_HOST)
* uri (check REQUEST_URI)
* qs (check QUERY_STRING)
* remote-addr (check REMOTE_ADDR)
* referer (check HTTP_REFERER)
* user-agent (check HTTP_USER_AGENT)
* default (default subject, maps to PATH_INFO)

Actions, are the functions to run if a rule matches. This actions are exported by plugins and have a return value

Action's return value
*********************

Each action has a return value, that value tell the routing engine what to do next.

The following return codes are supported:

* NEXT (continue to the next rule)
* CONTINUE (stop scanning the internal routing table and run the request)
* BREAK (stop scanning the internal routing table and close the request)
* GOON (continue to the next rule with an action plugin different from the current one)

When a rule does not match, NEXT is assumed

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

The previous rules, build the following table:

* if the HTTP_USER_AGENT var contains 'curl' redirect the request to http://uwsgi.it (code 302, action returns BREAK)
* if the REMOTE_ADDR is '127.0.0.1' returns a 403 Forbidden (action returns BREAK)
* if the PATH_INFO starts with /test print the string 'someone called /test' in the logs (action returns NEXT)
* if the PATH_INFO ends with '.php' rewrite it to /index.php (action returns NEXT)
* for all of the PATH_INFO add the HTTP header 'Server: my uWSGI server' to the response (action returns NEXT)
* if HTTP_HOST is localhost add the logvar 'local' setting it to '1'
* if REQUEST_URI starts with /foo and ends with .jpg get it from the uWSGI cache using the supplied key (built over regexp grouping)
 (action returns BREAK)

GOTO
****

Yes, the most controversial construct of the whole information technology industry (and history) is here. You can make forward jumps (only forward !!!)
to specific points of the internal routing table. You can set labels to mark specific point of the table, or if you are brave (or fool)
directly the rule number (rule number are printed on server startup, but please use labels...)

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

The example is like the previous one, but we make tiny differences between domains. Check the use of "last:", that interrupt
the routing table scan.

Obviously (or not ?) you can rewrite the first 2 rules as one:

.. code-block:: ini

   [uwsgi]

   route-host = (.*) goto:$1
   
The available actions
*********************

This is the list of currently (february 2013) supported actions


continue
^^^^^^^^

return value: CONTINUE

stop the scanning of the internal routing table and continue to the request handler

last
^^^^

same as continue

break
^^^^^

return value: BREAK

stop the scanning of the internal routing table and close the request

can optionally returns the specified HTTP status code:

.. code-block:: ini

   [uwsgi]
   route = ^/notfound break:404 Not Found
   route = ^/bad break:
   route = ^/error break:500

goon
^^^^

return value: GOON

jump (forward) to the first rule with the action plugin different from the current one.

This function is only for internal use.

log
^^^

return value: NEXT

print the specified message in the logs

.. code-block:: ini

   [uwsgi]
   route = ^/logme/(.) log:hey i am printing $1

logvar
^^^^^^

return value: NEXT

add the specified logvar

.. code-block:: ini

   [uwsgi]
   route = ^/logme/(.) logvar:item=$1

goto
^^^^

return value: NEXT

make a forward jump to the specified label or rule position

addvar
^^^^^^

return value: NEXT

add the specified CGI var to the request

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) addvar:FOOVAR=prefix$1suffix

addheader
^^^^^^^^^

return value: NEXT

add the specified HTTP header to the response

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) addheader:Foo: Bar

delheader
^^^^^^^^^

return value: NEXT

remove the specified HTTP header from the response


.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) delheader:Foo

remheader
^^^^^^^^^

alias for delheader

signal
^^^^^^

return value: NEXT

raise the specified uwsgi signal

send
^^^^

return value: NEXT

Extremely advanced (and dangerous) function allowing you to add raw data to the response

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) send:destroy the world

send-crnl
^^^^^^^^^

return value: NEXT

Extremely advanced (and dangerous) function allowing you to add raw data to the response with \r\n suffix

.. code-block:: ini

   [uwsgi]
   route = ^/foo/(.) send-crnl:HTTP/1.0 100 Continue


redirect
^^^^^^^^

return value: BREAK

plugin: router_redirect

redirect (302) to the specified url/uri

redirect-302
^^^^^^^^^^^^

alias for redirect

redirect-permanent
^^^^^^^^^^^^^^^^^^

return value: BREAK

plugin: router_redirect

redirect (301) to the specified url/uri

redirect-301
^^^^^^^^^^^^

alias for redirect-permanent


rewrite
^^^^^^^

return value: NEXT

plugin: router_rewrite

Apache mod_rewrite inspired rewrite engine. Rebuild PATH_INFO and QUERY_STRING accordingly to the specified rule

.. code-block:: ini

   [uwsgi]
   route-uri = ^/foo/(.*) rewrite:/index.php?page=$1.php

rewrite-last
^^^^^^^^^^^^

alias for rewrite but with a return value of CONTINUE

uwsgi
^^^^^

return value: BREAK

plugin: router_uwsgi

Rewrite the modifier1 and modifier2 values of a request or route the request to an external uwsgi server

.. code-block:: ini

   [uwsgi]
   route = ^/psgi uwsgi:127.0.0.1:3031,5,0

route all of the requests starting with /psgi to the uwsgi server running on 127.0.0.1:3031 setting modifier1 to 5 and modifier2 to 0

If you only want to change the modifiers without routing the request to an external server use the following syntax

.. code-block:: ini

   [uwsgi]
   route = ^/psgi uwsgi:,5,0

you can even set a specific UWSGI_APPID value

.. code-block:: ini

   [uwsgi]
   route = ^/psgi uwsgi:127.0.0.1:3031,5,0,fooapp

The request is async-friendly (engine like gevent, or ugreen are supported) and if offload threads are available they will be used.

http
^^^^

return value: BREAK

plugin: router_http

route the request to an external http server

.. code-block:: ini

   [uwsgi]
   route = ^/zope http:127.0.0.1:8181

you can specify an alternative Host header with the following syntax:

.. code-block:: ini

   [uwsgi]
   route = ^/zope http:127.0.0.1:8181,myzope.uwsgi.it


