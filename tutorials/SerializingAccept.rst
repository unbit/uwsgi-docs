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

In modern times, the vast majority of UNIX systems have evolved, and now the kernel ensure (more or less) only one process/thread is woke up on a connection event.

Ok, problem solved, what we are talking abut ?

select()/poll()/kqueue()/epoll()/...
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In the pre-1.0 era, uWSGI was a lot simpler (and less interesting) than the current form. It did not have the signal framework and it was not able to listen to multiple addresses, for this reason
its loop engine was only calling accept() in each process/thread, and thundering herd (thanks to modern kernels) was not a problem.

