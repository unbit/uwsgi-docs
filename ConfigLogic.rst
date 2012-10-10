Configuration logic
===================

Starting from 1.1 certain logic constructs are available.

The following statements are currently supported:

* ``for`` .. ``endfor``
* ``if-dir`` / ``if-not-dir``
* ``if-env`` / ``if-not-env``
* ``if-exists`` / ``if-not-exists``
* ``if-file`` / ``if-not-file``
* ``if-option`` / ``if-not-option`` -- undocumented
* ``if-reload`` / ``if-not-reload`` -- undocumented

Each of these statements exports a context value you can access with the special placeholder ``%(_)`` For example, the for statement sets ``%(_)`` to the current iterated value.

.. warning:: Recursive logic is not supported and will cause uWSGI to promptly exit.

for
---

Iterates over space-separated strings.

.. code-block:: ini

  [uwsgi]
  master = true
  ; iterate over a list of ports
  for = 3031 3032 3033 3034 3035
  socket = 127.0.0.1:%(_)
  endfor =
  module = helloworld

or equivalently

.. code-block:: xml

  <uwsgi>
    <master/>
    <for>3031 3032 3033 3034 3035</for>
      <socket>127.0.0.1:%(_)</socket>
    <endfor/>
    <module>helloworld</module>
  </uwsgi>

or equivalently still

.. code-block:: shell

  uwsgi --for="3031 3032 3033 3034 3035" --socket="127.0.0.1:%(_)" --endfor --module helloworld

if-env
------

Check if an environment variable is defined, putting its value in the context placeholder.

.. code-block:: ini

  [uwsgi]
  if-env = PATH
  print = Your path is %(_)
  check-static = /var/www
  endif =
  socket = :3031

if-exists
---------

Check for the existence of a file/directory. The context placeholder is set to the filename found.

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

Check if the given path exists and is a regular file. The context placeholder is set to the filename found.

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

Check if the given path exists and is a directory. The context placeholder is set to the filename found.

.. code-block:: yml

  uwsgi:
    socket: 4040
    processes: 2
    if-file: config.ru
    rack: %(_)
    endif: