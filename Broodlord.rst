Auto-scaling with Broodlord mode
================================

Broodlord (taken from Starcraft, like :doc:`Zerg` mode) is a way for vassals to
ask for more workers from the Emperor.  Broodlord mode alone is not very
useful. However, when combined with :doc:`Zerg`, :doc:`Idle` and :doc:`Emperor`
it can be used to implement auto-scaling for your apps.

A 'simple' example
------------------

We'll start apps with a single worker, adding resources on demand.  Broodlord
mode expects an additional stanza in your config file to be used for zergs.

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

The ``vassal-sos-backlog`` option (supported only on Linux and TCP sockets)
will ask the Emperor for zergs when the listen queue is higher than the given
value. By default the value is 10. More "vassal-sos-" options will be added in
the future to allow for more specific detect-overload systems.

The ``[zerg]`` stanza is the config the Emperor will run when a vassal requires
resources.  The ``die-on-idle`` option will completely destroy the zerg when
inactive for more than 30 seconds.  This configuration shows how to combine the
various uWSGI features to implement different means of scaling.  To run the
Emperor we need to specify how many zerg instances can be run:

.. code-block:: sh

  uwsgi --emperor /etc/vassals --emperor-broodlord 40

This will allow you to run up to 40 additional zerg workers for your apps.

--vassal-sos
------------

This has been added in 2.0.7, and allows the vassal to ask for reinforcement as soon as all of its workers are busy.

The option takes a value (integer) that is the number of seconds to wait before asking for a new reinforcement.

Manually asking for reinforcement
---------------------------------

You can use the master fifo (with command 'B') To force an instance to ask for reinforcement by the Emperor

.. code-block:: sh

   echo B > /var/run/master.fifo

Under the hood (aka: hacking broodlord mode)
--------------------------------------------

Technically broodlord mode is a simple message sent by a vassal to force the Emperor to spawn another vassal with ':zerg' suffix as the instance name.

Albeit the suffix is ':zerg' this does not mean you need to use zerg mode. A 'zerg' instance could be a completely independent one simply subscribing
to a router, or binding to a SO_REUSEPORT socket.
