Using Lua/WSAPI with uWSGI
==========================

Compilation notes
-----------------

Before compiling the plugin take a look at the :file:`plugins/lua/uwsgiplugin.py` configuration file. If you have installed Lua in some exotic directory you may need to adjust the ``CFLAGS`` and ``LIBS`` values.

For example, on a Debian/Ubuntu system you should use something like this:

.. code-block:: python

  import os, sys
  
  NAME='lua'
  CFLAGS = ['-I/usr/include/lua5.1/']
  LDFLAGS = []
  GCC_LIST = ['lua_plugin']
  LIBS = ['-llua5.1']

The ``lua.ini`` buildconf will build uWSGI with embedded Lua support. The ``luap.ini`` buildconf will build Lua support as a plugin.

.. code-block:: sh

  python uwsgiconfig.py --build lua # embedded
  python uwsgiconfig.py --build luap # plugin
  # if you have already build the uWSGI core with the default config file...
  python uwsgiconfig.py --plugin plugins/lua
  # or if you have used another config file (for example core.ini)
  python uwsgiconfig.py --plugin plugins/lua core

Your first WSAPI application
----------------------------

We will use the official WSAPI example, let's call it :file:`pippo.lua`:

.. code-block:: lua

  function hello(wsapi_env)
    local headers = { ["Content-type"] = "text/html" }
    local function hello_text()
      coroutine.yield("<html><body>")
      coroutine.yield("<p>Hello Wsapi!</p>")
      coroutine.yield("<p>PATH_INFO: " .. wsapi_env.PATH_INFO .. "</p>")
      coroutine.yield("<p>SCRIPT_NAME: " .. wsapi_env.SCRIPT_NAME .. "</p>")
      coroutine.yield("</body></html>")
    end
    return 200, headers, coroutine.wrap(hello_text)
  end
  
  return hello

Now run uWSGI with the ``lua`` option (remember to add ``--plugins lua`` as the first command line option if you are using it as a plugin)

.. code-block:: sh

  ./uwsgi -s :3031 -M -p 4 --lua pippo.lua -m

The Lua plugin's official uwsgi protocol modifier number is ``6``, so remember to set it in your web server configuration with the ``uWSGIModifier1``/``uwsgi_modifier1`` directive.

Abusing coroutines
------------------

One of the most exciting feature of Lua is coroutine (cooperative multithreading) support. uWSGI can benefit from this using its async core.

The Lua plugin will initialize a ``lua_State`` for every async core.

We will use a CPU-bound version of our pippo.lua to test it:

.. code-block:: lua

  function hello(wsapi_env)
    local headers = { ["Content-type"] = "text/html" }

    local function hello_text()
      coroutine.yield("<html><body>")
      coroutine.yield("<p>Hello Wsapi!</p>")
      coroutine.yield("<p>PATH_INFO: " .. wsapi_env.PATH_INFO .. "</p>")
      coroutine.yield("<p>SCRIPT_NAME: " .. wsapi_env.SCRIPT_NAME .. "</p>")
      for i=0, 10000, 1 do
          coroutine.yield(i .. "<br/>")
      end
      coroutine.yield("</body></html>")
    end

    return 200, headers, coroutine.wrap(hello_text)
  end

  return hello

and run uWSGI with 8 async cores...

.. code-block:: sh

  ./uwsgi -s :3031 -M -p 4 --lua pippo.lua -m --async 8

And just like that, you can manage 8 concurrent requests within a single worker!

Threading
---------

The Lua plugin is "thread-safe" as uWSGI maps a lua_State to each internal pthread.

For example you can run the Sputnik_ wiki engine very easily.

Use LuaRocks_ to install Sputnik and ``versium-sqlite3``. A database-backed storage is required as the default filesystem storage does not support being accessed by multiple interpreters concurrently.

Create a wsapi compliant file:

.. code-block:: lua

    require('sputnik')
    return sputnik.wsapi_app.new{
      VERSIUM_STORAGE_MODULE = "versium.sqlite3", 
      VERSIUM_PARAMS = {'/tmp/sputnik.db'},
      SHOW_STACK_TRACE = true,
      TOKEN_SALT = 'xxx',
      BASE_URL       = '/',
    }

And run your threaded uWSGI server

..code-block:: sh

  ./uwsgi --plugins lua --lua sputnik.ws --threads 20 -s :3031

.. _Sputnik: http://sputnik.freewisdom.org/
.. _LuaRocks: http://www.luarocks.org/

A note on memory
----------------

As we all know, uWSGI is... fascist about memory. Memory is a precious resource. Do not trust software that does not care for your memory!
The Lua garbage collector is automatically called after each request. An option to set the frequency at which the GC runs will be available soon.