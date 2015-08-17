On demand vassals via subscriptions
===================================

Spawn an Emperor with a command socket (it is a channel allowing external process to govern vassals)

.. code-block:: ini

   [uwsgi]
   emperor = /etc/uwsgi/vassals
   emperor-command-socket = /run/emperor.socket
