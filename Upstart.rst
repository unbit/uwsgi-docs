Running uWSGI via Upstart
=========================

Upstart is the init system of Ubuntu-like distributions.

It is based on declarative configuration files -- not shell scripts of yore -- that are put in the :file:`/etc/init` directory.

A simple script (/etc/init/uwsgi.conf)
--------------------------------------

.. code-block:: upstart

    # simple uWSGI script
    
    description "uwsgi tiny instance"
    start on runlevel [2345]
    stop on runlevel [06]
    
    respawn
    
    exec uwsgi --master --processes 4 --socket :3031 --wsgi-file /var/www/myapp.wsgi
    
Using the Emperor
-----------------

.. seealso:: :doc:`Emperor`

A better approach than init files for each app would be to only start an Emperor via Upstart and let it deal with the rest.

.. code-block:: upstart

    # Emperor uWSGI script
    
    description "uWSGI Emperor"
    start on runlevel [2345]
    stop on runlevel [06]
    
    respawn
    
    exec uwsgi --emperor /etc/uwsgi


.. code-block:: upstart

    # Emperor uWSGI script
    
    description "uWSGI Emperor"
    start on runlevel [2345]
    stop on runlevel [06]
    
    respawn
    
    exec uwsgi --master --emperor /etc/uwsgi

Socket activation (from Ubuntu 12.04)
-------------------------------------

Newer Upstart releases have an Inetd-like feature that lets processes start when connections are made to specific sockets.

You can use this feature to start uWSGI only when a client (or the webserver) first connects to it.

The 'start on socket' directive will trigger the behaviour.

You do not need to specify the socket in uWSGI as it will be passed to it by Upstart itself.

.. code-block:: upstart

    # simple uWSGI script
    
    description "uwsgi tiny instance"
    start on socket PROTO=inet PORT=3031
    stop on runlevel [06]
    
    respawn
    
    exec uwsgi --master --processes 4 --wsgi-file /var/www/myapp.wsgi

