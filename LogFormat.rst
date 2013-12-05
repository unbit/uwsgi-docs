Formatting uWSGI requests logs 
==============================

uWSGI has a ``--logformat`` option for building custom request loglines. The
syntax is simple:

.. code-block:: ini

   [uwsgi]
   logformat = i am a logline reporting "%(method) %(uri) %(proto)" returning with status %(status)

All of the variables marked with ``%()`` are substituted using specific rules.
Three kinds of logvars are defined ("offsetof", functions, and user-defined).

offsetof
********

These are taken blindly from the internal ``wsgi_request`` structure of the current request.

* ``%(uri)`` -> REQUEST_URI
* ``%(method)`` -> REQUEST_METHOD
* ``%(user)`` -> REMOTE_USER
* ``%(addr)`` -> REMOTE_ADDR
* ``%(host)`` -> HTTP_HOST
* ``%(proto)`` -> SERVER_PROTOCOL
* ``%(uagent)`` -> HTTP_USER_AGENT (starting from 1.4.5)
* ``%(referer)`` -> HTTP_REFERER (starting from 1.4.5)

functions
*********

These are simple functions called for generating the logvar value:

* ``%(status)`` -> HTTP response status code
* ``%(micros)`` -> response time in microseconds
* ``%(msecs)`` -> response time in milliseconds
* ``%(time)`` -> timestamp of the start of the request
* ``%(ctime)`` -> ctime of the start of the request
* ``%(epoch)`` -> the current time in Unix format
* ``%(size)`` -> response body size + response headers size (since 1.4.5)
* ``%(ltime) -> human-formatted (Apache style)`` request time (since 1.4.5)
* ``%(hsize)`` -> response headers size (since 1.4.5)
* ``%(rsize)`` -> response body size (since 1.4.5)
* ``%(cl)`` -> request content body size (since 1.4.5)
* ``%(pid)`` -> pid of the worker handling the request (since 1.4.6)
* ``%(wid)`` -> id of the worker handling the request (since 1.4.6)
* ``%(switches)`` -> number of async switches (since 1.4.6)
* ``%(vars)`` -> number of CGI vars in the request (since 1.4.6)
* ``%(headers)`` -> number of generated response headers (since 1.4.6)
* ``%(core)`` -> the core running the request (since 1.4.6)
* ``%(vsz)`` -> address space/virtual memory usage (in bytes) (since 1.4.6)
* ``%(rss)`` -> RSS memory usage (in bytes) (since 1.4.6)
* ``%(vszM)`` -> address space/virtual memory usage (in megabytes) (since 1.4.6)
* ``%(rssM)`` -> RSS memory usage (in megabytes) (since 1.4.6)
* ``%(pktsize)`` -> size of the internal request uwsgi packet (since 1.4.6)
* ``%(modifier1)`` -> modifier1 of the request (since 1.4.6)
* ``%(modifier2)`` -> modifier2 of the request (since 1.4.6)
* ``%(metric.XXX)`` -> access the XXX metric value (see :doc:`Metrics`)
* ``%(rerr)`` -> number of read errors for the request (since 1.9.21)
* ``%(werr)`` -> number of write errors for the request (since 1.9.21)
* ``%(ioerr)`` -> number of write and read errors for the request (since 1.9.21)
* ``%(tmsecs)`` -> timestamp of the start of the request in milliseconds since the epoch (since 1.9.21)
* ``%(tmicros)`` -> timestamp of the start of the request in microseconds since the epoch (since 1.9.21)

User-defined logvars
********************

You can define logvars within your request handler. These variables live only
per-request.

.. code-block:: python

   import uwsgi
   def application(env, start_response):
       uwsgi.set_logvar('foo', 'bar')
       # returns 'bar'
       print uwsgi.get_logvar('foo')
       uwsgi.set_logvar('worker_id', str(uwsgi.worker_id()))
       ...

With the following log format you will be able to access code-defined logvars:

.. code-block:: sh

   uwsgi --logformat 'worker id = %(worker_id) for request "%(method) %(uri) %(proto)" test = %(foo)'

Apache-style combined request logging
*************************************

To generate Apache-compatible logs:

.. code-block:: ini

   [uwsgi]
   ...
   log-format = %(addr) - %(user) [%(ltime)] "%(method) %(uri) %(proto)" %(status) %(size) "%(referer)" "%(uagent)"
   ...

Hacking logformat
*****************

To add more C-based variables, open ``core/logging.c`` and add them after
existing ones (before ``// logvar``, though), for example:

.. code-block:: c

    if (!uwsgi_strncmp(ptr, len, "uri", 3)) {
            logchunk->pos = offsetof(struct wsgi_request, uri);
            logchunk->pos_len = offsetof(struct wsgi_request, uri_len);
    }
    else if (!uwsgi_strncmp(ptr, len, "method", 6)) {
            logchunk->pos = offsetof(struct wsgi_request, method);
            logchunk->pos_len = offsetof(struct wsgi_request, method_len);
    }
    else if (!uwsgi_strncmp(ptr, len, "user", 4)) {
            logchunk->pos = offsetof(struct wsgi_request, remote_user);
            logchunk->pos_len = offsetof(struct wsgi_request, remote_user_len);
    }
    else if (!uwsgi_strncmp(ptr, len, "addr", 4)) {
            logchunk->pos = offsetof(struct wsgi_request, remote_addr);
            logchunk->pos_len = offsetof(struct wsgi_request, remote_addr_len);
    }
    else if (!uwsgi_strncmp(ptr, len, "host", 4)) {
            logchunk->pos = offsetof(struct wsgi_request, host);
            logchunk->pos_len = offsetof(struct wsgi_request, host_len);
    }
    else if (!uwsgi_strncmp(ptr, len, "proto", 5)) {
            logchunk->pos = offsetof(struct wsgi_request, protocol);
            logchunk->pos_len = offsetof(struct wsgi_request, protocol_len);
    }
    else if (!uwsgi_strncmp(ptr, len, "status", 6)) {
            logchunk->type = 3;
            logchunk->func = uwsgi_lf_status;
            logchunk->free = 1;
    }

For function-based vars the prototype is:

.. code-block:: c

   ssize_t uwsgi_lf_foobar(struct wsgi_request *wsgi_req, char **buf);

where ``buf`` is the destination buffer for the logvar value (will be
automatically freed if you set ``logchunk->free`` as in the previous
``"status"``-related C code).

.. code-block:: c

   ssize_t uwsgi_lf_status(struct wsgi_request *wsgi_req, char **buf) {
           *buf = uwsgi_num2str(wsgi_req->status);
           return strlen(*buf);
   }
