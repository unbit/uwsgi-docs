SSI (Server Side Includes) plugin
=================================

Server Side Includes are an "old-fashioned" way to write dynamic web pages.

It is generally recognized as a templating system instead of a full featured language.

The main purpose of the uWSGI SSI plugin is having a fast templating system that can use the uWSGI api.

Currently (March 2013) the plugin is in beta quality and implements less than 30% of the standard (the focus is in exposing uWSGI api as SSI commands)

Using it as a request handler
*****************************

The plugin has an official modifier, the 19:

.. code-block:: ini

   [uwsgi]
   plugin = ssi
   http = :9090
   http-modifier1 = 19
   http-var = DOCUMENT_ROOT=/var/www

The plugin build the filename as DOCUMENT_ROOT+PATH_INFO, the file is then parsed as a server side include.

Both DOCUMENT_ROOT and PATH_INFO are required, otherwise a 500 error will be returned.

An example config for nginx will be:

.. code-block:: c

   location ~ \.shtml$ {
       root /var/www;
       include uwsgi_params;
       uwsgi_pass 127.0.0.1:3031;
       uwsgi_modifier1 19;
   }

.. code-block:: ini

   [uwsgi]
   plugin = ssi
   socket = 127.0.0.1:3031

Using it as a routing action
****************************

A more versatile approach is using the ssi parser as a routing action:

.. code-block:: ini

   [uwsgi]
   plugin = ssi
   http-socket = :9090
   route = ^/(.*) ssi:/var/www/$1.shtml

the routing action does not need DOCUMENT_ROOT or PATH_INFO

Pay attention: as all of the routing actions, no check on file paths is made to allow higher customizations. If you pass untrusted paths
to the ssi action, you should sanitize them (you can use routing again, checking for the presence of .. or other dangerous symbols)

Supported SSI commands
**********************

This is the list of supported commands (and their args). If a command is not part of the standard (read: uWSGI specific) it will be reported

echo
^^^^

args = ``var``

print the content of the specified request variable

printenv
^^^^^^^^

print the list of all of the request variables

include
^^^^^^^

args = ``file``

include the specified file (relative to the current directory)

cache
^^^^^

uWSGI specific/non standard

args = ``key`` ``name``

print the value of the specified cache key in the specified cache name

Status
******

The plugin is fully thread safe and very fast.

Very few commands are available, more will be added soon.
