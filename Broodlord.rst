Auto-scaling with Broodlord mode
================================

Broodlord (taken from Starcraft, like :doc:`Zerg` mode) is a way for vassals to ask for more workers from the Emperor.

Broodlord mode alone is not very useful, but combined with :doc:`Zerg`, :doc:`Idle` and :doc:`Emperor`, it can be used to implement auto-scaling for your apps.

A simple example
----------------

We'll start apps with a single worker, adding resources on demand.

Broodlord mode expects an additional stanza in your config file to be used for zergs (additional workers).

.. code-block:: ini

  [uwsgi]
  socket = :3031
  master = true
  vassal-sos-backlog = 10
  module = werkzeug.testapp:test_app
  processes = 1
  zerg-server = /tmp/broodlord.sock
  disable-logging = true
  
  [zerg]
  zerg = /tmp/broodlord.sock
  master = true
  module = werkzeug.testapp:test_app
  processes = 1
  disable-logging = true
  idle = 30
  die-on-idle = true

The ``vassal-sos-backlog`` option (supported only on Linux and TCP sockets) will ask the Emperor for zergs when the listen queue is higher than the given value, default 10. More "vassal-sos-" options will be added in the future to allow more specific detect-overload systems.

The ``[zerg]`` stanza is the config the Emperor will run when a vassal requires resources.

The ``die-on-idle`` option will completely destroy the zerg when inactive for more than 30 seconds.

As you can see this configuration is a sort of a puzzle: you can combine the various uWSGI features to implement various ways of scaling.

Now you have to run the Emperor specifying how many zerg instances can be run

.. code-block:: sh

  uwsgi --emperor /etc/vassals --emperor-broodlord 40

This will allow you to run up to 40 additional zerg workers for your apps.