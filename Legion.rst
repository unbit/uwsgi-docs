The uWSGI Legion subsystem (1.5-dev)
====================================

Starting from uWSGI 1.5-dev a new subsystem for clustering has been added: The Legion subsystem.

A Legion is a group of uWSGI nodes constantly fighting for domination.

Each node has a valor (different from the others). 

The node with the higher valor is the Lord of the Legion (or if you like a more engineer-friendly term: the master)

This constant fight generates 4 kind of events: start of the fight (setup), end of the fight (death), becoming a lord (lord), loosing the lord title (unlord).

You can trigger actions every time such an event rises, and this should switch-on the light on your brain.

Still confused ?
****************

An example, as always is the best approach for learning:

Ip Takeover
^^^^^^^^^^^

This is probably the king of all of the example, as this is a very common needs in clustered environments.

The ip address is a resource that must be owned by only one node (i suppose you know what could happens otherwise...).

That node is our Lord.

If we configure a Legion right (remember, a single uWSGI instances can be a member of all of the legions you need) we
could easily implement ip takeover.

.. code-block: ini

   [uwsgi]
   legion-freq = 1
   legion-tolerance = 3
   legion = clusterip 225.1.1.1:4242 98 bf-cbc:hello
   legion-node = clusterip 225.1.1.1:4242

   legion-lord = clusterip cmd:ip addr add 192.168.173.111/24 dev eth0
   legion-lord = clusterip cmd:arping -c 3 -S 192.168.173.111 192.168.173.1

   legion-setup = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0
   legion-unlord = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0
   legion-death = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0

