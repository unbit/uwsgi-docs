uWSGI 2.0.6
===========

Changelog [20140701]


Bugfixes
^^^^^^^^

* fixed a memory leak with subscription system
* fixed shortcut for ssl-socket
* fixed apache2 mod_proxy_uwsgi (it is now considered stable with all mpm engines)
* fixed SCRIPT_NAME and PATH_TRANSLATED generation in php plugin (thanks Matthijs Kooijman)
* remove the old FIFO socket from the event queue when recreating it (thanks Marko Tiikkaja)


New features
^^^^^^^^^^^^

The new Rados plugins
*********************

Credits: Marcin Deranek

The rados plugin has been improved and stabilized, and now it is considered usable in production.

Async modes and multithreading correctly works, and support for uploading objects (via PUT) and creating new pools (MKCOL)
has been added.

Expect webdav support in uWSGI 2.1

Docs have been updated: http://uwsgi-docs.readthedocs.org/en/latest/Rados.html

--if-hostname
*************

This is a configuration logic for including options only when the specified hostname matches:

.. code-block:: ini

   [uwsgi]
   if-hostname = node1.local
     socket = /tmp/socket1.socket
   endif =
   
   if-hostname = node2.local
     socket = /var/run/foo.socket
   endif = 
   
Apache2 mod_proxy_uwsgi stabilization
*************************************

After literally years of bug reports, and corrupted data, the mod_proxy_uwsgi is now stable, and on modern
apache2 releases it supports unix sockets too.

Updated docs: http://uwsgi-docs.readthedocs.org/en/latest/Apache.html#mod-proxy-uwsgi

uwsgi[rsize] routing var
************************

this routing var (meaningful only in the 'final' chain) exposes the response size of the request

the callint scheme
******************

This scheme allows you to generate blob from functions exposed by your uWSGI instance:

.. code-block:: ini

   [uwsgi]
   uid = @(callint://get_my_uid)
   gid = @(callint://get_my_gid)
   
--fastrouter-fallback-on-no-key
*******************************

The corerouters fallback procedure requires a valid key (domain name) has been requested. This option forces the various routers
to trigger the fallback procedure even if a key has not been found.

php 5.5 opcode caching via --php-sapi-name
******************************************

For mysterious reasons the opcode caching of php5.5 is not enabled in the embed sapi. This option (set it to 'apache' if you want) allows you to fake the opcode caching engine forcing it to enable itself.

Improved chain-reloading
************************

Thanks to Marko Tiikkaja the chain reloading procedure correctly works in cheaper modes and it is more verbose.

added 'chdir' keyval to --attach-daemon2
****************************************

You can now set where attached daemons need to chdir()

Availability
^^^^^^^^^^^^

uWSGI 2.0.6 has been released on 20140701

You can download it from

http://projects.unbit.it/downloads/uwsgi-2.0.6.tar.gz
