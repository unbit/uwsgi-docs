Running python webapps on Heroku with uWSGI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Prerequisites: a Heroku account (on the ceddar platform), git (on the local system) and the heroku toolbelt.

Note: you need a uWSGI version >= 1.4.6 to correctly run python apps. Older versions may work, but are not supported.

Preparing the environment
*************************

On your local system prepare a directory for your project:

.. code-block:: sh

   mkdir uwsgi-heroku
   cd uwsgi-heroku
   git init .
   heroku create

the last command will create a new heroku application (you can check it on the web dashboard).

For our example we will run the Werkzeug WSGI testapp, so we need to install the werkzeug package in addition to uWSGI.

First step is creating a requirements.txt file and tracking it with git.

The content of the file will be simply

..code-block:: sh

   uwsgi
   werkzeug

Let's track it with git

.. code-block:: sh

   git add requirements.txt

Creating the uWSGI config file
******************************

Now we can create our uWSGI configuration file. Basically all of the features can be used on heroku

.. code-block:: ini

   [uwsgi]
   http-socket = :$(PORT)
   master = true
   processes = 4
   die-on-term = true
   module = werkzeug.testapp:test_app
   memory-report = true

as you can see this is a pretty standard configuration. The only heroku-required options are --http-socket and --die-on-term.

The first is required to bind the uWSGI socket to the port requested by the Heroku system (exported via the environment variable PORT we can access with $(PORT))

The second one (--die-on-term) is required to change the default behaviour of uWSGI when it receive a SIGTERM (brutal realod, while Heroku expect a shutdown)

The memory-report option (as we are in a memory contrained environment) is a good thing.

Remember to track the file

.. code-block:: sh

   git add uwsgi.ini

Preparing for the first commit/push
***********************************

We now need the last step: creating the Procfile.

The Procfile is a file describing which commands to start. Generally (with other deployment systems) you will use it for every
additional process required by your app (like memcached, redis, celery...), but under uWSGI you can continue using its advanced facilities to manage them.

So, the Procfile, only need to start your uWSGI instance:

.. code-block:: sh

   web: uwsgi uwsgi.ini

Track it

.. code-block:: sh

   git add Procfile

And finally let's commit all:

.. code-block:: sh

   git commit -a -m "first commit"

and push it (read: deploy) to Heroku:

.. code-block:: sh

    git push heroku master

The first time it will requires a couple of minutes as it need to prepare your virtualenv and compile uWSGI.

Following push will be much faster.

