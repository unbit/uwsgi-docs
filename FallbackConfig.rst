Fallback configuration
======================

If you need a "reset to factory defaults", or "show a welcome page if the user has made mess with its config" scenario, fallback configuration
is your silver bullet

Simple case
***********

A very common problem is screwing-up the port on which the instance is listening.

To emulate this kind of error we try to bind on port 80 as unprivileged user:

.. code-block:: sh

   uwsgi --uid 1000 --http-socket :80
   
uWSGI will exit with:

.. code-block:: sh

   bind(): Permission denied [core/socket.c line 755]
   
Internally (from the kernel point of view) the instance exited with status 1

Now we want to allow the instance to automatically bind on port 8080 when the user supplied config fails.

Let's define a fallback config (you can save it as safe.ini):

.. code-block:: ini

   [uwsgi]
   print = Hello i am the fallback config !!!
   http-socket = :8080
   wsgi-file = welcomeapp.wsgi
   
Now we can re-run the (broken) instance:

.. code-block:: sh

   uwsgi --fallback-config safe.ini --uid 1000 --http-socket :80


Your error will be now something like:

.. code-block:: sh

   bind(): Permission denied [core/socket.c line 755]
   Thu Jul 25 21:55:39 2013 - !!! /home/roberto/uwsgi/uwsgi (pid: 7409) exited with status 1 !!!
   Thu Jul 25 21:55:39 2013 - !!! Fallback config to safe.ini !!!
   [uWSGI] getting INI configuration from safe.ini
   *** Starting uWSGI 1.9.15-dev-a0cb71c (64bit) on [Thu Jul 25 21:55:39 2013] ***
   ...
   
as you can see the instance has detected the exit code 1, and binary patched itself with a new one (without changing the pid, or calling fork())


Broken apps
***********

Another common problem is the inhability to load an application, but instead bringing down the whole site we want to load
an alternate application:

.. code-block:: sh

   uwsgi --fallback-config safe.ini --need-app --http-socket :8080 --wsgi-file brokenapp.py
   
Here the key is --need-app. It will call exit(1) if the instance has not been able to load at least an application.
