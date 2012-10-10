The uWSGI project
=================

uWSGI is an extremely advanced, sysadmin-friendly, highly-modular application container server coded in C.

It can communicate with your front-end webserver via HTTP, FastCGI, ZeroMQ and its highly specified/optimized protocol
named 'uwsgi' (all-lowercase) already supported out-of-the-box by a lot of webservers.

Born as a simple WSGI-only server, over time it has evolved in a complete stack for networked/:doc:`clustered<Clustering>` web applications, implementing :doc:`message/object passing<CustomRouting>`, :doc:`caching<Caching>`, :doc:`RPC` and :doc:`process management<ProcessManagement>`.

uWSGI can be run in preforking, threaded, :doc:`asynchronous/evented<Async>` and :doc:`green thread/coroutine<GreenThread>` modes. Various forms of green threads/coroutines are supported, including :doc:`uGreen`, Greenlet, Stackless, :doc:`Gevent` and :doc:`FiberLoop`.

Sysadmins will love it as it can be :doc:`configured via several methods<Configuration>`, including command line, environment variables, XML, INI, YAML, JSON, SQLite and LDAP.

Thanks to its pluggable architecture it can be extended without limits to support more platforms and languages.

To get started with uWSGI, take a look at the :doc:`Install` page. Then continue to :doc:`Quickstart` or if you are feeling daring, the :doc:`Options` page. Some example configurations are available on the :doc:`Examples` page.

.. note::

  With a large open source project such as uWSGI the code and the documentation may not always be in sync.
  The mailing list is the best source for help regarding uWSGI.


Table of Contents
=================


.. toctree::
   :maxdepth: 1

   Download
   LanguagesAndPlatforms
   WebServers
   FAQ
   ThingsToKnow
   Configuration
   Options
   Vars
   Protocol
   AlarmSubsystem
   AttachingDaemons

Web Server support
==================
   
.. toctree::
   :maxdepth: 1
 
   Apache
   Cherokee
   HTTP
   Lighttpd
   Nginx

.. include:: FeatureOverview.rst

Contact
=======

============  =
Mailing list  http://lists.unbit.it/cgi-bin/mailman/listinfo/uwsgi
Gmane mirror  http://dir.gmane.org/gmane.comp.python.wsgi.uwsgi.general
IRC           #uwsgi @ irc.freenode.org. The owner of the channel is `unbit`.
Twitter       http://twitter.com/unbit
============  =

.

Donate
======

uWSGI development is sponsored by the Italian ISP `Unbit <http://unbit.it/>` and its customers. You can buy commercial
support and licensing. If you are not an Unbit customer, or you cannot/do not want to buy a commercial uWSGI license,
consider making a donation. Obviously please feel free to ask for new features in your donation.
We will give credit to everyone who wants to sponsor new features.

See the `old uWSGI site<http://projects.unbit.it/uwsgi/#Donateifyouwant>` for the donation link.
You can also `donate via GitTip<https://www.gittip.com/unbit/>`.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. toctree::
   :hidden:

   FeatureOverview
   HTTPS
   LDAP
   examples/README
   tutorials/README
   tips_and_tricks/README
   README
   