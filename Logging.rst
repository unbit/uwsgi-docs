Logging
=======

.. seealso:: :doc:`LogFormat`

Basic logging
-------------

The most basic form of logging in uWSGI is of course writing everything, both requests and errors/informational messages, to stdout/stderr. This happens automatically.

But like most everything in uWSGI, this is fully configurable. The most basic form of log redirection is the ``--logto``/``--logto2``/``--daemonize`` options which allow you to redirect logs to files (or ``/dev/null``, mind).

Basic logging to files
^^^^^^^^^^^^^^^^^^^^^^

To log to files instead of stdout/stderr, use ``--logto``, or to simultaneously daemonize uWSGI, ``--daemonize``.

.. code-block:: sh

    ./uwsgi -s :3031 -w simple_app --daemonize /tmp/mylog.log
    ./uwsgi -s :3031 -w simple_app --logto /tmp/mylog.log
    # logto2 only opens the log file after privileges have been dropped to the specified uid/gid.
    ./uwsgi -s :3031 -w simple_app --uid 1001 --gid 1002 --logto2 /tmp/mylog.log

Basic logging (connected UDP mode)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using UDP logging you can "centralize" cluster logging or redirect the write of logs (that can be very heavy for your I/O resources) to another machine. UDP logging works both in daemonized and interactive mode. UDP logging works with connected-socket mode, so the UDP server must be available before uWSGI starts. For a more raw approach (working in unconnected mode) see the above section on socket logging.

To enable it you simply pass the address of an UDP server to the ``--daemonize``/``--logto`` option:

.. code-block:: sh

    ./uwsgi -s :3031 -w simple_app --daemonize 192.168.0.100:1717
    ./uwsgi -s :3031 -w simple_app --logto 192.168.0.100:1717

This will redirect all the stdout/stderr data to the UDP socket on 192.168.0.100, port 1717.

Now you need an UDP server that will manage your UDP messages. You could use netcat, or even uWSGI:

.. code-block:: sh

    nc -u -p 1717 -s 192.168.0.100 -l
    ./uwsgi --udp 192.168.0.100:1717

The second way is a bit more useful as it will print the source (ip:port) of every message. In case of multiple uWSGI server logging on the same UDP server it will allow you to recognize one server from another. And of course you can write your own apps to manage/filter/save the logs received via udp.


Pluggable loggers
-----------------

uWSGI also supports pluggable loggers, which allow you to more flexibly specify where to log, and what to log (at request/error granularity at the time of writing).

Depending on the configuration of your uWSGI build, some loggers may or may not be available. Some may require to be loaded as plugins. To find out what plugins are available in your build, invoke uWSGI with ``--logger-list``.

To set up a pluggable logger, use the ``--logger`` or ``--req-logger`` options. ``--logger`` will set up a logger for every message while ``--req-logger`` will set up a logger for request information messages.

The syntax for the logger options is as follows:

.. code-block:: sh

    --logger <plugin>[:options]"
    --logger "<name> <plugin>[:options]" # The quotes are only required on the command line -- config files don't use them

You may set up as many loggers as you like. Named plugins are used for log routing.

A very simple example of split request/error logging (using plain old boring files) would be

.. code-block:: ini

    [uwsgi]
    req-logger = file:/tmp/reqlog
    logger = file:/tmp/errlog

Log routing
-----------

By default all log lines are sent to all declared loggers. If this is not what you want, you can use ``--log-route`` (and ``--log-req-route`` for request loggers) to specify a regular expression to route certain log messages to different destinations.

For instance:

.. code-block:: ini

    [uwsgi]
    logger = mylogger1 syslog
    logger = theredisone redislog:127.0.0.1:6269
    logger = theredistwo redislog:127.0.0.1:6270
    logger = file:/tmp/foobar # This logger will log everything as it's not named
    logger = internalservererror file:/tmp/errors
    # ...
    log-route = internalservererror (HTTP/1.\d 500)
    log-route = mylogger1 uWSGI listen queue of socket .* full

This will log all 500 errors to /tmp/errors, while listen queue full errors will end up in /tmp/foobar.

This is somewhat similar to the :doc:`AlarmSubsystem` (though alarms are usually heavier and should only be used for critical situations).

Logging to files
----------------

``logfile`` plugin -- embedded by default.

.. code-block::

    uwsgi --socket :3031 --logger file:/tmp/uwsgi.log

Logging to sockets
------------------

``logsocket`` plugin -- embedded by default.

You can log to an unconnected UNIX or UDP socket using ``--logger socket:...`` (or ``--log-socket ...``).

.. code-block:: sh

    uwsgi --socket :3031 --logger socket:/tmp/uwsgi.logsock

will send log entries to the Unix socket ``/tmp/uwsgi.logsock``.

.. code-block:: sh

    uwsgi --socket :3031 --logger socket:192.168.173.19:5050

will shoot log datagrams to the UDP address 192.168.173.19 on port 5050.
 
You may also multicast logs to multiple log servers by passing the multicast address:

.. code-block:: sh

    uwsgi --socket :3031 --logger socket:225.1.1.1:1717

Logging to syslog
-----------------

``logsyslog`` plugin -- embedded by default

The ``logsyslog`` plugin routes logs to Unix standard syslog. You may pass an optional ID to send as the "facility" parameter for the log entry.

