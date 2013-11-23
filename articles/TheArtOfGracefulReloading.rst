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

Finally you could have made an application error in your just committed code, so uWSGI will not start, or will start sending wrong things (or errors...)

Reloads (brutal or graceful) can easily fail.

The listen queue
****************


Pre-fork()'ing VS lazy
**********************

Standard (default/boring) graceful reload (aka SIGHUP)
******************************************************

Workers reloading in lazy apps mode
***********************************

Chain relading (lazy apps)
**************************

Zerg mode
*********

The Zerg dance
**************

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
