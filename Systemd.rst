Systemd
=======

uWSGI is a new-style daemon for `systemd <http://www.freedesktop.org/wiki/Software/systemd>`_.

It can notify status change and readyness.

When uWSGI detects it is running under systemd, the notification system is enabled.

Adding the Emperor to systemd
*****************************

The best approach to integrate uWSGI apps with your init system is using the :doc:`Emperor<Emperor>`.

Your init system will talk only with the Emperor that will rule all of the apps itself.

Create a systemd service file (you can save it as /etc/systemd/system/emperor.uwsgi.service)

.. code-block:: ini

   [Unit]
   Description=uWSGI Emperor
   After=syslog.target

   [Service]
   ExecStart=/root/uwsgi/uwsgi --ini /etc/uwsgi/emperor.ini
   Restart=always
   KillSignal=SIGQUIT
   Type=notify
   StandardError=syslog
   NotifyAccess=main

   [Install]
   WantedBy=multi-user.target

Then run it

.. code-block:: sh

   systemctl start emperor.uwsgi.service

And check its status.

.. code-block:: sh

   systemctl status emperor.uwsgi.service

You will see the Emperor reporting the number of governed vassals to systemd (and to you).

.. code-block:: sh

   emperor.uwsgi.service - uWSGI Emperor
    Loaded: loaded (/etc/systemd/system/emperor.uwsgi.service)
	  Active: active (running) since Tue, 17 May 2011 08:51:31 +0200; 5s ago
   Main PID: 30567 (uwsgi)
	  Status: "The Emperor is governing 1 vassals"
	  CGroup: name=systemd:/system/emperor.uwsgi.service
		  ├ 30567 /root/uwsgi/uwsgi --ini /etc/uwsgi/emperor.ini
		  ├ 30568 /root/uwsgi/uwsgi --ini werkzeug.ini
		  └ 30569 /root/uwsgi/uwsgi --ini werkzeug.ini


You can stop the Emperor (and all the apps it governs) with

.. code-block:: sh

   systemctl stop emperor.uwsgi.service

A simple ``emperor.ini`` could look like this (www-data is just an anonymous user)

NOTE: DO NOT daemonize the Emperor (or the master) unless you know what you are doing!!!

.. code-block:: ini

   [uwsgi]
   emperor = /etc/uwsgi/vassals
   uid = www-data
   gid = www-data

If you want to allow each vassal to run under different privileges, remove the ``uid`` and ``gid`` options from the emperor configuration (and please read the Emperor docs!)

Logging
*******

Using the previous service file all of the Emperor messages go to the syslog. You can avoid it by removing the ``StandardError=syslog`` directive.

If you do that, be sure to set a ``--logto`` option in your Emperor configuration, otherwise all of your logs will be lost!

Putting sockets in /run/
************************

On a modern system, /run/ is mounted as a tmpfs and is the right place to put sockets and pidfiles into. You can have systemd create a uwsgi directory to put them into by creating a systemd-tmpfiles configuration file (you can save it as /etc/tmpfiles.d/emperor.uwsgi.conf):

.. code-block:: ini

   d /run/uwsgi 0755 www-data www-data -

Socket activation
*****************

Starting from uWSGI 0.9.8.3 socket activation is available. You can setup systemd to spawn uWSGI instances only after the first socket connection.

Create the required emperor.uwsgi.socket (in ``/etc/systemd/system/emperor.uwsgi.socket``). Note that the *.socket file name must match the *.service file name.

.. code-block:: ini

   [Unit]
   Description=Socket for uWSGI Emperor

   [Socket]
   # Change this to your uwsgi application port or unix socket location
   ListenStream=/tmp/uwsgid.sock

   [Install]
   WantedBy=sockets.target

Then disable the service and enable the socket unit.

.. code-block:: sh

   # systemctl disable emperor.uwsgi.service
   # systemctl enable emperor.uwsgi.socket
