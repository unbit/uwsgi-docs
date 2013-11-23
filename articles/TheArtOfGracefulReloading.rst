The Art of Graceful Reloading
=============================

Author: Roberto De Ioris

The following article is language-agnostic, and albeit uWSGI-specific some of its initial considerations apply to other application servers and platforms too.

All of the described techniques assumes a modern (>=1.4) uWSGI release with the master process enabled.

What is a "graceful reload" 
***************************

During the life-cycle of your webapp you will reload it hundreds of time.

You need reloading for code updates, you need reloading for changes in the uWSGI configuration, you need reloading to reset the state of your app.

Basically reloading is one of the most simple, frequent and DANGEROUS operation you do everytime.

So, why "graceful" ?

Take a traditional (and highly suggested) architecture: a fronted proxy/load-balancer (like nginx) forwarding requests to one or more uWSGI daemons listening on various addresses.

If you manage your reloads as "stop the instance" -> "start the instance", the timeslice between the two phases is a brutal disservice to your customers.

The main trick for avoiding it, is not closing the file descriptor mapped to the uWSGI daemon address, and abuse the unix fork() behaviour (read: file descriptors are inherited by default) to exec() the 'uwsgi' binary again.

The result is your proxy enqueuing requests to the socket until it will be able to accept() them again with the user/customer only seeing a little slowdown in the first response (the time required for the app to be fully loaded again)

Another important step of graceful reload is avoid destroying workers/threads that are still managing requests. Obviously requests could be stuck, so you should have a timeout for running workers (in uWSGI it is called the ``worker's mercy`` and it has a default value of 60 seconds)

This kind of trick is pretty easy to accomplish and basically all of the modern servers/application servers do it (more or less)

But, as always, the world is an ugly place and lot of problems arise, and the "inherited sockets" approach is often not enough

Things go wrong
***************

We have seen that holding the uWSGI sockets alive, allows the proxy webserver to enqueue requests without spitting out error
to the clients. This is true only if your app restart fast, and sadly this could not happen.

Framework like Ruby on Rails or Zope are really slow in starting up by default, your app could have a slow startup by itself, or your machine could
be so loaded that every process generation (fork() ) take ages.

In addition to this, your site could be so famous that even if your app restart in a couple of seconds the queue of your sockets could be filled upm forcing the proxy server
to raise an error.

Do no forget your workers/threads still running requests could block the reload for various seconds, more seconds than your proxy server could tolerate.

Finally you could have made an application error in your just committed code, so uWSGI will not start, or will start sending wrong things (or errors...)

Reloads (brutal or graceful) can easily fail.

The listen queue
****************

Let's start with the dream of every webapp developer: success

Your app is visited by thousand of clients and you obviously make money with it. Unfortunately it is a very complex app and requires
10 seconds to warm up.

During graceful reloads, you expect new clients to wait 10 seconds (worst case) to start seeing contents, unfortunately, you have
hundreds of concurrent requests, so the first 100 customers will wait for the server warm up, while the others will get an error from the proxy.

This happens because the default listen queue of uWSGI is 100 slot. Before you ask, it is an average value choosen by the maximum value allowed by default by your kernel.

Each operating system has a default limit (Linux has 128 for example), so before increasing it you need to increase your kernel limit.

So, once your kernel is ready, you can increase the listen queue to the maximum number of users you expect to enqueue during a reload.

To increase the listen queue you use the ``--listen <n>`` option where <n> is the maximum number of slots

To raise kernel limits, you should check your os docs, some example:

sysctl ``kern.ipc.somaxcon`` on FreeBSD

``/proc/sys/net/core/somaxconn`` on Linux

Waiting instead of errors is good, no errors and no waiting is even better
**************************************************************************

This is the focus of this article.

We have seen how to increase the tolerance of your proxy during application server reloading.

The customers will wait instead of getting scary errors, but we all want to make money, so why force them to wait ?

We want zero-downtime and zero-wait


Pre-fork()'ing VS lazy-apps VS lazy
***********************************

This is one of the controversial choices of the uWSGI project.

By default uWSGI loads the whole application in the first process and after the app is loaded it fork() itself multiple times.

This is the common UNIX pattern, it could highly reduce the memory usage of your app, allows lot of funny tricks and on some languages
can bring you lot of headaches.

Albeit its name, uWSGI born as a Perl application server (it was not called uWSGI and it was not open source), and in the Perl world preforking
is generally the blessed way.

This is not true for lot of other languages, platform and frameworks, so before starting dealing with uWSGI you should choose how to manage fork() in your stack.

Seeing it from the "graceful reloading" point of view, preforking extremely speed up things, your app is loaded only one time, and spawning additional worker
will be really fast. Expecially for frameworks/languages doing lot of disk access for finding modules, avoiding it for each worker of your stack will increase startup times.

On the contrary, the preforking approach forces you to reload the whole stack whenever you make code changes instead of reloading only the workers.

In addition to this, your app could need preforking for the way it has been developed.

Remember: lazy-apps is different from lazy, the first one only instruct uWSGI to load the application one time per-worker, while the second is more invasive (and generally discouraged) as it changes lot of internal defaults.

The following approaches will show you how to accomplish zero-downtime/wait reloads in both preforking and lazy modes.

Each approach has pros and cons, choose carefully

Standard (default/boring) graceful reload (aka SIGHUP)
******************************************************

to trigger it: send SIGHUP to the master, write 'r' to the master fifo, use --touch-reload, call uwsgi.reload() api

In preforking and --lazy-apps mode, it will wait for running workers, it will close all of the file descriptors except the one mapped to sockets and will call exec() on itself

In --lazy mode, it will wait for runnign workers and then it will restart all of them. This means you cannot change uWSGI options during this kind of reload. Remember --lazy is discouraged !!!

Pros: easy to manage, no corner-case problems, no inconsistent states, basically full reset of the instance

Cons: the ones we seen before, listen queue filling up, stuck workers, potential long waiting times.


Workers reloading in lazy-apps mode
***********************************

requires: --lazy-apps

to trigger it: write 'w' to the master fifo, use --touch-workers-reload

this will wait for running workers and then it will restart each of them.

Pros: avoid restarting the whole instance

Cons: no user-experience improvements over standard graceful reload, it is only a shortcut for situation where code updates do not imply instance reconfiguration

Chain reloading (lazy apps)
***************************

requires: --lazy-apps

to trigger it: write 'c' to the master fifo, use --touch-chain-reload

This is the first approach improving user-experience

When triggered it will start one worker at time, the following worker is not reloaded until the previous one is ready to accept new requests.

Pros: potentially highly reduce waiting clients, reduce the load of the machine during reloads (mo multiple processes loading the same code)

Cons: only useful for code updates, you need a good amount of workers to get a better user-experience

Zerg mode
*********

requires: a zerg server or a zerg pool

to trigger it: run the instance in zerg mode

This is the first approach using multiple instances of the same application to increase user experience.

Zerg mode works by making use of the venerable "fd passing over unix sockets" technique.

Basically an external process (the zerg server/pool) binds to the various sockets required by your app. Your uWSGI instance instead of binding by itself, asks the zerg server/pool to pass it the file descriptor. This means multiple unrelated instances
can ask for the same file descriptors and works togheter.

Zerg mode born for improving auto-scalability, but soon became one of the most loved approaches for zero-downtime reloading.


SO_REUSEPORT (Linux >= 3.9 and BSDs)
************************************

The Black Art (for rich people): master forking
***********************************************

Subscription system
*******************

References
**********

:doc:`../MasterFIFO`

:doc:`../Hooks`

:doc:`../Zerg`
