The PyPy plugin
===============

Idea/Design: Maciej Fijalkowski

Contributors: Alex Gaynor, Armin Rigo

Since uWSGI 1.9.11 a new pypy plugin based on cffi is available. The old one, base on (slow) cpyext has been removed
from the tree.

The plugin load libpypy-s.so on startup, set the home of the pypy installation and execute a special python module
implementing the plugin logic. Yes, the 90% of the plugin is implemented in python, and theoretically this apparoach will allows
writing uWSGI plugin directly in python (in addition to C,C++ and Objective C)

Currently (May 2013) all of the required patches are available into pypy official tip (on bitbucket) but binary packages/tarballs
are not available, so you need to build/translate libpypy-c by yourself, or download one of the following files:

Linux x86 32bit

Linux x86 64bit

Building libpypy-c (if needed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get the pypy mercurial tip from bitbucket and translate it (it should require no more than 50 minutes, but be sure to have at least 2GB of free memory):

.. code-block:: sh

   ./rpython/bin/rpython -Ojit --shared --gcrootfinder=shadowstack pypy/goal/targetpypystandalone
   

Install uWSGI with PyPy support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As always you have different ways to install uWSGI based on your needs.

If you have installed pip in your pypy home just run:

.. code-block::

  pip install uwsgi
  
The uwsgi setup.py file will recognize the pypy environment and will build a pypy-only uWSGI binary

You can compile manually:

.. code-block:: sh

   UWSGI_PROFILE=pypy make
   
Or you can use the network installer:

.. code-block:: sh

   curl http://uwsgi.it/install | bash -s pypy /tmp/uwsgi
   
it will build a uWSGI+PyPy binary in /tmp/uwsgi

Or you can build the plugin:

.. code-block:: sh

   python uwsgiconfig.py --plugin plugins/pypy
   
The PyPy Home
^^^^^^^^^^^^^

The uWSGI python plugin (the one based on CPython) works by linking libpython. That means you need to rebuild the plugin whenever you want
to use a different python version. The pypy plugin is different, as libpypy-c is loaded on startup and its symbol resolved at runtime, so you can move
to a different pypy version on the fly.

The downside is that you need to inform uWSGI where your PyPy installation is.

Supposing your PyPy is in /opt/pypy you can start uWSGI with:

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy
  
With this command line uWSGI will search fr libpypy-c.so in /opt/pypy and if found, it will set it as the pypy home too.

If your libpypy-c.so is outsize of the pypy home (and in a directory not reachable by the linker), you can use the --pypy-lib option:

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-lib /opt/libs/libpypy-c.so
   
With this approach you are able to use library from a specific pypy build and home from another one

The PyPy setup file
^^^^^^^^^^^^^^^^^^^

As said before, the 90% of the uWSGI pypy plugin is written in python. This code is loaded at runtime, and you can even customize it.

Yes, it means you can change the way the plugin works without rebuilding uWSGI !

The pypy_setup.py file is embedded in the uWSGI binary, and it is automatically loaded on startup.

If you want to change it, just pass another script via the --pypy-setup option

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-lib /opt/libs/libpypy-c.so --pypy-setup /home/foobar/foo.py
   
This python module implements uWSGI hook and the virtual uwsgi python module (for accessing the uwsgi api from your apps)

WSGI support
^^^^^^^^^^^^

The plugin implements PEP 333 and PEP 3333. You can load both wsgi modules and mod_wsgi style wsgi files.

To load a WSGI module (it must be in your pythonpath):

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-wsgi myapp
   
To load a WSGI file:

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-wsgi-file /var/www/myapp/myapp.wsgi
   
RPC support
^^^^^^^^^^^

You can register RPC function using the uwsgi.register_rpc api function (in the same way you do it with the cpython plugin)

.. code-block:: py

   import uwsgi
   
   def hello():
       return "Hello World"
       
   uwsgi.register_rpc('hello', hello)
   
