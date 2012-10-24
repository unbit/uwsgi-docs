Reloading of the uWSGI server
=============================

The uWSGI server can be gracefully restarted without closing the main sockets.

This functionality allows you patch/upgrade the uWSGI server without closing the connection with the web server and losing a single connection.

When you send the `SIGHUP` to the master process it will try to gracefully stop all the workers, waiting for the completion of any currently running requests.

Then it closes all the eventually opened file descriptor not related to uWSGI.

Lastly it assigns the server socket descriptor to a fixed, known file descriptor (number 3) and calls `execve` with the original args and environment of the uWSGI process.

When the process image is overwritten the new server is alive and checks if it is a "respawned" instance:

.. code-block:: c

   if (!getsockopt(3, SOL_SOCKET, SO_TYPE, &socket_type, &socket_type_len)) {
       fprintf(stderr, "...fd 3 is a socket, i suppose this is a graceful reload of uWSGI, i will try to do my best...\n");
       is_a_reload = 1;
       serverfd = 3;
   }

Now the server knows that it is a reloaded instance and will skip all the socket initialization.

.. note::

   Sending the `SIGTERM` signal will obtain the same result reload-wise but will not wait for the completion of running requests.

   .. seealso:: :doc:`Signals`



