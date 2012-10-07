Configuring uWSGI
=================

uWSGI can be configured using several different methods. All configuration methods may be mixed and matched in the same invocation of uWSGI.

In the following examples the "socket" configuration option will be set to `/tmp/uwsgi.sock` and `127.0.0.1:8000`, and Master mode will be enabled with 3 workers.

.. note::

   Some of the configuration methods may require to be compiled in.


Command line arguments
----------------------

Example::

  uwsgi --socket /tmp/uwsgi.sock --socket 127.0.0.1:8000 --master --workers 3


Environment variables
---------------------

When passed as environment variables, options are capitalized and prefixed with `UWSGI_`, and dashes are substituted with underscores.

.. note::

   Several values for the same configuration variable are not supported with this method.

Example::

   UWSGI_SOCKET=127.0.0.1 UWSGI_MASTER=1 UWSGI_WORKERS=3 uwsgi

XML files
---------

The root node should be `<uwsgi>` and option values text nodes. Boolean values may be set without a text value.

Example::

  <uwsgi>
    <socket>/tmp/uwsgi.sock</socket>
    <socket>127.0.0.1:8000</socket>
    <master/>
    <workers>3</workers>
  </uwsgi>

JSON files
----------

The JSON file should represent an object with one key-value pair, the key being `"uwsgi"` and the value an object of configuration variables. Native JSON lists, booleans and numbers are supported.

Example::

  {"uwsgi": {
    "socket": ["/tmp/uwsgi.sock", "127.0.0.1:8000"],
    "master": true,
    "workers": 3
  }}

YAML files
----------

The root element should be `uwsgi`. Boolean options may be set as `true` or `1`.

Example::

  uwsgi:
    socket: /tmp/uwsgi.sock
    socket: 127.0.0.1:8000
    master: 1
    workers: 3


SQLite configuration
--------------------

.. note::

  Under construction.

LDAP configuration
------------------

LDAP is a flexible way to centralize configuration of large clusters of uWSGI servers. Configuring it is a complex topic. See :doc:`LDAP` for more information.
