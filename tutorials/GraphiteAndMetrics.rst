Setting up Graphite on Ubuntu using the Metrics subsystem
=========================================================

This tutorial will guide you in installing a multi-app server, with each application sending metrics to a central graphite/carbon server.

Graphite is available here: http://graphite.wikidot.com/

The uWSGI Metrics subsystem is documented here: :doc:`Metrics`

The tutorial assumes an Ubuntu Saucy (13.10) release on amd64

While for Graphite we will use Ubuntu official packages, uWSGI core and plugins will be downloaded and installed from official sources

Installing Graphite and the others needed packages
**************************************************

.. code-block:: sh

   sudo apt-get install python-dev ruby-dev build-essential libpcre3-dev graphite-carbon graphite-web
   
python-dev and ruby-dev are required as we want to support both WSGI and Rack apps.

pcre development headers allow you to build uWSGI with internal routing support (something you always want)

Initializing Graphite
*********************

The first step will be enabling th Carbon server.

The Graphite project is composed by three subsystems: whisper, carbon and the web frontend

Whisper is a data storage format (similar to rrdtool)

Carbon is the server gathering metrics and storing in whisper (well it does more, but this is its main purpose)

The web frontend visualize the charts/graphs built from the data gathered by the carbon server.

To enable the carbon server edit ``/etc/default/graphite-carbon`` and set CARBON_CACHE_ENABLED to true

Before starting the carbon server we need to build its search index.

Just run:

.. code-block:: sh

   sudo /usr/bin/graphite-build-search-index

Then start the carbon server (at the next reboot it will be automatically started)

.. code-block:: sh

   sudo /etc/init.d/carbon-cache start

Building and Installing uWSGI
*****************************

Download latest stable uWSGI tarball

.. code-block:: sh

   wget http://projects.unbit.it/downloads/uwsgi-latest.tar.gz
   
explode it, and from the created directory run:

.. code-block::

   python uwsgiconfig.py --build core
   
this will build the uWSGI "core" binary.

We now want to build the python, rack and carbon plugins:

.. code-block::

   python uwsgiconfig.py --plugin plugins/python core
   python uwsgiconfig.py --plugin plugins/rack core
   python uwsgiconfig.py --plugin plugins/carbon core
   
   
now we have ``uwsgi``, ``python_plugin.so``, ``rack_plugin.so`` and ``carbon_plugin.so``

let's copy it to system directories:

.. code-block:: sh

   sudo mkdir /etc/uwsgi
   sudo mkdir /usr/lib/uwsgi
   sudo cp uwsgi /usr/bin/uwsgi
   sudo cp python_plugin.so /usr/lib/uwsgi
   sudo cp rack_plugin.so /usr/lib/uwsgi
   sudo cp carbon_plugin.so /usr/lib/uwsgi

Setting up the uWSGI Emperor
****************************

Create an upstart config file for starting :doc:`Emperor`.

.. code-block:: sh

   # Emperor uWSGI script

   description "uWSGI Emperor"
   start on runlevel [2345]
   stop on runlevel [06]

   exec /usr/bin/uwsgi --emperor /etc/uwsgi
   
save it as ``/etc/init/emperor.conf`` and start the Emperor:

.. code-block::

   start emperor
   
   
From now on, to start uWSGI instances just drop their config files into /etc/uwsgi

Spawning the Graphite web interface
***********************************

Before starting the graphite web interface (that is a Django app) we need to initialize its database.

Just run:

.. code-block:: sh

   sudo graphite-manage syncdb
   
this is the standard django syncdb command for manage.py. Just answer the questions to create an admin user.

Now we are ready to create a uWSGI vassal:

.. code-block:: ini

   [uwsgi]
   plugins-dir = /usr/lib/uwsgi
   plugins = python
   uid = _graphite
   gid = _graphite
   wsgi-file = /usr/share/graphite-web/graphite.wsgi
   http-socket = :8080
   
Save it as ``/etc/uwsgi/graphite.ini``
   
the _graphite user (and group) is create by the ubuntu package. Our uWSGI vassal will run under this privileges.

The web interface will be available on the port 8080 of your server natively speaking HTTP. If you prefer to proxy it,
just change ``http-socket`` to ``http`` or place it behind a full webserver like nginx (this step is not covered in this tutorial)


Spawning vassals sending metrics to Graphite
********************************************

Using Graphiti (Ruby/Sinatra based) as alternative frontend
***********************************************************

Notes
*****
