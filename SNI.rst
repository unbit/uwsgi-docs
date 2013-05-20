SNI - Server Name Identification (virtual hosting for SSL nodes)
================================================================

uWSGI 1.9 (codenamed "ssl as p0rn") added support for SNI (Server Name Identification) throughout the whole
SSL subsystem. The HTTPS router, the SPDY router and the SSL router can all use it transparently.

SNI is an extension to the SSL standard which allows a client to specify a "name" for the resource
it wants. That name is generally the requested hostname, so you can implement virtual hosting-like behavior like you do using the HTTP ``Host:`` header without requiring extra IP addresses etc.

In uWSGI an SNI object is composed of a name and a value. The name is the servername/hostname while the value is the "SSL context" (you can think of it as the sum of certificates, key and ciphers for a particular domain).

Adding SNI objects
******************

To add an SNI object just use the ``--sni`` option:

.. code-block:: sh

   --sni <name> crt,key[,ciphers,client_ca]

For example:

.. code-block:: sh

   --sni unbit.com unbit.crt,unbit.key

or for client-based SSL authentication and OpenSSL HIGH cipher levels

.. code-block:: sh

   --sni secure.unbit.com unbit.crt,unbit.key,HIGH,unbit.ca

Adding complex SNI objects
**************************

Sometimes you need more complex keys for your SNI objects (like when using wildcard certificates)

If you have built uWSGI with PCRE/regexp support (as you should) you can use the ``--sni-regexp`` option.

.. code-block:: sh

   --sni-regexp *.unbit.com unbit.crt,unbit.key,HIGH,unbit.ca

Massive SNI hosting
*******************

One of uWSGI's main purposes is massive hosting, so SSL without support for that would be pretty annoying.

If you have dozens (or hundreds, for that matter) of certificates mapped to the same IP address you can simply put them in a directory (following a simple convention we'll elaborate in a bit) and let uWSGI scan it whenever it needs to find a context for a domain.

To add a directory just use

.. code-block:: sh

   --sni-dir <path>

like

.. code-block:: sh

   --sni-dir /etc/customers/certificates

Now, if you have ``unbit.com`` and ``example.com`` certificates (.crt) and keys (.key) just drop them in there following these naming rules:

* ``/etc/customers/certificates/unbit.com.crt``
* ``/etc/customers/certificates/unbit.com.key``
* ``/etc/customers/certificates/unbit.com.ca``
* ``/etc/customers/certificates/example.com.crt``
* ``/etc/customers/certificates/example.com.key``

As you can see, ``example.com`` has no .ca file, so client authentication will be disabled for it.

If you want to force a default cipher set to the SNI contexts, use

.. code-block:: sh

   --sni-dir-ciphers HIGH

(or whatever other value you need)

Notes
*****

* Unloading SNI objects is not supported. Once they are loaded into memory they will be held onto until reload.
