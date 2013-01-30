Serving static files with uWSGI (updated to 1.5)
================================================

Sadly you cannot live without serving static files via some protocol (HTTP, SPDY...).

uWSGI as a big series of options and micro-optimizations for serving static files.

Generally your webserver of choice (nginx, mongrel2...) will serve static files efficiently and fast
and will simply forward dynamic requests to uwsgi backend nodes.

The uWSGI project has ISPs and PaaS (read: the hostign market) as the main target, where generally you would want to avoid
generating disk I/O on a central server, while you want each user dedicated-area to be accounted for that (and more important
you want to allow your customer to customize the way they serve static assets without bothering your system administrator)


Mode 1: check for a static resource before passing the request to your app
**************************************************************************

This a common way of managing static files in web apps. Fraemwork like RubyOnRails use it from ages.

Suppose your static assets are under /customers/foobar/app001/public

You want to check each request has a corresponence in that directory before passign the request to your app.

The --check-static option is for you:

.. code-block:: sh

   --check-static /customers/foobar/app001/public

If uWSGI receives a request for /foo.png will first check for /customers/foobar/app001/public/foo.png and if it is not found
it will invoke your app.

You can specify --check-static multiple times

.. code-block:: sh

   --check-static /customers/foobar/app001/public --check-static /customers/foobar/app001/static

uWSGI will first check for /customers/foobar/app001/public/foo.png if it does not find it it will try /customers/foobar/app001/static/foo.png
and if it is still not available the request will goes on to your app.

