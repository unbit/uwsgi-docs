Massive "secure" Hosting with the Emperor and Linux Namespaces, AKA "Improving pythonanywhere.com"
==================================================================================================

Author: Roberto De Ioris

*** WORK IN PROGRESS ***

Disclaimer
**********

In the following intro i will mention two companies: Unbit and pythonanywhere.com. I work with both (effectively i own the first one :P).

If you think i am making advertising to both, well you are right.

Intro
*****

Since 2005 i work as chief sysadmin in the italian ISP Unbit (http://unbit.it) and as a consultant for various hosting company worldwide.

Unbit is a developer-oriented service, we allow hosting basically anything you want without forcing you to a VPS, simply abusing Linux kernel facilities (it is very similar to what currently Heroku
does but about 5 years before Heroku existed ;)

In 2009 we started the uWSGI project, initially as a WSGI server, then we slowly realized that its paradigms could be applied to all our infrastructure, so now it is becoming
a sort of "hosting platform" for various languages. We plan to use only uWSGI for the whole Unbit hosting stack by 2014.

Before you get excited, Unbit accepts only Italian customers (we are not racists, it is a policy for avoiding legal problems with the other hosting companies we work with) and our prices
are quite high as we do not make any kind of over-selling (and more important we do not give free-accounts ;)

In more than 8 years me and my co-workers experienced thousands of problems (yes, if you want to enter the internet services market be prepared to invest the vast majority of your time
solving problems created by users without the minimal respect for you as a person ;) so, what you see in the whole uWSGI project is the result of this years
of headaches and non-sleeping nights (and insults by customers)

During summer 2013 i worked a bit with the pythonanywhere.com guys (mainly with Harry Percival).

They heavily use uWSGI features for their service, so they helped popping-up new ideas and solutions in my mind.

In uWSGI 1.9.15 lot of new patches for advanced Linux namespaces usage have been merged, thanks to the collaboration with pythonanywhere.com guys.

Based on the experiences of the two companies, this article will show one of the approaches you can follow to build your service for hosting unreliable webapps (yes, even if you have the largest collection of pacifist customers, they have to be considered 'unreliable' and 'evil', otherwise you are not a good sysadmin).

It is not a step-by-step tutorial, but some kind of cookbook to give you some basis for improving and adapting the concepts for your needs.

What we want to allow to our users
**********************************

- deploy WSGI,PSGI and RACK applications (no CGI and php, albeit technically possible, if you think you can make any kind of money with php hosting you should start finding a second job)
- run cron scripts
- run private services (redis, beanstalkd, memcached...)
- applications can connect to the internet
- multiple domain names can map to the same instance

...and what we want to forbid
*****************************

- users cannot see the processes of the other accounts in the machine. Their init process has to be the uWSGI master
- users cannot see the files of the other accounts in the machine
- users cannot connect to private services (memcached, redis...) of the other accounts in the machine
- users cannot read/write ipc semaphores, shared memory and message queues of the other accounts in the machine
- users cannot allocate more memory than the amount they payed for
- users cannot use more cpu power than the amount they payed for

The Operating System
********************

The Webserver
*************

As we do not need to worry about php and the abuse of .htaccess files, we can choose any server we want.

We prefer nginx (even if we [Unbit] are slowly moving to the uWSGI http/https/spdy router), but you can use whatever you like.

The "control panel"
*******************

This is the thing you need to develop, the more your panel is usable and powerful the more your users will be happy.

Your control panel is probably the thing will make your hosting company successfull.

The objective of your control panel is generating "vassal files" (see below). Vassal files can be .ini, xml, yaml and json (unless you have particular reasons to use other formats).

The vassal file contains the whole structure of a customer micro-system. As soon as a vassal file is created it will be deployed (and when it is changed it will be reloaded)

uWSGI 'language' plugins
************************

We want to support multiple kind of applications. The better approach will be having a single uWSGI binary and a series of 'language plugins' (one for each language you want to support).

You can support multiple versions of the same language. Just build the corresponding plugin.

In Unbit we make an extremely modular uWSGi distribution (basically all is a plugin). This is required as we account any MB of memory
so we allow users to enable only the required features to gain much memory as possible.

If you are still not a black-belt in uWSGI mastering, i suggest you to start with the included 'nolang' build profile.

It will build a standard uwsgi binary without any language builtin.

...

Linux namespaces
****************

Linux cgroups
*************

uWSGI Emperor and vassals
*************************

Networking
**********

This is probably the most complex part

Cron
****

Static file serving
*******************



Additional daemons
******************

Bonus: KSM
**********

What is missing
***************

- SSH/shells
- Accounting network usage
- Scaling to multiple machines
