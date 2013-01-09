uWSGI Perl support (PSGI)
=========================

:term:`PSGI` is the equivalent of :term:`WSGI` in the Perl world.

* http://plackperl.org/
* http://github.com/miyagawa/psgi-specs/blob/master/PSGI.pod

The PSGI plugin is officially supported and has an officially assigned uwsgi modifier, ``5``. So as usual, when you're in the business of dispatching requests to Perl apps, set the ``modifier1`` value to 1 in your web server configuration.

Compiling the PSGI plugin
-------------------------

You can build a PSGI-only uWSGI server using the supplied :file:`buildconf/psgi.ini` file.

.. code-block:: sh

    python uwsgiconfig --build psgi
    # or compile it as a plugin...
    python uwsgiconfig --plugin plugins/psgi
    # and if you have not used the default configuration
    # to build the uWSGI core, you have to pass
    # the configuration name you used while doing that:
    python uwsgiconfig --plugin plugins/psgi core

Usage
-----

There is only one option exported by the plugin: ``psgi <app>``

You can simply load applications using

.. code-block:: sh

    ./uwsgi -s :3031 -M -p 4 --psgi myapp.psgi -m
    # or when compiled as a plugin,
    ./uwsgi --plugins psgi -s :3031 -M -p 4 --psgi myapp.psgi -m


Tested PSGI frameworks/applications
-----------------------------------

The following frameworks/apps have been tested with uWSGI:

* MojoMojo_
* Mojolicious_
* Mojolicious+perlbrew+uWSGI+nginx_ install bundle

.. _MojoMojo: http://mojomojo.org/
.. _Mojolicious: http://mojolicio.us/
.. _Mojolicious+perlbrew+uWSGI+nginx: https://github.com/kraih/mojo/wiki/nginx-&-uwsgi(psgi)-&-perlbrew-&-mojolicious

Multi-app support
-----------------

You can load multiple almost-isolated apps in the same uWSGI process using the ``mount`` option or using the ``UWSGI_SCRIPT``/``UWSGI_FILE`` request variables.

.. code-block:: ini

    [uwsgi]
    
    mount = app1=foo1.pl
    mount = app2=foo2.psgi
    mount = app3=foo3.pl

.. code-block:: nginx

    server {
      server_name example1.com;
      location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:3031;
        uwsgi_param UWSGI_APPID app1;
        uwsgi_param UWSGI_SCRIPT foo1.pl;
        uwsgi_modifier1 5;
      }
    }
    
    server {
      server_name example2.com;
      location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:3031;
        uwsgi_param UWSGI_APPID app2;
        uwsgi_param UWSGI_SCRIPT foo2.psgi;
        uwsgi_modifier1 5;
      }
    }
    
    server {
      server_name example3.com;
      location / {
        include uwsgi_params;
        uwsgi_pass 127.0.0.1:3031;
        uwsgi_param UWSGI_APPID app3;
        uwsgi_param UWSGI_SCRIPT foo3.pl;
        uwsgi_modifier1 5;
      }
    }


Notes
-----

* Async support should work out-of-the-box.
* Threads are supported on ithreads-enabled perl builds. For each app, a new interpreter will be created for each thread. This shouldn't be too different from a simple multi-process fork()-based subsystem. 
* There are currently no known memory leaks.


Real world example, `HTML::Mason`
---------------------------------

1. Install the HTML::Mason PSGI handler from CPAN and create a directory for your site.
   
   .. code-block:: sh
      
      cpan install HTML::Mason::PSGIHandler
      mkdir mason

2. Create ``mason/index.html``:

   .. code-block:: html
   
       % my $noun = 'World';
       % my $ua = $r->headers_in;
       % foreach my $hh (keys %{$ua}) {
        <% $hh %><br/>
       % }
       Hello <% $noun %>!<br/>
       How are ya?<br/>
       Request <% $r->method %> <% $r->uri %><br/>

3. Create the PSGI file (``mason.psgi``):

   .. code-block:: perl
   
       use HTML::Mason::PSGIHandler;
       
       my $h = HTML::Mason::PSGIHandler->new(
    	      comp_root => "/Users/serena/uwsgi/mason", # required
       );
       
       my $handler = sub {
    	      my $env = shift;
    	      $h->handle_psgi($env);
       };
    
   Pay attention to ``comp_root``, it must be an absolute path!

4. Now run uWSGI:

   .. code-block:: sh

    ./uwsgi -s :3031 -M -p 8 --psgi mason.psgi -m

5. Then go to ``/index.html`` with your browser.
