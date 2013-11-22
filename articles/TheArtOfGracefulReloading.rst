The Art of Graceful Reloading
=============================

Author: Roberto De Ioris

The following article is language-agnostic, and albeit uWSGI-specific some of its initial considerations apply to other application servers and platforms too.

What is a "graceful reload" 
***************************

During the life-cycle of your webapp you will reload it hundreds of time.

You need reloading for code updates, you need reloading for changes in the uWSGI configration, you need reloading to reset the state of your app.

Basically reloading is one of the most simple, frequent and DANGEROUS operation you do everytime.

So, why "graceful" ?

Take a traditional (and highly suggested) architecture: a fronted proxy/load-balancer (like nginx) forwardign requests to one or more uWSGI daemons listening on variosu addresses.

If you manage your reloads as "stop the instance" -> "start the instance", the timeslice between the two phases is a brutal disservice to your customers.

The main trick for avoiding it, is not closing the file descriptor mapped to the uWSGI daemon address, and abuse the unix fork() behaviour (read: fiel descriptors are inherited by default) to exec() the 'uwsgi' binary again.

The result is your proxy enqueuing requests to the socket until it will be able to accept() them again with the user/customer only seeing a little slowdown in the first response (the time required for the app to be fully loaded again)


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
