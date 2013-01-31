The SPDY router (uWSGI 1.5)
===========================

Starting from uWSGI 1.5 the HTTPS router has been extended to support the SPDY protocol.

Currently version 3 of the protocol is supported.

To run the HTTPS router with SPDY support use the --https2 syntax:

.. code-block:: sh

   uwsgi --https2 addr=0.0.0.0:8443,cert=foobart.crt,key=foobar.key,spdy=1 --module werkzeug.testapp:test_app

This will start an https router on port 8443 with SPDY support forwarding requests to the werkzeug test app.

If you go to https://address:8443/ with a SPDY-enabled browser you will see additional WSGI vars reported by werkzeug:

``SPDY`` set to 'on'

``SPDY.version`` reports protocol version (generally '3')

``SPDY.stream`` reports the stream id (an odd number)

Notes
*****

During uploads the window size is constantly updated

the ``--http-timeout`` directive is used to set the SPDY timeout, this is the maximum amount of inactivity time
after the SPDY connection is closed

PING requests from the browsers are ALL acknowledged

On connect the SPDY router send a settings packet to the client with optimal values

If a stream fails badly the whole connection is closed

RST messages are always honoured

TODO
****

Add old SPDY v2 support (is it whorty ?)

Allows PUSHing of resources from the uWSGI cache

Allows tuning internal buffers
