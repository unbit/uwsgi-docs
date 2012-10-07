
Managing external daemons/services with uWSGI (1.3.1)
=====================================================

uWSGI can easily monitor external processes, allowing you to increase reliability and usability of your multi-tier apps.

For example you can manage services like memcached, redis, celery, delayed_job or even a dedicate postgresql instance.

Kind of services
****************

Currently uWSGI supports 3 kinds of processes:

* directly attached (non daemonized)
* pidfile governed (both foreground and daemonized)
* pidfile governed with daemonization management

The first category allows you to directly attach processes to the uWSGI master. When the master dies or it is reloaded
this processes are destroyed. This is the best choice for services that must be flushed whenever the app is restarted.

Pidfile governed processes can survive master death/reload as long as pidfile of those processes is available (and matches a valid pid). This is the best choice
for processes requiring longer persistence and for which a brutal kill could mean loss of datas (like databases).

The last kind of processes is an 'expansion' of the second one. If your process does not support daemonization or writing to pidfile you can let the master do the hard work.
Very few daemons/applications requires that feature, but it could be useful for tiny prototype applications or simply bad-designed ones.



Examples
********

Managing a **memcached** instance in 'dumb' mode (whenever uWSGI is stopped/reloaded memcached is destroyed)

.. code-block:: ini

   [uwsgi]
   master = true
   socket = :3031
   attach-daemon = memcached -p 11311 -u roberto

Managing a **memcached** instance in 'smart' mode (memcached survives uWSGI stop/realod)


.. code-block:: ini

   [uwsgi]
   master = true
   socket = :3031
   smart-attach-daemon = /tmp/memcached.pid memcached -p 11311 -d -P /tmp/memcached.pid -u roberto

Managing 2 **mongodb** instances (smart mode)

.. code-block:: ini

   [uwsgi]
   master = true
   socket = :3031
   smart-attach-daemon = /tmp/mongo1.pid mongod --pidfilepath /tmp/mongo1.pid --dbpath foo1 --port 50001
   smart-attach-daemon = /tmp/mongo2.pid mongod --pidfilepath /tmp/mongo2.pid --dbpath foo2 --port 50002

Managing **PostgreSQL** dedicated-instance (cluster in /db/foobar1)

.. code-block:: ini

   [uwsgi]
   master = true
   socket = :3031
   smart-attach-daemon = /db/foobar1/postmaster.pid /usr/lib/postgresql/9.1/bin/postgres -D /db/foobar1

Managing **celery**

.. code-block:: ini

   [uwsgi]
   master = true
   socket = :3031
   smart-attach-daemon = /tmp/celery.pid celery -A tasks worker --pidfile=/tmp/celery.pid

Managing **delayed_job**

.. code-block:: ini

   [uwsgi]
   master = true
   socket = :3031
   env = RAILS_ENV=production
   rbrequire = bundler/setup
   rack = config.ru
   chdir = /var/apps/foobar
   smart-attach-daemon = %(chdir)/tmp/pids/delayed_job.pid %(chdir)/script/delayed_job start

Managing **dropbear**

When using namespace option you can attach dropbear daemon (lightweight ssh server) to allow you direct access to system inside namespace.
This requires that /dev/pts filesystem is mounted inside namespace and that the user your workers will be running as will have access to /etc/dropbear directory inside namespace.

.. code-block:: ini

   [uwsgi]
   namespace = /ns/001/:testns
   namespace-keep-mount = /dev/pts
   socket = :3031
   exec-as-root = chown -R www-data /etc/dropbear
   attach-daemon = /usr/sbin/dropbear -j -k -p 1022 -E -F -I 300

