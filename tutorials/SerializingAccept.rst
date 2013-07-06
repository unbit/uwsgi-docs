Serializing accept(), AKA Thundering Herd, AKA the Zeeg Problem
===============================================================

One of the hystorical problems in the UNIX world is the "thundering herd".

What is it ?

Take a process binding to a networking address (it could be AF_INET, AF_UNIX or whatever you want) and then forking itself:

.. code-block:: c

   int s = socket(...)
   bind(s, ...)
   listen(s, ...)
   fork()
   
after having forked itself a bunch of times, each of the process will generally start blocking on accept()

.. code-block:: c

   for(;;) {
       int client = accept(...);
       if (client < 0) continue;
       ...
   }
   
The funny problem is that on older/classic UNIX, accept() is woke up in each process blocked on it.

That means a vast amount of wasted cpu cycles (the kernel scheduler has to give control to all of the sleeping processes waiting on that socket)

This behaviour (for various reasons) is amplified when instead of processes you use threads (so, you have multiple threads blocked on accept())

The "de-facto" soluction was placing a lock before the accept() call to serialize its usage:

.. code-block:: c

   for(;;) {
       lock();
       int client = accept(...);
       unlock();
       if (client < 0) continue;
       ...
   }
   
For threads dealing with locks is generally easier, but for processes you have to fight with system-specific solutions or fallback to the venerable SysV ipc
subsystem (more on this later)

In modern times, the vast majority of UNIX systems have evolved, and now the kernel ensure (more or less) only one process/thread is woke up on a connection event.

Ok, problem solved, what we are talking abut ?

select()/poll()/kqueue()/epoll()/...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the pre-1.0 era, uWSGI was a lot simpler (and less interesting) than the current form. It did not have the signal framework and it was not able to listen to multiple addresses, for this reason
its loop engine was only calling accept() in each process/thread, and thundering herd (thanks to modern kernels) was not a problem.

Evolution has a price, so after a bit the standard loop engine of a uWSGI process/thread moved from:

.. code-block:: c

   for(;;) {
       int client = accept(s, ...);
       if (client < 0) continue;
       ...
   }
   
to a more "complex":

.. code-block:: c

   for(;;) {
       int interesting_fd = wait_for_fds();
       if (fd_need_accept(interesting_fd)) {
           int client = accept(interesting_fd, ...);
           if (client < 0) continue;
       }
       else if (fd_is_a_signal(interesting_fd)) {
           manage_uwsgi_signal(interesting_fd);
       }
       ...
   }
   
The problem is now the wait_for_fds() example function: it will call something like select(), poll() or the more modern epoll() and kqueue()

This kind of system calls are "monitors" for file descriptors, and they are woke up in all of the processes/threads waiting for the same file descriptor.

Before you start blaming your kernel developers, this is the right approach, as the kernel cannot knows if you are waiting for those file descriptors to call accept() or to make something funnier.

So, welcome again to the thundering herd.

Application Servers VS WebServers
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The popular, battle tested, solid, multiprocess reference webserver is for sure Apache HTTPD.

It survived decades of IT evolutions and its still one of the most important technologies powering the whole Internet.

Born as multiprocess-only, apache had to always deal with the thundering herd problem and they solved it using SysV ipc semaphores.

Even on modern Apache releases, stracing one of its process you will see something like that (it is a Linux system):

.. code-block:: c

   semop(...); // lock
   epoll_wait(...);
   accept(...);
   semop(...); // unlock
   ... // manage the request
   
the SysV semaphore protect your epoll_wait from thundering herd.

So, another problem solved, the world is a such a beatiful place... but ....

```SysV IPC is not good for application servers :(```

   



