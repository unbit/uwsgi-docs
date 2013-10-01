Configuration logic
===================

Starting from 1.1 certain logic constructs are available.

The following statements are currently supported:

* ``for`` .. ``endfor``
* ``if-dir`` / ``if-not-dir``
* ``if-env`` / ``if-not-env``
* ``if-exists`` / ``if-not-exists``
* ``if-file`` / ``if-not-file``
* ``if-opt`` / ``if-not-opt`` -- undocumented
* ``if-reload`` / ``if-not-reload`` -- undocumented

Each of these statements exports a context value you can access with the
special placeholder ``%(_)``. For example, the "for" statement sets ``%(_)`` to
the current iterated value.

.. warning:: Recursive logic is not supported and will cause uWSGI to promptly exit.

for
---

For iterates over space-separated strings. The following three code blocks are equivalent.

.. code-block:: ini

  [uwsgi]
  master = true
  ; iterate over a list of ports
  for = 3031 3032 3033 3034 3035
  socket = 127.0.0.1:%(_)
  endfor =
  module = helloworld


.. code-block:: xml

  <uwsgi>
    <master/>
    <for>3031 3032 3033 3034 3035</for>
      <socket>127.0.0.1:%(_)</socket>
    <endfor/>
    <module>helloworld</module>
  </uwsgi>


.. code-block:: sh

  uwsgi --for="3031 3032 3033 3034 3035" --socket="127.0.0.1:%(_)" --endfor --module helloworld

Note that the for-loop is applied to each line inside the block
separately, not to the block as a whole. For example, this:

.. code-block:: ini

  [uwsgi]
  for = a b c
  socket = /var/run/%(_).socket
  http-socket = /var/run/%(_)-http.socket
  endfor =

is expanded to:

.. code-block:: ini

  [uwsgi]
  socket = /var/run/a.socket
  socket = /var/run/b.socket
  socket = /var/run/c.socket
  http-socket = /var/run/a-http.socket
  http-socket = /var/run/b-http.socket
  http-socket = /var/run/c-http.socket

if-env
------

Check if an environment variable is defined, putting its value in the context
placeholder.

.. code-block:: ini

  [uwsgi]
  if-env = PATH
  print = Your path is %(_)
  check-static = /var/www
  endif =
  socket = :3031

if-exists
---------

Check for the existence of a file or directory. The context placeholder is set
to the filename found.

.. code-block:: ini

  [uwsgi]  
  http = :9090
  ; redirect all requests if a file exists
  if-exists = /tmp/maintainance.txt
  route = .* redirect:/offline
  endif =

.. note:: The above example uses :doc:`InternalRouting`.

if-file
-------

Check if the given path exists and is a regular file. The context placeholder
is set to the filename found.

.. code-block:: xml

  <uwsgi>
    <plugins>python</plugins>
    <http-socket>:8080</http-socket>
    <if-file>settings.py</if-file>
      <module>django.core.handlers.wsgi:WSGIHandler()</module>
    <endif/>
  </uwsgi>

if-dir
------

Check if the given path exists and is a directory. The context placeholder is
set to the filename found.

.. code-block:: yaml

  uwsgi:
    socket: 4040
    processes: 2
    if-file: config.ru
    rack: %(_)
    endif:
