The SPDY router (uWSGI 1.9)
===========================

Starting from uWSGI 1.9 the HTTPS router has been extended to support version 3 of the SPDY protocol.

To run the HTTPS router with SPDY support use the ``--https2`` option:

.. code-block:: sh

   uwsgi --https2 addr=0.0.0.0:8443,cert=foobart.crt,key=foobar.key,spdy=1 --module werkzeug.testapp:test_app

This will start an HTTPS router on port 8443 with SPDY support, forwarding requests to the werkzeug test app the instance is running.

If you go to https://address:8443/ with a SPDY-enabled browser you will see additional WSGI vars reported by werkzeug:

* ``SPDY`` set to 'on'
* ``SPDY.version`` reports protocol version (generally '3')
* ``SPDY.stream`` reports the stream identifier (an odd number)

Notes
*****

* You need at least OpenSSL version 1.x to use SPDY (all of the modern Linux distros should have it).
* During uploads the window size is constantly updated.
* The ``--http-timeout`` directive is used to set the SPDY timeout. This is the maximum amount of inactivity time after the SPDY connection is closed.
* ``PING`` requests from the browsers are ALL acknowledged.
* On connect, the SPDY router sends a settings packet to the client with optimal values.
* If a stream fails in some catastrophic way, the whole connection is closed hard.
* RST messages are always honoured

TODO
****

* Add old SPDY v2 support (is it worth it?)
* Allow PUSHing of resources from the uWSGI cache
* Allow tuning internal buffers
