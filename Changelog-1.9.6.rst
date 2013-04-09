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




Availability
************
