The TunTap Router
=================

The TunTap router is an ad-hoc solution for giving network connectivity to Linux processes running in a dedicated network namespace (well obviously it has other uses, but very probably this is the most interesting one, and the one for which it was developed)


The TunTap router is not compiled in by default.


For having it in one shot:

.. code-block:: sh

   UWSGI_EMBED_PLUGINS=tuntap make
   
(yes the plugin is named only 'tuntap' as effectively it exposes various tuntap devices features)

The best way to use it is binding it to a unix socket, allowing processes in new namespaces to reach it (generally unix sockets are the best communication channel for linux namespaces).


The first config
****************

We want our vassals to live in the 192.168.0.0/24 network, with 192.168.0.1 as default gateway.

The default gateway (read: the tuntap router) is managed by the Emperor itself

.. code-block:: ini

   [uwsgi]
   ; create the tun device 'emperor0' and bind it to a unix socket
   tuntap-router = emperor0 /tmp/tuntap.socket
   ; give it an ip address
   exec-as-root = ifconfig emperor0 192.168.0.1 netmask 255.255.255.0 up
   ; setup nat
   exec-as-root = iptables -t nat -F
   exec-as-root = iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
   ; enable linux ip forwarding
   exec-as-root = echo 1 >/proc/sys/net/ipv4/ip_forward
   ; force vassals to be created in a new network namespace
   emperor-use-clone = net
   emperor = /etc/vassals
   
The vassals spawned by this Emperor will born without network connectivity.

To give them access to the public network we create a new tun device (it will exist only in the vassal network namespace)
instructing it to route traffic to the Emperor tuntap unix socket:

.. code-block:: ini

   [uwsgi]
   ; create uwsgi0 tun interface and force it to connect to the Emperor exposed unix socket
   tuntap-device = uwsgi0 /tmp/tuntap.socket
   ; bring up loopback
   exec-as-root = ifconfig lo up
   ; bring up interface uwsgi0
   exec-as-root = ifconfig uwsgi0 192.168.0.2 netmask 255.255.255.0 up
   ; and set the default gateway
   exec-as-root = route add default gw 192.168.0.1
   ; classic options
   uid = customer001
   gid = customer001
   socket = /var/www/foobar.socket
   psgi-file = foobar.pl
   ...
