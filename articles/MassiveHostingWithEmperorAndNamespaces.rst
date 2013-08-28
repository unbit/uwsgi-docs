Massive "secure" Hosting with the Emperor and Linux Namespaces, AKA "Improving pythonanywhere.com"
==================================================================================================

Author: Roberto De Ioris

Intro
*****

During summer 2013 i worked a bit with the pythonanywhere.com guys (mainly with Harry Percival).
They heavily use uWSGI features for their service, so they helped popping-up new ideas and solutions in my mind.

During 1.9.15 development cycle lot of new patches for advanced Linux namespaces usage have been merged.
This article will show one of the approaches you can follow to host unreliable webapps (yes, even if you have the largest collection of pacifist customers, they have to be considered 'unreliable' and 'evil', otherwise you are not a good sysadmin)

What we want to allow to our users
**********************************

...and what we want to forbid
*****************************

- users cannot see the processes of the other accounts in the machine. Their init process has to be the uWSGI master
- users cannot see the files of the other accounts in the machine
- users cannot connect to private services (memcached, redis...) of the other accounts in the machine
- users cannot read/write ipc semaphores, shared memory and message queues of the other accounts in the machine
- users cannot allocate more memory than the amount they payed for
- users cannot use more cpu power than the amount they payed for

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
