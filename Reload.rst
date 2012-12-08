Reloading of the uWSGI server
=============================

When running with the ``master`` process mode, the uWSGI server can be gracefully restarted without closing the main sockets.

This functionality allows you patch/upgrade the uWSGI server without closing the connection with the web server and losing a single connection.

When you send the `SIGHUP` to the master process it will try to gracefully stop all the workers, waiting for the completion of any currently running requests.

Then it closes all the eventually opened file descriptor not related to uWSGI.

Lastly, it binary patches (using execve()) the uWSGI process image with a new one, inheriting all of the previous file descriptors.

Now the server knows that it is a reloaded instance and will skip all the sockets initialization, reusing the previous ones.

.. note::

   Sending the `SIGTERM` signal will obtain the same result reload-wise but will not wait for the completion of running requests.

   .. seealso:: :doc:`ProcessSignals`

.. note::
 
   The reload functionality can also be used via the uWSGI API as published to the applications being run.

   .. seealso:: :py:func:`uwsgi.reload`

Other (more advanced) ways
==========================

As always in the uWSGI project, there are more ways to accomplish the same result using different techiques.

For very high-loaded sites, solutions like the :doc:`Zerg` mode or the :doc:`SubscriptionSystem` can be a better choice
