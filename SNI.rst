SNI - Server Name Identification or VirtualHosting for your ssl nodes 
=====================================================================

uWSGI 1.5 (aka: ssl as p0rn) added support for SNI (Server Name Identification) to the whole
ssl subsystem. The HTTPS router, the SPDY router and the SSL router can use it transparently.

SNI is an extension to the ssl standard, allowing a client to specify a "name" for the resource
it wants. That name is generally the requested hostname, so you can implement a virtualhosting-like behaviour
(like you do using the HTTP Host: header)

In uWSGI a sni object is composed by a name and a value. The name is the servername/hostname while the value is the SSL Context
(you can see it as the sum of certificates,key and cihpers for a particular domain).

To add a sni object just use the --sni opion:

..parsed-literal:
   --sni <name> crt,key[,ciphers,client_ca]

Example:

..parsed-literal:
   --sni unbit.com unbit.crt,unbit.key

or (for client based ssl authentication)

..parsed-literal:
   --sni secure.unbit.com unbit.crt,unbit.key,HIGH,unbit.ca
