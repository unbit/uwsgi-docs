uWSGI 1.9.7
===========


Bugfixes
********

- fixed teajs engine build

- fixed offloading status code (set to 202 when a request is offloaded)

- execute cron tasks within 60 second resolution, instead of 61 seconds

- fixed websocket proxy

- check for python3 unicode encoding (instead of crashing...)

- fixed ipcsem removal on reload

- fixed kqueue timer on OpenBSD, NetBSD and DragonFlyBSD

- fixed/reimplemented perl uwsgi::register_rpc

- fixed fd leak on sendfile() error

- fixed Content-Length when gzip file variant is used

- allows non-request plugins to register rpc functions

- more robust error checking for cgroups


New features
************


Legion cron
^^^^^^^^^^^

A common needs when multiple instances of an application are running, is to force only one
of them to run cron tasks. The new --legion-cron uses :doc:`Legion` to accomplish that:

.. code-block:: ini

   [uwsgi]
   ; use the new legion-mcast shortcut (with a valor 90)
   legion-mcast = mylegion 225.1.1.1:9191 90 bf-cbc:mysecret
   ; run the script only if the instance is the lord of the legion "mylegion"
   legion-cron = mylegion -1 -1 -1 -1 -1 my_script.sh


Curl cron
^^^^^^^^^

The curl_cron plugin has been added allowing the cron subsystem to call urls (via libcurl) instead of unix commands:

.. code-block:: ini

   [uwsgi]
   ; call http://uwsgi.it every minute
   curl-cron = -1 -1 -1 -1 -1 http://uwsgi.it/

The output of the request is reported in the log

Gzip caching
^^^^^^^^^^^^

--skip-atexit
^^^^^^^^^^^^^

proxyhttp and proxyuwsgi
^^^^^^^^^^^^^^^^^^^^^^^^

The transformation api
^^^^^^^^^^^^^^^^^^^^^^

--alarm-fd
^^^^^^^^^^

The spooler server plugin and the cheaper busyness algorithm compiled in by default
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
