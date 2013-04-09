uWSGI 1.9.6
===========

Changelog 20130409

Bugfixes
********

* workaround for building the python plugin with gcc 4.8

Sorry, this is not a real bugfix, but making a release without bugfixes seems wrong...

New Features
************

Sqlite and LDAP pluginization
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Storing configurations in sqlite databases or LDAP tree is a pretty "uncommon" way to configure uWSGI
instances. For such a reason they have been moved to dedicated plugins.

If you store config in a sqlite database, just add --plugin sqlite3. For LDAP, just add --plugin ldap:

.. code-block:: sh

   uwsgi --plugin sqlite --sqlite config.db

Configuring dynamic apps with internal routing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

'Til now, you need to configure your webserver to load apps dinamically.

Three new instructions have been added to load aplication on demand.

Check the example:

.. code-block:: ini

   [uwsgi]

   http-socket = :9090

   route = ^/foo chdir:/tmp
   route = ^/foo log:SCRIPT_NAME=${SCRIPT_NAME}
   route = ^/foo log:URI=${REQUEST_URI}
   route = ^/foo sethome:/var/uwsgi/venv001
   route = ^/foo setfile:/var/uwsgi/app001.py
   route = ^/foo break:

   route = ^/bar chdir:/var
   route = ^/bar addvar:SCRIPT_NAME=/bar
   route = ^/bar sethome:/var/uwsgi/venv002
   route = ^/bar setfile:/var/uwsgi/app002.py
   route = ^/bar break:

as you can see, rewriting SCRIPT_NAME is now very easy. The sethome instruction is currently available only for python application
(it means 'virtualenv')

Carbon avg computation (Author: Łukasz Mierzwa)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can now configure how the carbon plugin send the response average when no requests have been managed.

You have three ways:

   --carbon-idle-avg none - don't push any avg_rt value if no requests were made

   --carbon-idle-avg last - use last computed avg_rt value (default)

   --carbon-idle-avg zero - push 0 if no requests were made



Numeric checks for the internal routing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

New check are available:

ishigher or '>'

islower or '<'

ishigherequal or '>='

islowerequal or '<='

Example:

.. code-block:: ini

   [uwsgi]
   route-if = ishigher:${CONTENT_LENGTH};1000 break:403 Forbidden


Math and time for the internal routing subsystem
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you build uWSGI with matheval support (matheval-dev on debian/ubuntu) you will get
math support in your routing system via the 'math' routing var.

The 'time' routing var has been added currently exporting only the 'unix' field returning the epoch.

Check this crazy example:

.. code-block:: ini

   [uwsgi]
   http-socket = :9090
   route-run = addvar:TEMPO=${time[unix]}
   route-run = log:inizio = ${TEMPO}
   route-run = addvar:TEMPO=${math[TEMPO+1]}
   route-run = log:tempo = ${TEMPO}


As you can see the routing subsystem can store values in request variables (here we create a 'TEMPO' var, and you will be able to access it even in your app request vars)

The 'math' operations can reference request vars

Check the matheval docs for the supported operations: http://matheval.sourceforge.net/docs/index.htm

Added non-standard seek() and tell() to wsgi.input (post-buffering required)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

While testing the 'smart mode' of the 'Klaus' project (https://github.com/jonashaag/klaus) we noticed it was violating
the WSGI standard calling seek() and tell() when in smart mode.

We have added support for both methods when post-buffering is enabled.

REMEMBER: they violate the WSGI standard, so try to avoid them (if you can). There are better ways to accomplish that.

Pyshell improvements, AKA Welcome IPython (Idea: C Anthony Risinger)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You can invoke the ipython shell instead of the default one when using --pyshell:

.. code-block:: sh

   uwsgi -s :3031 --pyshell="from IPython import embed; embed()"

Obviously you can pass whatever code to --pyshell

The 'rpcraw' routing instruction
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Another powerful and extremely dangerous routing action. It will call a rpc function
sending its return value directly to the client (without further processing).

Empty return values means "go to the next routing rule".

Return values must be valid HTTP:

.. code-block:: js

   uwsgi.register_rpc('myrules', function(uri) {
        if (uri == '/foo') {
                return "HTTP/1.0 200 OK\r\nContent-Type: text/plain\r\nServer: uWSGI\r\nFoo: bar\r\n\r\nCiao Ciao";
        }
        return "";
   });

.. code-block:: ini

   [uwsgi]
   plugin = v8
   v8-load = rules.js
   route = ^/foo rpcraw:myrules ${REQUEST_URI}



Availability
************
