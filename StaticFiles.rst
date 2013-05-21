Serving static files with uWSGI (updated to 1.9)
================================================

Sadly you cannot live without serving static files via some protocol (HTTP, SPDY...).

uWSGI has a big series of options and micro-optimizations for serving static files.

Generally your webserver of choice (nginx, mongrel2...) will serve static files efficiently and fast
and will simply forward dynamic requests to uwsgi backend nodes.

The uWSGI project has ISPs and PaaS (read: the hosting market) as the main target, where generally you would want to avoid
generating disk I/O on a central server, while you want each user dedicated-area to be accounted for that (and more important
you want to allow your customers to customize the way they serve static assets without bothering your system administrator)


Mode 1: check for a static resource before passing the request to your app
**************************************************************************

This a common way of managing static files in web apps. Frameworks like RubyOnRails have used this method for ages.

Suppose your static assets are under /customers/foobar/app001/public

You want to check each request has a corresponding file in that directory before passing the request to your app.

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

When mappings are not enough, advanced internal routing (available from 1.9) will be your last resort.

Thanks to the power of regexps you will be able to build really complex mappings:

.. code-block:: ini

   [uwsgi]
   route = /static/(.*)\.png static:/var/www/images/pngs/$1/highres.png
   route = *\.jpg static:/var/www/always_the_same_photo.jpg

Setting the index page
**********************

By default, requests for a "directory" (like / or /foo) are bypassed (if not advanced internal routing is in place).
If you want to map specific files to a "directory" request (like the venerable index.html) just use the ``--static-index``
option

.. code-block:: sh

   --static-index index.html --static-index index.htm --static-index home.html

as the other options, the first one matching will stop the chain

Mime types
**********

Your HTTP/SPDY/whateveryouwant responses for static files should always return the correct mime type for the specifc file.

By default uWSGI build its list of mime types from the /etc/mime.types file, but you can load additional files with the ``--mime-file``
option

.. code-block :: sh

   --mime-file /etc/alternatives.types --mime-file /etc/apache2/mime.types

all of the files will be combined in a single auto-optimizing linked list

Skipping specific extensions
****************************

Some platform/language, most-notably cgi-based ones, like php are deployed in a very simple manner.
You simply drop them in the document root and they are executed whenever you call them.

This approach, when combined with static file serving, requires a bit of attention for avoiding your cgi/php/whatever to be
served like static files.

The ``--static-skip-ext`` will do the trick.

A very common pattern on cgi and php deployment is that one:

.. code-block:: sh

   --static-skip-ext .php --static-skip-ext .cgi --static-skip-ext .php4


Setting the Expires headers
***************************

When serving static files, abusing client browser caching is the path to wisdom. By default uWSGI will add a Last-Modified
header to all of the static-responses, and will honour the If-Modified-Since request header.

This could be not enough for high traffic sites. You can add an automatic Expires headers using one of the following options

``--static-expires-type``

will set the Expires header to the specified number of seconds for the specified mime type:

.. code-block:: sh

   --static-expires-type text/html=3600

will add an Expires header with a value of an hour since now

``--static-expires-type-mtime``

same as the previous one, but will add the specified number of seconds to the file modification time and not the current time

``--static-expires``

this will set Expires header for all of the filenames (after the complete mapping to the filesystem) matching the specified regexp

.. code-block:: sh

   --static-expires /var/www/static/foo*\.jpg 3600

``--static-expires-mtime``

same as the previous one, but will add the specified number of seconds to the file modification time and not the current time

``--static-expires-uri`` and ``--static-expires-uri-mtime``

like ``--static-expires`` but the regexp is matched over the REQUEST_URI value

``--static-expires-path-info`` and ``--static-expires-path-info-mtime``

like ``--static-expires`` but the regexp is matched over the PATH_INFO value

Transferring modes
******************

If you have developed an async/nonblocking application, serving static files directly from uWSGI is not a big problem.
All of the transfers are managed in the async way, so your app will not block during them.

In multiprocess/multithread modes, your process (or threads) will be blocked during the whole transfer of the file.

For little files this is not a problem, but for the biggest one you'd better to offload their transfer.

You have various ways:

X-Sendfile
^^^^^^^^^^

If your webserver support the X-Sendfile header and has access to the file you want to send (for example it is on the same machine
of your application or can access it via nfs) you can avoid the transfer of the file from your app with that option:

