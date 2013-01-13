WebSockets Support (from 1.5-dev)
=================================


In uWSGI 1.5 a high performance websockets (rfc 6455) implementation has been added.

Albeit lot of different solutions exist for the problem, most of them rely on higher-level languages implementation, that rarely
are good enough for topics like gaming or streaming.

The uWSGI websockets implementation is compiled in by default and can be combined with the Channels subsystem (another new feature of the 1.5 tree)

Channels allows you to fast exchange messages (it is all managed with various unix ipc techniques) with all of the cores of the instance (and pretty soon with other instances too) without the need of an external queue
(like zeromq or redis)

Websockets support is sponsored by 20Tab S.r.l. http://20tab.com/

An echo server
**************

This is how a uWSGI-websockets application looks like:

.. code-block :: python

   def application(env, start_response):
       # complete the handshake
       uwsgi.websocket_handshake(env['HTTP_SEC_WEBSOCKET_KEY'], env.get('HTTP_ORIGIN', ''))
       while True:
           msg = uwsgi.websocket_recv()
           uwsgi.websocket_send(msg) 


You do not need to worry about keeping the connection alive or reject dead peers. The uwsgi.websocket_recv()
function will do all of the dirty work for you in background.

Handshaking
***********

Handshaking is the first phase of a websocket connection.

To send a full handshake response you can use that function

uwsgi.websocket_handshake(key[,origin])

without correct handshaking the connection will never complere

Sending
*******

Sending data to the browser is realy easy:

uwsgi.websocket_send(msg)

Nothing more

Receiving
*********

This is the real core of the whole implementation.

This function lies about its real purpose. It returns a websocket message, but it really holds the connection
openend (using the ping/pong subsystem) and monitor the whole status. 

msg = uwsgi.websocket_recv()

The function can receive messages from a named channel (see below) and automatically forward them to your websocket connection
(the function will always returns ONLY websocket messages sent from the browser, other communications happens in background)

Channels
********

Channels are a feature of uWSGI 1.5. They are a pretty complex (from an implementation point of view) messaging system
but are really easy to use.

Channels must be created on startup using the --channel <name> option. You can have all of the channels you need, but remember that
each channel is preatty expensive as it will allocate 2 decriptor (via socketpair()) for each core of the instance.

Joining a websocket to a channel will automagically forward all of the messages sent to the channel to the websocket connection.

uwsgi.websocket_channel_join(channel)

PING/PONG
*********



Available proxies
*****************

uwsgi http router
haproxy

Languages support
*****************

python
perl

Concurrency models
******************

multithread
gevent
goroutines

wss:// (websockets over https)
******************************

Websockets over SPDY
********************

Routing
*******

.. code-block:: ini

   [uwsgi]
   route = ^/websocket uwsgi:127.0.0.1:3032

Performance tips
****************
