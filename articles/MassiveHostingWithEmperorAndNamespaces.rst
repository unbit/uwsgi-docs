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

We are probably one of the few hosting company making kernel hacking and releasing the vast majority of its software as open source.

Before you get excited, Unbit accepts only Italian customers (we are not racists, it is a policy for avoiding legal problems with the other hosting companies we work with) and our prices
are quite high as we do not make any kind of over-selling (and more important we do not give free-accounts ;)

In more than 8 years me and my co-workers experienced thousands of problems (yes, if you want to enter the internet services market be prepared to invest the vast majority of your time
solving problems created by users without the minimal respect for you as a person ;) so, what you see in the whole uWSGI project is the result of this years
of headaches and non-sleeping nights (and insults by customers)

During summer 2013 i worked a bit with the pythonanywhere.com guys (mainly with Harry Percival).

They heavily use uWSGI features for their service, so they helped popping-up new ideas and solutions in my mind.

In uWSGI 1.9.15 lot of new patches for advanced Linux namespaces usage have been merged.

This article will show one of the approaches you can follow to build your service for hosting unreliable webapps (yes, even if you have the largest collection of pacifist customers, they have to be considered 'unreliable' and 'evil', otherwise you are not a good sysadmin)

What we want to allow to our users
**********************************

- deploy WSGI,PSGI and RACK applications (no CGI and php, albeit technically possible, if you think you can make any kind of money with php hosting you should start finding a second job)
- run cron scripts
- run private services (redis, beanstalkd, memcached...)
- applications can connect to the internet
- ...

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

The "control panel"
*******************

uWSGI 'language' plugins
************************

Linux namespaces
****************

Linux cgroups
*************

uWSGI Emperor and vassals
*************************

Networking
**********

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
