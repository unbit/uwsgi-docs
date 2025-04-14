The CFFI Plugin
===============

Introduction
^^^^^^^^^^^^

A new Python plugin supports PyPy3 (not Python 2). It is based on the older
PyPy plugin and the cffi library's embedding feature. It should work on Linux
or on OSX.

Even more of this plugin is implemented in Python than in the previous PyPy
plugin. It is possible to redefine the plugin at runtime in Python or
to write a uWSGI event loop.

It doesn't work on PyPy3 7.3.1 due to a bug, but it should work on other
recent versions of PyPy or a nightly build.

Since the cffi embedding interface is independent of the Python implementation,
this plugin can also be compiled for CPython 3, but with reduced performance
compared to the classic Python plugin or the PyPy3 cffi plugin.

This plugin uses ``rpath`` so that the plugin finds the Python library it was
complied for without having to set an option or environment variable.

Installation
^^^^^^^^^^^^

.. code-block:: sh

    pypy3 uwsgiconfig.py --plugin plugins/cffi

Options
^^^^^^^

* ``cffi-home`` - set PYTHONHOME/virtualenv
* ``cffi-wsgi`` - load a WSGI module (or use ``--mount`` instead)
* ``cffi-init`` - load a module during init (to customize the plugin)
* ``cffi-eval`` - evaluate Python code before fork()
* ``cffi-eval-post-fork`` - evaluate Python code soon after fork()
* ``cffi-exec`` - execute Python code from file before fork()
* ``cffi-exec-post-fork`` - execute Python code from file soon after fork()

The plugin reads the PYTHONPATH enviroment variable.

Using ``--mount``
^^^^^^^^^^^^^^^^^

``--mount`` is a plugin-independent option to load applications. The syntax is
``--mount <mountpoint>=<app>``

``<mountpoint>`` is usually ``/`` or e.g. ``/app1`` or ``/app2``. If there is only one application, it can be anything; the first app loaded is the default. If there are multiple, uwsgi will look them up based on the path if you pass ``--manage-script-name``.

``<app>`` is either the path to a file ending in ``.py`` or ``.wsgi`` defining a global ``application`` callable, or the name of an importable module ``mod`` or ``pkg.mod``, or a colon-separated ``pkg.mod:app`` to use a callable besides the default ``application``.

REPL trick
^^^^^^^^^^

It's useful to have a shell. You could use a builtin repl:

.. code-block:: sh

   uwsgi --socket :3031 --plugin cffi --cffi-eval "import code; code.interact()" --honour-stdin

Or IPython installed in a virtualenv:

.. code-block:: sh

    /uwsgi --socket :3031 --plugin cffi --cffi-home $VIRTUAL_ENV --cffi-eval "import IPython; IPython.embed()" --honour-stdin

The uWSGI C API
^^^^^^^^^^^^^^^

The cffi plugin automatically wraps most of ``uwsgi.h``. It is reachable through ``_uwsgi.ffi`` and ``_uwsgi.lib``. Functions missing from this plugin's version of the ``uwsgi`` module could be accessed this way.

.. code-block:: python

    >>> import _uwsgi
    >>> _uwsgi.lib.uwsgi_endswith(b'foobar', b'bar')
    1

Learn how to use ``cffi`` at https://cffi.readthedocs.io/

Notes
^^^^^

* The cffi plugin shouldn't be used with the python plugin, but it doesn't check. Don't do it! 
*  The plugin does not support application dictionaries or ``uwsgi.applications``.
* The plugin always runs in the equivalent of ``--single-interpreter`` mode.
* The plugin does not work with the default ``--async`` event loop.
