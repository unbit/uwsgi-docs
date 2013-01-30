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

The ``--check-static`` option is for you:

.. code-block:: sh

   --check-static /customers/foobar/app001/public

If uWSGI receives a request for /foo.png will first check for /customers/foobar/app001/public/foo.png and if it is not found
it will invoke your app.

You can specify ``--check-static`` multiple times

.. code-block:: sh

   --check-static /customers/foobar/app001/public --check-static /customers/foobar/app001/static

uWSGI will first check for /customers/foobar/app001/public/foo.png if it does not find it it will try /customers/foobar/app001/static/foo.png
and if it is still not available the request will goes on to your app.

Mode 2: trust frontend supplied DOCUMENT_ROOT
*********************************************

If your frontend (a webserver, a uWSGI corerouters...) set the DOCUMENT_ROOT values, you can instruct uWSGI to trust it
as a valid directory for checking for static files.

Just use the ``--check-static-docroot`` option

Mode 3: using mountpoints
*************************

A more general approach is "mapping" specific request prefixes to physical directory on your file system.

``static-map mountpoint=path`` will do the trick

.. code-block:: sh

   --static-map /images=/var/www/img

if you get a request for /images/logo.png and /var/www/img/logo.png exists, it will be served, otherwise your app will manage the request.

You can specify multiple ``--static-map`` options even for the same mountpoint

.. code-block:: sh

   --static-map /images=/var/www/img --static-map /images=/var/www/img2 --static-map /images=/var/www/img3

the file will be searched in each directory til is found (otherwise, as always, the request will be managed by your app)

In some specific cases you may want to build the internal path in a different way. The ``--static-map2`` option will change the translation in that way:

.. code-block:: sh

   --static-map2 /images=/var/www/img

a request for /images/logo.png will be mapped to /var/www/img/images/logo.png

That means the full request will be appended to the path

You can map (or map2) both directory and files:

.. code-block:: sh

   --static-map /images/logo.gif=/tmp/oldlogo.gif


Mode 4: using advanced internal routing
***************************************

When mappings are not enough, advanced internal routing (available from 1.5) will be your last resort.

Thanks to the power of regexps you will be able to build really complex mappings:

.. code-block:: ini

   [uwsgi]
   route = /static/(.*)\.png static:/var/www/images/pngs/$1/highres.png
   route = *\.jpg static:/var/www/always_the_same_photo.jpg

Setting the index page
**********************

Mime types
**********

Skipping specific extensions
****************************

Setting the Expires headers
***************************

Transferring modes
******************

X-Sendfile
X-Accel-Redirect
Offloading

Security
********

--static-safe

Caching paths mappings/resolutions
**********************************

--static-cache-paths

--static-cache-paths-name will use the specified new generation cache

Bonus trick: storing static files in the cache
**********************************************

--load-file-in-cache

Notes
*****