.. code-block:: sh

   --file-serve-mode x-sendfile

in that way, uWSGI will only generates response headers and the webserver will be delegated to transferring it

X-Accel-Redirect
^^^^^^^^^^^^^^^^

This is currently (january 2013) supported only on nginx. Works in the same way as x-sendfile, the only difference
is in the option argument:

.. code-block:: sh

   --file-serve-mode x-accel-redirect

Offloading
^^^^^^^^^^

This is the best approach if your frontend server has no access to the static files.
It uses the :doc:`OffloadSubsystem` to delegate the file transfer to a pool of non-blocking threads.

Each one of this thread can manage thousands of file transfer concurrently.

To enable file transfer offloading just use the option

``--offload-threads``

specifying the number of threads to spawn (try to set it to the number of cpu cores to take advantage of SMP)

.. code-block:: sh

   --offload-threads 8

will spawn 8 threads for each process and they will be automatically used for transferring files


GZIP (uWSGI 1.9)
****************

uWSGI 1.9 can check for a .gz variant of a static file.

Lot of users/sysadmins underestimate the impact on servers of on-the-fly gzip encoding.

Compressing files every time (unless your webservers is caching them in some way) will use CPU
and will not be able to use advanced techniques like sendfile(). For a very loaded site (or network) this could
be a problem (expecially when gzip encoding is a need for better user experience).

Albeit uWSGI is able to compress contents on the fly (this is used in the http/https/spdy router for example), the best approach
for serving gzipped static files is generating them "manually" (obviously you can use a script for that), and let uWSGI
choose if it is best to serve the uncompressed or the compressed one every time.

In this way serving a gzip content will be no different from serving standard static files (sendfile, offloading...)

To trigger that behaviour you have various options:

``static-gzip <regexp>`` check for .gz variant for all of the requested files mathing the specified regexp (the regexp is applied to the full filesystem path of the file)

``static-gzip-dir <dir>`` check for .gz variant for all of the files under the specified dir

``static-gzip-prefix <prefix>`` check for .gz variant for all of the files having the specified filesystem prefix (alias for the previous option)

``static-gzip-ext <ext>`` check for .gz variant for all of the files with the specified extension

``static-gzip-suffix <suffix>`` check for .gz variant for all of the files ending with the specified suffix (alias for the previous option)

``static-gzip-all`` check for .gz variant for all of the requested static files

Example:

in your /var/www directory you have uwsgi.c and uwsgi.c.gz files.

If a client make a request for uwsgi.c and accept gzip content encoding, uwsgi.c.gz will be served instead

Security
********

Every static mapping is fully translated to the "real" path (so symbolic links are translated too).

If the resulting path is not under the one specified in the option, a security error will be triggered.

If you trust your unix skills and know what you are doing, you can add a list of "safe" paths. If a translated path
is not under a configured directory but it is under a safe one, it will be served.

Example:

.. code-block:: sh

   --static-map /foo=/var/www/

/var/www/test.png is a symlink to /tmp/foo.png

After the translation of /foo/test.png, uWSGI will raise a security error as /tmp/foo.png is not under /var/www/.

Using

.. code-block:: sh

   --static-map /foo=/var/www/ --static-safe /tmp

will bypass that limit.

You can specify multiple ``--static-safe`` options

Caching paths mappings/resolutions
**********************************

One of the bottlenecks in static file serving is the constant massive amount of stat() syscalls.

You can use the uWSGI caching subsystem to store mappings from uri to filesystem paths.

.. code-block:: sh

   --static-cache-paths 30

will cache each static file translation for 30 seconds in the uWSGI cache

From uWSGI 1.9 an updated caching subsystem has been added, allowing you to create multiple caches.

If you want to store translation on a specific cache you can use

``--static-cache-paths-name <cachename>``

Bonus trick: storing static files in the cache
**********************************************

You can directly store a static file in the uWSGI cache during startup using that option (you can specify it multiple times)

``--load-file-in-cache <filename>``

the content of the file will be stored under the key <filename>.


Pay attention:

.. code-block:: sh

   --load-file-in-cache ./foo.png

will store the item as ./foo.png

Notes
*****

The static file serving subsystem automatically honours the If-Modified-Since HTTP request header
