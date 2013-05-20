uWSGI Subscription Server
=========================

Some components of the uWSGI stack require a key-value mapping system.

For example the :doc:`FastRouter<FastRouter>` needs to know which server to contact for a specific request.

In big networks with a lot of nodes manually managing this configuration could be a proper pain in the ass.
As uWSGI doesn't want to be a PITA, it implements a subscription system where the node itself announces its presence to Subscription Servers, which will in turn populate their internal dictionaries.

.. code-block:: sh

    uwsgi --fastrouter :1717 --fastrouter-subscription-server 192.168.0.100:2626

This will run an uWSGI fastrouter on port 1717 and create an empty dictionary where the hostname is the key and the uwsgi address is the value.

To populate this dictionary you can contact 192.168.0.100:2626, the address of the subscription server.

For every key multiple addresses can exist, enabling round robin load balancing.

A node can announce its presence to a Subscription Server using the ``subscribe-to`` or ``subscribe2`` options.

.. code-block:: sh

    uwsgi -s 192.168.0.10:3031 -w myapp -M --subscribe-to 192.168.0.100:2626:uwsgi.it

The FastRouter will map every request for uwsgi.it to 192.168.0.10:3031.

To now add a second node for uwsgi.it simply run it and subscribe:

.. code-block:: xxx

    uwsgi -s 192.168.0.11:3031 -w myapp -M --subscribe-to 192.168.0.100:2626:uwsgi.it

Dead nodes are automatically removed from the pool.

The syntax for ``subscribe2`` is similar but it allows far more control since it allows to specify additional options like the address to which all requests should be forwarded. Its value syntax is a string with "key=value" pairs, each separated by a comma.

.. code-block:: sh

    uwsgi -s 192.168.0.10:3031 -w myapp -M --subscribe2 server=192.168.0.100:2626,key=uwsgi.it,addr=192.168.0.10:3031

Possible keys are:

  * ``server`` - address (ip:port) of the subscription server we want to connect to
  * ``key`` - key used for mapping, hostname (FastRouter or HttpRouter) or ip:port (RawRouter)
  * ``socket`` - TODO
  * ``addr`` - address to which all requests should be forwared for this subscription
  * ``weight`` - node weight for load balancing
  * ``modifier1`` - modifier1 value for our app
  * ``modifier2`` - modifier2 value for our app
  * ``sign`` - TODO
  * ``check`` - TODO

The subscription system is currently available for cluster joining (when multicast/broadcast is not available), the Fastrouter and HTTP.

That said, you can create an evented/fast_as_hell HTTP load balancer in no time.

.. code-block:: sh

    uwsgi --http :80 --http-subscription-server 192.168.0.100:2626

Now simply subscribe your nodes to the HTTP subscription server.

Securing the Subscription System
--------------------------------

The subscription system is meant for "trusted" networks. All of the nodes in your network can potentially make one goddamn mess with it.

If you are building an infrastructure for untrusted users or you simply need more control over who can subscribe to a Subscription Server you can use openssl rsa public/private key pairs for "signing" you subscription requests.

.. code-block:: sh

    # First, create the private key for the subscriber. DO NOT SET A PASSPHRASE FOR THIS KEY.
    openssl genrsa -out private.pem
    # Generate the public key for the subscription server:
    openssl rsa -pubout -out test.uwsgi.it_8000.pem -in private.pem

The keys must be named after the domain/key we are subscribing to serve, plus the .pem extension.

.. note:: If you're subscribing to a pool for an application listening on a specified port you need to use the ``domain_port.pem`` scheme for your key files. Generally all of the DNS-allowed chars are supported, all of the others are mapped to an underscore.

An example of an RSA protected server looks like this:

.. code-block:: ini

    [uwsgi]
    master = 1
    http = :8000
    http-subscription-server = 127.0.0.1:2626
    subscriptions-sign-check = SHA1:/etc/uwsgi/keys

The last line tells uWSGI that public key files will be stored in /etc/uwsgi/keys.

At each subscription request the server will check for the availability of the public key file and use it, if available, to verify the signature of the packet. Packets that do not correctly verify are rejected.

On the client side you need to pass your private key along with other ``subscribe-to`` options. Here's an example:

.. code-block:: ini

    [uwsgi]
    socket = 127.0.0.1:8080
    subscribe-to = 127.0.0.1:2626:test.uwsgi.it:8000,5,SHA1:/home/foobar/private.pem
    psgi = test.psgi

Let's analyze the ``subscribe-to`` incantation:

* ``127.0.0.1:2626`` is the subscription server we want to subscribe to.
* ``test.uwsgi.it:8000`` is the subscription key.
* ``5`` is the modifier1 value for our psgi app
* ``SHA1:/home/private/test.uwsgi.it_8000.pem`` is the <digest>:<rsa> couple for authenticating to the server (the <rsa> field is the private key path).

.. note:: Please make sure you're using the same digest method (SHA1 in the examples above) both on the server and on the client.

To avoid replay attacks, each subscription packet has an increasing number (normally the unix time) avoiding the allowance of duplicated packets.
Even if an attacker manages to sniff a subscription packet it will be unusable as it is already processed previously.
Obviously if someone manages to steal your private key he will be able to build forged packets.
