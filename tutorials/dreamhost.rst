Running uWSGI on Dreamhost shared hosting
*****************************************

Note: the following tutorial gives suggestions on how to name files with the objective of hosting multiple applications
on your account. You are obviously free to change naming schemes.

The tutorial assumes a shared hosting account, but it works on the VPS offer too (even if on such a system you have lot more freedom and you could use
better techniques to accomplish the result)


Preparing the environment
*************************

Log in via ssh to your account and move to the home (well, you should be already there after login).

Download a uWSGI tarball (anything >= 1.4 is good, but for maximum performance use >= 1.9), explode it and build it
normally (run make).

At the end of the procedure copy the resulting ``uwsgi`` binary to your home (just to avoid writing longer paths later).

Now move to the document root of your domain (it should be named like the domain) and put a file named ``uwsgi.fcgi`` in it with that content:

.. code-block:: sh

   #!/bin/sh
   /home/XXX/uwsgi /home/XXX/YYY.ini

change XXX with your account name and YYY with your domain name (it is only a convention, if you know what you are doing feel free to change it)

Give the file 'execute' permission

.. code-block:: sh

   chmod +x uwsgi.fcgi

Now in your home create a YYY.ini (remember to change YYY with your domain name) with that content

.. code-block:: ini

   [uwsgi]
   flock = /home/XXX/YYY.ini
   account = XXX
   domain = YYY

   protocol = fastcgi
   master = true
   processes = 3
   logto = /home/%(account)/%(domain).uwsgi.log
   virtualenv = /home/%(account)/venv
   module = werkzeug.testapp:test_app
   touch-reload = %p
   auto-procname = true
   procname-prefix-spaced = [%(domain)]

change the first three lines accordingly.

Preparing the python virtualenv
*******************************

As we want to run the werkzeug test app, we need to install its package in a virtualenv.

Move to the home:

.. code-block:: sh

   virtualenv venv
   venv/bin/easy_install werkzeug

The .htaccess
*************

Move again to the document root to create the .htaccess file that will instruct Apache to forward request to uWSGI

.. code-block:: sh

   RewriteEngine On
   RewriteBase /
   RewriteRule ^uwsgi.fcgi/ - [L]
   RewriteRule ^(.*)$ uwsgi.fcgi/$1 [L]

Ready
*****

Go to your domain and you should see the Werkzeug test page. If it does not show you can check uWSGI logs in the file you specified with the
logto option.

The flock trick
***************

As the apache mod_fcgi/mod_fastcgi/mod_fcgid implemenetations are very flaky on process management, you can easily end with lot of copies
of the same process running. The flock trick avoid that. Just remember that the flock option is very special as you cannot use
placeholder or other advanced techniques with it. You can only specify the absolute path of the file to lock.

Statistics
**********

As always remember to use uWSGI internal stats system

first, install uwsgitop

.. code-block:: sh

   venv/bin/easy_install uwsgitop

Enable the stats server on the uWSGI config

.. code-block:: ini

.. code-block:: ini

   [uwsgi]
   flock = /home/XXX/YYY.ini
   account = XXX
   domain = YYY

   protocol = fastcgi
   master = true
   processes = 3
   logto = /home/%(account)/%(domain).uwsgi.log
   virtualenv = /home/%(account)/venv
   module = werkzeug.testapp:test_app
   touch-reload = %p
   auto-procname = true
   procname-prefix-spaced = [%(domain)]

   stats = /home/%(account)/stats_%(domain).sock

(as we have touch-reload in place, as soon as you update the ini file your instance is reloaded, and you will be able to suddenly use uwsgitop)


.. code-block:: sh

    venv/bin/uwsgitop /home/WWW/stats_YYY.sock

(remember to change XXX and YYY accordingly)


Running Perl/PSGI apps (requires uWSGI >= 1.9)
**********************************************

Older uWSGI versions does not work well with plugins other than the python one, as the fastcgi implementation has lot of limits.

Starting from 1.9, fastCGI is a first-class citizen in the uWSGI project, so all of the plugins work with it.

As before, compile the uWSGI sources but this time we will build a PSGI monolithic binary:

.. code-block:: sh

   UWSGI_PROFILE=psgi make

copy the resulting binary in the home as uwsgi_perl

Now edit the previously created uwsgi.fcgi file changing it to

.. code-block:: sh

   #!/bin/sh
   /home/XXX/uwsgi_perl /home/XXX/YYY.ini

(again, change XXX and YYY accordingly)

Now upload an app.psgi file in the document root (this is your app)

.. code-block:: pl

   my $app = sub {
      my $env = shift;
      return [
          '200',
          [ 'Content-Type' => 'text/plain' ],
          [ "Hello World" ]
      ];
   };