.. code-block:: sh

    uwsgi --socket :3031 --logger syslog:uwsgi1234

Logging to remote syslog
------------------------

``logrsyslog`` plugin -- embedded by default


The ``logrsyslog`` plugin routes logs to Unix standard syslog residing on a remote server. In addtition to the address+port of the remote syslog server, you may pass an optional ID to send as the "facility" parameter for the log entry.

.. code-block:: sh

    uwsgi --socket :3031 --logger rsyslog:12.34.56.78:12345,uwsgi1234

Redis logger
------------

``redislog`` plugin -- embedded by default.

By default the ``redislog`` plugin will 'publish' each logline to a redis pub/sub queue.

The logger plugin syntax is:

.. code-block:: sh

    --logger redislog[:<host>,<command>,<prefix>]

By default ``host`` is mapped to ``127.0.0.1:6379``, ``command`` is mapped to "publish uwsgi" and ``prefix`` is empty.

So, to publish to a queue called foobar, use ``redislog:127.0.0.1:6379,publish foobar``, etc.

Redis logging is not limited to pub/sub. You could for instance push items into a list with

.. code-block:: sh

    --logger redislog:/tmp/redis.sock,rpush foo,example.com

As error situations could cause the master to block while writing a log line to a remote server, it's a good idea to use ``--threaded-logger`` to offload log writes to a secondary thread.

MongoDB logger
--------------

``mongodblog`` plugin -- embedded by default.

The logger syntax for MongoDB logging (``mongodblog``) is

.. code-block:: sh

    --logger mongodblog[:<host>,<collection>,<node>]

Where ``host`` is the address of the MongoDB instance (default ``127.0.0.1:27017``), ``collection`` names the collection to write log lines into (default ``uwsgi.logs``) and ``node`` is an identification string for the instance sending logs (default: server hostname).

.. code-block:: sh

    --logger mongodblog

will run the logger with default values, while

.. code-block:: sh

    --logger mongodblog:127.0.0.1:9090,foo.bar

will write logs to the mongodb server 127.0.0.1:9090 in the collection ``foo.bar`` using the default node name.

Like with the Redis logger, offloading log writes to a dedicated thread is a good choice.

.. code-block:: ini

    [uwsgi]
    threaded-logger = true
    logger = mongodblog:127.0.0.1:27017,uwsgi.logs_of_foobar
    # As usual, you could have multiple loggers:
    # logger = mongodblog:192.168.173.22:27017,uwsgi.logs_of_foobar
    socket = :3031

ZeroMQ logging
--------------

As with UDP logging you can centralize/distribute logging via ZeroMQ. Build your logger daemon using a ``ZMQ_PULL`` socket:

.. code-block:: python

    import zmq
    
    ctx = zmq.Context()
    
    puller = ctx.socket(zmq.PULL)
    puller.bind("tcp://192.168.173.18:9191")
    
    while True:
        message = puller.recv()
        print message,

Now run your uWSGI server:

.. code-block:: sh

    uwsgi --logger zeromq:tcp://192.168.173.18:9191 --socket :3031 --module werkzeug.testapp:test_app

(``--log-zeromq`` is an alias for this logger.)


Crypto logger (plugin)
----------------------

If you host your applications on cloud services without persistent storage you may want to send your logs to external systems.

However logs often contain sensitive information that should not be transferred in clear.

The ``logcrypto`` plugin logger attempts to solve this issue allowing you to encrypt each log packet and send it over UDP to a server able to decrypt it.

This will send each log packet to an UDP server available at 192.168.173.22:1717 encrypting the text with the secret key ``ciaociao`` with Blowfish in CBC mode.


.. code-block:: sh

   uwsgi --plugin logcrypto --logger crypto:addr=192.168.173.22:1717,algo=bf-cbc,secret=ciaociao -M -p 4 -s :3031

An example server is available at https://github.com/unbit/uwsgi/blob/master/contrib/cryptologger.rb

Graylog2 logger (plugin)
------------------------

``graylog2`` plugin -- not compiled by default.

This plugin will send logs to a Graylog2 server in Graylog2's native GELF format.

.. code-block:: sh

    uwsgi --plugin graylog2 --logger graylog2:127.0.0.1:1234,dsfargeg

Systemd logger (plugin)
-----------------------

``systemd_logger`` plugin -- not compiled by default.

This plugin will write log entries into the Systemd journal.

.. code-block:: sh

    uwsgi --plugin systemd_logger --logger systemd


Writing your own logger plugins
-------------------------------

This plugin, ``foolog.c`` will write your messages in the file specified with --logto/--daemonize with a simple prefix using vector IO.

.. code-block:: c

    #include "../../uwsgi.h"
    
    ssize_t uwsgi_foolog_logger(struct uwsgi_logger *ul, char *message, size_t len) {
    
            struct iovec iov[2];
    
            iov[0].iov_base = "[foo] ";
            iov[0].iov_len = 6;
    
            iov[1].iov_base = message;
            iov[1].iov_len = len;
    
            return writev(uwsgi.original_log_fd, iov, 2);
    }
    
    void uwsgi_foolog_register() {
            uwsgi_register_logger("syslog", uwsgi_syslog_logger);
    }
    
    struct uwsgi_plugin foolog_plugin = {
        .name = "foolog",
        .on_load = uwsgi_foolog_register,
    };