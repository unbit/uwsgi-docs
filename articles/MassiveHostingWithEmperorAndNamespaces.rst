Massive "secure" Hosting with the Emperor and Linux Namespaces, AKA "Improving pythonanywhere,com"
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
