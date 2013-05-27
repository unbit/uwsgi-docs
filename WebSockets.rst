WebSocket support (from 1.9-dev)
================================

In uWSGI 1.9, a high performance websocket (RFC 6455) implementation has been added.

Although many different solutions exist for WebSockets, most of them rely on a higher-level language implementation, that rarely is good enough for topics like gaming or streaming.

The uWSGI websockets implementation is compiled in by default and can be combined with the Channels subsystem (another new feature of the 1.9 tree).

Channels allow you to quickly exchange messages (managed with various Unix IPC techniques) with all of the cores of the uWSGI instance (and pretty soon with other instances too) without the need of an external queue like ZeroMQ or Redis.

Websocket support is sponsored by 20Tab S.r.l. http://20tab.com/

An echo server
**************

This is how a uWSGI websockets application looks like:

.. code-block:: python

   def application(env, start_response):
       # complete the handshake
       uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
       while True:
           msg = uwsgi.websocket_recv()
           uwsgi.websocket_send(msg) 

You do not need to worry about keeping the connection alive or reject dead peers. The ``uwsgi.websocket_recv()`` function will do all of the dirty work for you in background.

Handshaking
***********

Handshaking is the first phase of a websocket connection.

To send a full handshake response you can use the ``uwsgi.websocket_handshake(key[,origin])`` function. Without a correct handshake the connection will never complete.

Sending
*******

Sending data to the browser is really easy. ``uwsgi.websocket_send(msg)`` -- nothing more.

Receiving
*********

This is the real core of the whole implementation.

This function actually lies about its real purpose. It does return a websocket message, but it really also holds the connection
opened (using the ping/pong subsystem) and monitors the stream's status. 

``msg = uwsgi.websocket_recv()``

The function can receive messages from a named channel (see below) and automatically forward them to your websocket connection.

It will always return only websocket messages sent from the browser -- any other communication happens in the background.

Channels
********

Channels are a new feature in uWSGI 1.9. They are a pretty complex (from an implementation point of view) messaging system but are really easy to use for end-users.

Channels must be created on startup using the ``--channel <name>`` option. You can have as many channels you need, but remember that
each channel is pretty expensive as it will allocate 2 file descriptors (via ``socketpair()``) for each core of the instance.

Joining a websocket to a channel will automagically forward all of the messages sent to the channel to the websocket connection.

``uwsgi.websocket_channel_join(channel)``

You can implement a chat room with only few lines of code (really!):

.. code-block:: python

   def application(env, start_response):
       # complete the handshake
       uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
       # join the channel 'room001'
       uwsgi.websocket_channel_join('room001')
       # enter the main cycle
       while True:
           # wait for messages (this will automatically forward channel messages to the socket)
           msg = uwsgi.websocket_recv()
           # when a message is available, forward it to the channel
           uwsgi.channel_send('room001', msg) 

That's all. (Really!)

When you call ``uwsgi.channel_send(...)`` all of the cores blocked in ``uwsgi.websocket_recv()`` will automatically
forward the packet to the browser.


PING/PONG
*********

To keep a websocket connection opened, you should constantly send ping (or pong, see later) to the browser and expect
a response from it. If the response from the browser/client does not arrive in a timely fashion the connection is closed (``uwsgi.websocket_recv()`` will raise an exception). In addition to ping, the ``uwsgi.websocket_recv()`` function send the so called 'gratuitous pong'. They are used
to inform the client of server availability.

All of these tasks happen in background. YOU DO NOT NEED TO MANAGE THEM!

Available proxies
*****************

Unfortunately not all of the HTTP webserver/proxies work flawlessly with websockets.

* The uWSGI HTTP/HTTPS/SPDY router supports them without problems. Just remember to add the ``--http-raw-body`` option.

  .. code-block:: sh

   uwsgi --http :8080 --http-raw-body --wsgi-file myapp.py

* Haproxy works fine.

Languages support
*****************

* Python
* Perl

Concurrency models
******************

* Multithread
* gevent
* Goroutines

wss:// (websockets over https)
******************************

The uWSGI HTTPS router works without problems with websockets. Just remember to use wss:// as the connection scheme in your client code.

Websockets over SPDY
********************

n/a

Routing
*******

.. code-block:: ini

   [uwsgi]
   route = ^/websocket uwsgi:127.0.0.1:3032

Performance tips
****************
