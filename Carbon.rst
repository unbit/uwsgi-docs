Integration with Graphite/Carbon
================================

Graphite (http://graphite.wikidot.com/) is a kick-ass realtime graphing application built on top of three components: Whisper (a data storage system), Carbon (a server gathering data and storing them in whisper files) and a Python web application for rendering and managing graphs.

The uWSGI Carbon plugin allows you to send uWSGI's internal statistics to one or more Carbon servers.

It is compiled in by default starting from uWSGI 1.0 but it can also be built as a plugin.

Quickstart
----------

For the sake of illustration, let's say your Carbon server is listening on ``127.0.0.1:2003`` and your uWSGI instance is on the machine ``debian32``, listening on ``127.0.0.1:3031`` with 4 processes.

Now by adding the ``--carbon`` option to your uWSGI instance, your server will periodically (by default every 60 seconds) send its statistics to the carbon server.

.. code-block:: sh

    uwsgi --socket 127.0.0.1:3031 --carbon 127.0.0.1:2003 --processes 4 

The metrics are named in this way:

.. code-block::

    uwsgi.<hostname>.<id>.requests
    uwsgi.<hostname>.<id>.worker<n>.requests

* ``hostname`` will be mapped to the machine hostname
* ``id`` is the name of the first uWSGI socket with dots replaced by underscores
* ``n`` is the number of the worker process, 1-based.

.. code-block:: xxx

    uwsgi.debian32.127_0_0_1:3031.requests
    uwsgi.debian32.127_0_0_1:3031.worker1.requests
    uwsgi.debian32.127_0_0_1:3031.worker2.requests
    uwsgi.debian32.127_0_0_1:3031.worker3.requests
    uwsgi.debian32.127_0_0_1:3031.worker4.requests
