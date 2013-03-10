Installing uWSGI
================

Installing from a distribution package
--------------------------------------

.. seealso:: See the :doc:`Download` page for a list of known distributions shipping uWSGI.

Installing from source
----------------------

To build uWSGI you need python and a c compiler (gcc and clang are supported).

Based on the languages you want to support you will need their development headers.

On a Debian/Ubuntu system you can install them (and the rest of the infrastructure required to build software) with:

.. code-block:: sh

   apt-get install build-essential python

And if you want to build a binary with python/wsgi support

.. code-block:: sh

   apt-get install python-dev

If you have a variant of `make` available in your system you can simply run `make`.

If you do not have `make` (or want to have more control) simply run:

.. code-block:: sh

   python uwsgiconfig.py --build

You can also use pip to install uWSGI (it will build a binary with python support). 

.. code-block:: sh

   # Install the latest stable release:
   pip install uwsgi
   # ... or if you want to install the latest LTS (long term support) release,
   pip install http://projects.unbit.it/downloads/uwsgi-lts.tar.gz

Or you can use ruby gems

.. code-block:: sh

   # Install the latest stable release:
   gem install uwsgi


At teh end of the build, you will get a report of the enabled features. If something you require is missing, just add the development headers
and rerun the build.

FOr example to build uWSGI with ssl and perl regexp support you need libssl-dev and pcre headers

Alternative build profiles
--------------------------

For historical reasons when you run 'make', uWSGI is built with Python as the only supported language.

You can build customized uWSGI servers using build profiles, located in the `buildconf/` directory.

You can use a specific profile with 

.. code-block:: sh

   python uwsgiconfig --build <profile>

Or you can pass it via an environment variable:

.. code-block:: sh

   UWSGI_PROFILE=lua make
   # ... or even ...
   UWSGI_PROFILE=gevent pip install uwsgi
   
