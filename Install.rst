Installing uWSGI
================

Installing from a distribution package
--------------------------------------

.. seealso:: See the :doc:`Download` page for a list of known distributions shipping uWSGI.

Installing from source
----------------------

By default uWSGI requires the Python and `libxml2` headers/development libraries.

On a Debian/Ubuntu system you can install them (and the rest of the infrastructure required to build software) with:

.. code-block:: sh

   apt-get install build-essential python-dev libxml2-dev

uWSGI's build system is Python-based. If you have a variant of `make` available in your system you can simply run `make`.

If you do not have `make` (or want to have more control) simply run:

.. code-block:: sh

   python uwsgiconfig.py --build

You can also use pip to install uWSGI. 

.. code-block:: sh

   # Install the latest stable release:
   pip install uwsgi
   # ... or if you want to install the latest LTS (long term support) release,
   pip install http://projects.unbit.it/downloads/uwsgi-lts.tar.gz

The build shouldn't take very long. After it completes, see the :doc:`Quickstart` page or dive in to the breadth of uWSGI's configuration options over at :doc:`Options`.

Alternative build profiles
--------------------------

For historical reasons, uWSGI is built with Python as the only supported language.

You can build customized uWSGI servers using build profiles, located in the find them in the `buildconf/` directory.

You can use a specific profile with 

.. code-block:: sh

   python uwsgiconfig --build <profile>

Or you can pass it via an environment variable:

.. code-block:: sh

   UWSGI_PROFILE=lua make
   # ... or even ...
   UWSGI_PROFILE=gevent pip install uwsgi
   