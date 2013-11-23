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

This kind of tricks are pretty easy to accomplish and basically all of the modern servers/application servers do it (more or less)

But, as always, the world is an ugly place and lot of problems arise, and the "inherited sockets" approach is often not enough

Things go wrong
***************

We have seen that holding the uWSGI sockets alive, allows the proxy webserver to enqueue requests without spitting out errors
to the clients. This is true only if your app restart fast, and sadly this could not always happen.

Frameworks like Ruby on Rails or Zope are really slow in starting up by default, your app could have a slow startup by itself, or your machine could
be so overloaded that every process generation (fork()) takse ages.

In addition to this, your site could be so famous that even if your app restarts in a couple of seconds the queue of your sockets could be filled up forcing the proxy server
to raise an error.

Do no forget your workers/threads still running requests could block the reload for various seconds, more seconds than your proxy server could tolerate.

Finally you could have made an application error in your just-committed code, so uWSGI will not start, or will start sending wrong things (or errors...)

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

.. note::

   This is only one of the reasons to tune the listen queue, but do not blindly set it to huge values as a way to increase availability

Proxy timeouts
**************

They are another thing you need to check if your reloads take lot of time.

Generally proxies allow you to set a "connect" timeout and a "read" timeout.

The first one is the maximum amount of time the proxy will wait for a successfull connection, the second one is the maximum amount of time
the server will be able to wait for data before giving up.

Generally when tuning for reloads, only the "connection" timeout matters. This timeout enters the game in the timeslice between uWSGI bind to an interface (or inherit it) and the call to accept()

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

Example:

spawn a zerg pool exposing 127.0.0.1:3031 to the unix socket /var/run/pool1

.. code-block:: ini

   [uwsgi]
   master = true
   zerg-pool = /var/run/pool1:127.0.0.1:3031
   
now spawn one or more instances attached to the zerg pool

.. code-block:: ini

   [uwsgi]
   ; this will give access to 127.0.0.1:3031 to the instance
   zerg = /var/run/pool1

When you want to make code or options updates, just spawn a new instanced attached to the zerg, and shutdown the old one when the new one is ready for accepting requests

The so-called ``zerg dance`` is a trick for automating this kind of reloads. There are various ways to accomplish it, the objective is automatically
``pause`` or ``destroy`` the old instance when the new one is fully ready and able to accept requests. More on this below.

Pros: potentially the silver bullet, allows instances with different options to cooperate for the same app

Cons: requires an additional process, can be hard to master, a reload requires a whole copy of the whole uWSGI stack

The Zerg Dance: Pausing instances
*********************************

We all make mistakes, sysadmins must improve their skill for fast solving mistakes, focusing in avoiding them is a waste of time. Unfortunately we are all humans.

Rolling back deployments could be your life-safer.

We have seen how zerg mode can allow us to have multiple instances asking on the same socket. In the previous chapter we used it to spawn the new instance working togheter with the old one.
Now, instead of shutting down the old instance, why not ``pause`` it. A paused instance is like the standby mode of your TV. It consumes very few resources, but you can bring it back on very fast.

``Zerg Dance`` is the battle-name for the procedure of continuosly swapping instances during reloads. Every reload results in a 'sleeping' instance and a running one. Following reloads destroy the old sleeping instance and transform the old running to the sleeping one and so on.

There are literally dozens of ways to accomplish the ``Zerg Dance``, the fact you can easily integrate scripts in your reloading procedures makes the approach extremey powerful and customizable.

Here we will see the one requiring zero-scripting, it could be the less versatile (and requires at least uWSGI 1.9.21), but should be a good starting point for improving things.

The Master Fifo, is the best way for managing instances instead of relying on unix signals. Basicaly you write 'single char' commands to gover the instance.

The funny thing about Master Fifo's is that you can have multiple of them configured for your instance and swap from one to another very easily.

An example will clarify things:

we spawn an instance with 3 master fifo's: new (the default one), running  and sleeping

.. code-block:: ini

   [uwsgi]
   ; fifo '0'
   master-fifo = /var/run/new.fifo
   ; fifo '1'
   master-fifo = /var/run/running.fifo
   ; fifo '2'
   master-fifo = /var/run/sleeping.fifo
   ; attach to zerg
   zerg = /var/run/pool1
   ; other options ...
   
by default the ``new`` one will be active (read: will be able to process commands)

Now we want to spawn a new instance, that once is ready to accept requests will put the old one in sleeping mode. For doinf it we will use uWSGI advanced hooks.

Hooks allows you to 'make things' in various phases of the uWSGI life-cycle.

