The PyPy plugin
===============

Idea/Design: Maciej Fijalkowski

Contributors: Alex Gaynor, Armin Rigo

Since uWSGI 1.9.11 a new pypy plugin based on cffi is available. The old one, based on (slow) cpyext has been removed
from the tree.

The plugin is currently supported only on Linux systems. Next releases will support other systems as well.

The plugin load libpypy-s.so on startup, set the home of the pypy installation and execute a special python module
implementing the plugin logic. Yes, the 90% of the plugin is implemented in python, and theoretically this apparoach will allows
writing uWSGI plugin directly in python (in addition to C,C++ and Objective C)

Currently (May 2013) all of the required patches are available into pypy official tip (on bitbucket) but binary packages/tarballs
are not available, so you need to build/translate libpypy-c by yourself, or download one of the following files (they require libssl 1.0):

Linux x86 32bit: http://projects.unbit.it/downloads/pypy/libpypy-c-x86_32_20130524.so

Linux x86 32bit (with debug symbols): http://projects.unbit.it/downloads/pypy/libpypy-c-x86_32_20130524-dbg.so

Linux x86 64bit: http://projects.unbit.it/downloads/pypy/libpypy-c-x86_64_20130524.so

Linux x86 64bit (with debug symbols): http://projects.unbit.it/downloads/pypy/libpypy-c-x86_64_20130524-dbg.so

In addition to the library you need to download a nightly build (use the jitted one obviously) from the pypy website. You will use
this directory as the pypy home (see below)

Building libpypy-c (if needed)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Get the pypy mercurial tip from bitbucket and translate it (it should require no more than 50 minutes, but be sure to have at least 2GB of free memory for 32 bit and 4GB for 64bit):

.. code-block:: sh

   ./rpython/bin/rpython -Ojit --shared --gcrootfinder=shadowstack pypy/goal/targetpypystandalone
   

Install uWSGI with PyPy support
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

As always you have different ways to install uWSGI based on your needs.

If you have installed pip in your pypy home just run:

.. code-block:: sh

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
  
With this command line uWSGI will search for libpypy-c.so in /opt/pypy and if found, it will set it as the pypy home too.

If your libpypy-c.so is outsize of the pypy home (and in a directory not reachable by the dynamic linker), you can use the --pypy-lib option:

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-lib /opt/libs/libpypy-c.so
   
With this approach you are able to use library from a specific pypy build and home from another one

Remember to prefix --pypy-lib with ./ if you want to point to a .so file in your current directory !!!

The PyPy setup file
^^^^^^^^^^^^^^^^^^^

As said before, the 90% of the uWSGI pypy plugin is written in python. This code is loaded at runtime, and you can even customize it.

Yes, it means you can change the way the plugin works without rebuilding uWSGI !

The pypy_setup.py file is embedded in the uWSGI binary, and it is automatically loaded on startup.

If you want to change it, just pass another script via the --pypy-setup option

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-lib /opt/libs/libpypy-c.so --pypy-setup /home/foobar/foo.py
   
This python module implements uWSGI hooks and the virtual uwsgi python module (for accessing the uwsgi api from your apps)

If you want to get the content of the embedded pypy_setup.py file you can read it from the binary symbols:

.. code-block:: sh

   uwsgi --print-sym uwsgi_pypy_setup

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
   
To call rpc functions you have both uwsgi.rpc and uwsgi.call:

.. code-block:: py

   import uwsgi
   
   uwsgi.rpc('192.168.173.100:3031', 'myfunc', 'myarg')
   uwsgi.call('myfunc', 'myarg')
   uwsgi.call('myfunc@192.168.173.100:3031', 'myarg')
   
   
Currently we have tested integeration (when rpc is used 'locally') between pypy/pypy pypy/jvm and pypy/lua

All worked flawlessly, that means you can call java functions from pypy ;)

IPython trick
^^^^^^^^^^^^^

Having a runtime shell for making tests is a very handy option. You can use IPython:

.. code-block:: sh

   uwsgi --socket :3031 --pypy-home /opt/pypy --pypy-eval "import IPython; IPython.embed()" --honour-stdin
   
   
uWSGI API status
^^^^^^^^^^^^^^^^

The following api functions, hooks and attributes are supported (updated to 20130526)

uwsgi.opt

uwsgi.post_fork_hook

uwsgi.add_cron()

uwsgi.setprocname()

uwsgi.alarm()

uwsgi.signal_registered()

uwsgi.mule_id()

uwsgi.worker_id()

uwsgi.masterpid()

uwsgi.lock()

uwsgi.unlock()

uwsgi.add_file_monitor()

uwsgi.add_timer()

uwsgi.add_rb_timer()

uwsgi.cache_get()

uwsgi.cache_set()

uwsgi.cache_update()

uwsgi.cache_del()

uwsgi.signal()

uwsgi.call()

uwsgi.rpc()

uwsgi.register_rpc()

uwsgi.register_signal()
   
Options
^^^^^^^

```pypy-lib```   load the specified libpypy-s.so

```pypy-setup``` load the specified pypy_setup script file

```pypy-home```  set the pypy home

```pypy-wsgi```  load a WSGI module

```pypy-wsgi-file```   load a mod_wsgi compliant wsgi file

```pypy-eval```   execute the specified string before fork()

```pypy-eval-post-fork```   execute the specified string after each fork()

```pypy-exec```   execute the specified python script before fork()

```pypy-exec-post-fork```   execute the specified python script after each fork()

```pypy-pp/pypy-python-path/pypy-pythonpath``` add the specified item to the pythonpath
   

Notes
^^^^^

Mixing libpython with libpypy-c is FORBIDDEN. A check in the pypy plugin prevent you from doing such hellish thing.

The PyPy plugin is generally more "orthodox" from the Python programmer point of view (while the Python one is blasphemous in lot of areas). We have been able to make that choice as we do not need
backward compatibility with older uWSGI releases.

The uwsgi API is still incomplete.

The WSGI loader does not update the uWSGI internal application list, so things like --need-app will not work. The server will report "dynamic mode" on startup even if the app
has been successfully loaded. This will be fixed soon.   
