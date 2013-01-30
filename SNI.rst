SNI - Server Name Identification or VirtualHosting for your ssl nodes 
=====================================================================

uWSGI 1.5 (aka: ssl as p0rn) added support for SNI (Server Name Identification) to the whole
ssl subsystem. The HTTPS router, the SPDY router and the SSL router can use it transparently.

SNI is an extension to the ssl standard, allowing a client to specify a "name" for the resource
it wants. That name is generally the requested hostname, so you can implement a virtualhosting-like behaviour
(like you do using the HTTP Host: header)

In uWSGI a sni object is composed by a name and a value. The name is the servername/hostname while the value is the SSL Context
(you can see it as the sum of certificates,key and cihpers for a particular domain).

Adding SNI objects
******************

To add a sni object just use the --sni opion:

.. code-block:: sh

   --sni <name> crt,key[,ciphers,client_ca]

Example:

.. code-block:: sh

   --sni unbit.com unbit.crt,unbit.key

or (for client based ssl authentication and HIGH ciphers)

.. code-block:: sh

   --sni secure.unbit.com unbit.crt,unbit.key,HIGH,unbit.ca

Adding complex SNI objects
**************************

Sometimes you need more complex keys for your SNI objects (like with wildcard certificates)

If you have built uWSGI with pcre/regexp support you can use the --sni-regexp option

.. code-block:: sh

   --sni *.unbit.com unbit.crt,unbit.key,HIGH,unbit.ca

Massive SNI hosting
*******************

uWSGI main purpose is massive hosting, so ssl without that feature would be pretty annoying.

If you have dozens (or hundreds...) of certificates mapped to the same ip you can simply put them in a directory (follwing a
simple convention) and let uWSGI to scan it whenever it need to add a new context for a domain.

To add a directory just use

.. code-block:: sh

   --sni-dir <path>

like

.. code-block:: sh

   --sni-dir /etc/customers/certificates

Now if you have unbit.com and example.com certificates and keys just drop them following that naming rules:

/etc/customers/certificates/unbit.com.crt

/etc/customers/certificates/unbit.com.key

/etc/customers/certificates/unbit.com.ca

/etc/customers/certificates/example.com.crt

/etc/customers/certificates/example.com.key


as you can see example.com has no .ca file, so client authentication will be disabled for it.

If you want to force a default ciphers set to the sni contexts just use

.. code-block:: sh

   --sni-dir-ciphers HIGH

or whatever value you need

Notes
*****

Unloading sni objects is not supported, once you load them in memory they will be hold til reload.
