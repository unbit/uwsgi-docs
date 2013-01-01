The uWSGI Legion subsystem (1.5-dev)
====================================

Starting from uWSGI 1.5-dev a new subsystem for clustering has been added: The Legion subsystem.

A Legion is a group of uWSGI nodes constantly fighting for domination.

Each node has a valor (different from the others, if possible). 

The node with the higher valor is the Lord of the Legion (or if you like a more engineer-friendly term: the master)

This constant fight generates 4 kind of events: start of the fight (setup), end of the fight (death), becoming a lord (lord), loosing the lord title (unlord).

You can trigger actions every time such an event rises, and this should switch-on the light on your brain...

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

.. code-block:: ini

   [uwsgi]

   legion = clusterip 225.1.1.1:4242 98 bf-cbc:hello
   legion-node = clusterip 225.1.1.1:4242

   legion-lord = clusterip cmd:ip addr add 192.168.173.111/24 dev eth0
   legion-lord = clusterip cmd:arping -c 3 -S 192.168.173.111 192.168.173.1

   legion-setup = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0
   legion-unlord = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0
   legion-death = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0

In this example we join a legion named 'clusterip'. To receive messages from the other nodes we bind on (multicast) address
225.1.1.1:4242. The valor of this node will be 98 and each message will be encrypted using blowfish cbc with the secret 'hello'.

The 'legion-node' option specify the destination of our announce messages. As we are using multicast we only need to specify a single node.

The last options are the actions to trigger on the various state of the cluster. For an ip takeover solution we seimply rely on iproute commands
to set/unset ip addresses and to send gratuitous arp.

The Quorum
**********

To choose a Lord each member of the legion has to cast a vote. When all of the active members of a legion agree on a Lord, the Lord is elected (and the old Lord degraded).

Every time a new node joins or leaves a legion the quorum is re-computed and logged to the whole nodes.

Choosing the Lord
*****************

Generally the node with the higher valor is choosen as the Lord, but there can be cases where different nodes have the same valor.
When a node is started a UUID is assigned to it. If two nodes with same valor are found the one with the lexycographically higher UUID wins

Split brain
***********

Even if each member of the Legion has to send a checksum of its internal cluster-membership (no quorum is reached if not all nodes have the same checksum)
the system is still vulnerable to the split brain problem. If a node lose network connectivity with the cluster, it could believe it is the only node available and starts
going in Lord mode.

For some scenario this is bad, so if you have more than 2 nodes in a legion you may want to consider tuning the quorum level.
The quorum level is the amount of votes (from different nodes) to receive needed to elect a lord. 

You can reduce the split brain problem asking the Legion subsystem to check for at least 2 votes:

.. code-block:: ini

   [uwsgi]

   legion = clusterip 225.1.1.1:4242 98 bf-cbc:hello
   legion-node = clusterip 225.1.1.1:4242

   legion-quorum = clusterip 2

   legion-lord = clusterip cmd:ip addr add 192.168.173.111/24 dev eth0
   legion-lord = clusterip cmd:arping -c 3 -S 192.168.173.111 192.168.173.1

   legion-setup = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0
   legion-unlord = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0
   legion-death = clusterip cmd:ip addr del 192.168.173.111/24 dev eth0


The legion-quorum is the option for the job

Actions
*******

Each one of the four phases of a legion (setup,death,lord,unlord) can trigger an action. The actions system is modular so you can
add new kind of actions.

Currently the supported actions are:

cmd:<command>
-------------

run a shell command

signal:<num>
------------

raise a uWSGI signal

log:<msg>
---------

log a message

For example you could combine the log action with the alarm subsystem to have cluster monitoring for free...
