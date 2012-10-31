Configuring uWSGI
=================

uWSGI can be configured using several different methods. All configuration methods may be mixed and matched in the same invocation of uWSGI.

In the following examples the "socket" configuration option will be set to `/tmp/uwsgi.sock` and `127.0.0.1:8000`, and Master mode will be enabled with 3 workers.

In all file-based configuration methods, the use of placeholders of the format ``%(foo)`` is supported in option values.

.. note:: Some of the configuration methods may require to be compiled in.

.. seealso:: :doc:`ConfigLogic`

.. seealso:: If you run Python applications, you can avoid the use of a configuration file to set up apps. See :ref:`PythonAppDict`.


.. _LoadingConfig:

Loading configuration files
---------------------------

uWSGI supports loading configuration files over several other methods than simple disk files::

  uwsgi --ini http://uwsgi.it/configs/myapp.ini # HTTP
  uwsgi --xml - # standard input
  uwsgi --yaml fd://0 # file descriptor
  uwsgi --json 'exec://nc 192.168.11.2:33000' # arbitrary executable

.. note::

  More esoteric file sources, such as the :doc:`Emperor<Emperor>`, embedded configuration (in two flavors), dynamic library symbols and ELF sections could also be used.
  This is undocumented, but it's possible. This is the uWSGI way.

.. _MagicVars:

Magic variables
---------------

uWSGI configuration files can include special "magic" variables, prefixed with a percent sign.

Currently the following magic variables (you can access them in Python via :py:data:`uwsgi.magic_table`) are defined.

======== ==
%v       the vassals directory
%o       the original config filename, as specified on the command line
%p       the absolute path of the configuration file
%s       the filename of the configuration file
%d       the absolute path of the directory containing the configuration file
%e       the extension of the configuration file
%n       the filename without extension
%c       the name of the directory containing the config file (version 1.3+)
%0..%9   a specific component of the full path of the directory containing the config file (version 1.3+)
======== ==

For example, here's :file:`funnyapp.ini`.

.. code-block:: ini

  [uwsgi]
  socket = /tmp/%n.sock
  module = werkzeug.testapp:test_app
  processes = 4
  master = 1

``%n`` will be replaced with the name of the config file, sans extension, so the result in this case will be

.. code-block:: ini

  [uwsgi]
  socket = /tmp/funnyapp.sock
  module = werkzeug.testapp:test_app
  processes = 4
  master = 1

.. _Placeholders:

Placeholders
------------

Placeholders are custom special variables defined during configuration time by simply setting a new configuration variable of your own devising.

As always, code is better than words

.. code-block:: ini

  [uwsgi]
  ; These are placeholders...
  my_funny_domain = uwsgi.it
  max_customer_address_space = 64
  customers_base_dir = /var/www
  ; And these aren't.
  socket = /tmp/sockets/%(my_funny_domain).sock
  chdir = %(customers_base_dir)/%(my_funny_domain)
  limit-as = %(max_customer_address_space)

Placeholders are accessible, like any uWSGI option, in your application code via :py:data:`uwsgi.opt`.

.. code-block:: python

  import uwsgi
  print uwsgi.opt['customers_base_dir']

This feature can be (ab)used to reduce the number of configuration files required by your application.


Command line arguments
----------------------

Example::

  uwsgi --socket /tmp/uwsgi.sock --socket 127.0.0.1:8000 --master --workers 3

.. _ConfigEnv:

Environment variables
---------------------

When passed as environment variables, options are capitalized and prefixed with `UWSGI_`, and dashes are substituted with underscores.

.. note::

   Several values for the same configuration variable are not supported with this method.

Example::

   UWSGI_SOCKET=127.0.0.1 UWSGI_MASTER=1 UWSGI_WORKERS=3 uwsgi

INI files
---------

.INI files are a standard de-facto configuration way used by a lot of applications.

It consists of ``[section]``s and ``key=value`` pairs.



An example uWSGI INI configuration:

.. code-block:: ini

  [uwsgi]
  socket = /tmp/uwsgi.sock
  socket = 127.0.0.1:8000
  workers = 3
  master = true

By default, uWSGI uses the ``[uwsgi]`` section, but you can specify another section name while loading the INI file with the syntax ``filename:section``, that is::

  uwsgi --ini myconf.ini:app1

* Whitespace is insignificant within lines.
* Lines starting with a semicolon (``;``) or a hash/octothorpe (``#``) are ignored as comments.
* Boolean values may be set without the value part. Simply ``master`` is thus equivalent to ``master=true``. This may not be compatible with other INI parsers such as ``paste.deploy``.
* For convenience, uWSGI recognizes bare ``.ini`` arguments specially, so the invocation ``uwsgi myconf.ini``  is equal to ``uwsgi --ini myconf.ini``.

XML files
---------

The root node should be ``<uwsgi>`` and option values text nodes.


An example:

.. code-block:: xml

  <uwsgi>
    <socket>/tmp/uwsgi.sock</socket>
    <socket>127.0.0.1:8000</socket>
    <master/>
    <workers>3</workers>
  </uwsgi>

You can also have multiple ``<uwsgi>`` stanzas in your file, marked with different ``id`` attributes. To choose the stanza to use, specify its id after the filename in the ``xml`` option, using a colon as a separator.
When using this `id` mode, the root node of the file may be anything you like. This will allow you to embed ``uwsgi`` configuration nodes in other XML files.

.. code-block:: xml

  <i-love-xml>
    <uwsgi id="turbogears"><socket>/tmp/tg.sock</socket></uwsgi>
    <uwsgi id="django"><socket>/tmp/django.sock</socket></uwsgi>
  </i-love-xml>

* Boolean values may be set without a text value.
* For convenience, uWSGI recognizes bare ``.xml`` arguments specially, so the invocation ``uwsgi myconf.xml``  is equal to ``uwsgi --xml myconf.xml``.

JSON files
----------

The JSON file should represent an object with one key-value pair, the key being `"uwsgi"` and the value an object of configuration variables. Native JSON lists, booleans and numbers are supported.

An example:

.. code-block:: json

  {"uwsgi": {
    "socket": ["/tmp/uwsgi.sock", "127.0.0.1:8000"],
    "master": true,
    "workers": 3
  }}

.. note::

   The `Jansson`_ library is required during uWSGI build time to enable JSON support.
   By default the presence of the library will be auto-detected and JSON support will be automatically enabled, but you can force JSON support to be enabled or disabled by editing your build configuration.

   .. seealso:: :doc:`Install`

.. _Jansson: http://www.digip.org/jansson/

YAML files
----------

The root element should be `uwsgi`. Boolean options may be set as `true` or `1`.

An example:

.. code-block:: yaml

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
