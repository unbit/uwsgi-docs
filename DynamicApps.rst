Adding applications dynamically
===============================

You can start the uWSGI server without configuring an application.

To load a new application you can use these variables in the uwsgi packet:

* ``UWSGI_SCRIPT`` -- pass the name of a WSGI script defining an ``application`` callable
* or ``UWSGI_MODULE`` and ``UWSGI_CALLABLE`` -- the module name (importable path) and the name of the callable to invoke from that module

Dynamic apps are officially supported on Cherokee, Nginx, Apache, cgi_dynamic. They are easily addable to the Tomcat and Twisted handlers.

Defining VirtualEnv with dynamic apps
-------------------------------------

Virtualenvs are based on the ``Py_SetPythonHome()`` function. This function has effect only if called before ``Py_Initialize()`` so it can't be used with dynamic apps.

To allow defining VirtualEnv with DynamicApps a hack is the only solution.

First of all you have to tell python engine to not import the ``site`` module. This is the module (by default automagically loaded at Python initialization) that will add all ``site-packages`` to ``sys.path``.

To emulate virtualenvs, we'll have to load the site module only after subinterpreter initialization.

Skipping the first ``import site``, we can now simply set ``sys.prefix`` and ``sys.exec_prefix`` on dynamic app loading and call

.. code-block:: c

   PyImport_ImportModule("site");
   // Some users would want to not disable initial site module loading, so the site module must be reloaded:
   PyImport_ReloadModule(site_module);

Now we can simply set the VirtualEnv dynamically using the ``UWSGI_PYHOME`` var::

.. code-block:: nginx

  location / {
    uwsgi_pass 192.168.173.5:3031;
    include uwsgi_params;
    uwsgi_param UWSGI_SCRIPT mytrac;
    uwsgi_param UWSGI_PYHOME /Users/roberto/uwsgi/VENV2;
  }