When the new instance is ready we want to force the old instance to start working on the sleeping fifo and to be put in ``pause`` mode

.. code-block:: ini

   [uwsgi]
   ; fifo '0'
   master-fifo = /var/run/new.fifo
   ; fifo '1'
   master-fifo = /var/run/running.fifo
   ; fifo '2'
   master-fifo = /var/run/sleeping.fifo
   ; attach to zerg
   zerg = /var/run/pool1
   
   ; hooks
   
   ; destroy the currently sleeping instance
   if-exists = /var/run/sleeping.fifo
     hook-accepting1-once = writefifo:/var/run/sleeping.fifo Q
   endif =
   ; force the currently running instance to became sleeping (slot 2) and place it in pause mode
   if-exists = /var/run/running.fifo
     hook-accepting1-once = writefifo:/var/run/running.fifo 2p
   endif =
   ; force this instance to became the running one (slot 1)
   hook-accepting1-once = writefifo:/var/run/new.fifo 1
   
The ``hook-accepting1-once`` phase is run one time per instance soon after the first worker is ready to accept requests

The ``writefifo`` command allows writing to fifo's but without failing if the other peers is not connected (this is different from a simple 'write' command that would fail or completely block when dealing with bad fifo's)

Both features have been added only in uWSGI 1.9.21, on older releases you can use the ``--hook-post-app`` option instead of ``--hook-accepting1-once`` but will lose the 'once' feature, so it will work reliably only in preforking mode.

Instead of ``writefifo`` you can use the shell variant ``exec:echo <string> > <fifo>``

Now start running instances with the same config files over and over again. If all goes well you shoudl always end with two instances, one sleeping and one running.

Finally if you want to bring back a sleeping instance just do:

.. code-block:: sh

   # destroy the running instance
   echo Q > /var/run/running.fifo
   # unpause the sleeping instance and set it as the running one
   echo p1 > /var/run/sleeping.fifo
   
Pros: truly zero-downtime isolation

Cons: requires high-level uWSGI and UNIX skills

SO_REUSEPORT (Linux >= 3.9 and BSDs)
************************************

On recent Linux kernels and modern BSDs you may try the ``--reuse-port`` options.

This option allows multiple unrelated instances to bind on the same network address.

You may see it as a kernel-level zerg mode. Basically all of the Zerg approaches can be followed

Once you add ``--reuse-port`` to you instance, all of the sockets will have the SO_REUSEPORT flag set.

Pros: similar to zerg mode, could be even easier to manage

Cons: requires kernel support, could lead to inconsistent states, you lose the hability to use TCP addresses as a way to avoid incidental multiple instances running

The Black Art (for rich and brave people): master forking
*********************************************************

to trigger it: write 'f' to the master fifo

This is the most dangerous of the reloading ways, but once mastered could lead to pretty cool results.

The approach is calling fork() in the master, close all of the file descriptors excluded the socket-related once, and exec() a new uWSGI instance.

You will end with two specular uWSGI instances working on the same sockets set

The scary thing about it is how easy (just write a single char to the master fifo) is to trigger it...

With a bit of mastery you can implement the zerg dance on top of it.

Pros: does not require kernel support nor an additional process, pretty fast

Cons: a whole copy for each reload, inconstent states all over the place (like pidfiles, logging.., the master fifo commands could help fixing them)

Subscription system
*******************

This is probably the best approach when you can count on multiple servers

You add the ``fastrouter`` between your proxy server (nginx) and your instances.

Instances will 'subscribe' to the fastrouter that will pass requests from nginx to them, load balancing and constantly monitoring all of them.

Subscriptions are simple udp packets that instruct the fastrouter about which domain map to which instance/instances

As you can subscribe, you can unsubscribe too, and this is where the magic happens:

.. code-block:: ini

   [uwsgi]
   subscribe-to = 192.168.0.1:4040:unbit.it
   unsubscribe-on-graceful-reload = true
   ; all of the required options ...
   
adding ``unsubscribe-on-graceful-reload`` will force teh instance to send an 'unsubscribe' packet to the fastrouter, so until it will not be back no requests will be sent to it.

Pros: low-cost zero-downtime, finally a KISS approach

Cons: requires a subscription server (like the fastrouter) that introduces overhead (even if we are talking about microseconds)


Do not COPY&PASTE !!!
*********************

Please, turn on your brain and try to adapt the showed config to your needs, or invent new ones.


References
**********

:doc:`../MasterFIFO`

:doc:`../Hooks`

:doc:`../Zerg`

:doc:`../Fastrouter`

:doc:`../SubscriptionServer`
