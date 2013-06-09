The uWSGI build system
======================

- This is updated to 1.9.13 -

This page describes how the uWSGI build system works and how it can be customized

uwsgiconfig.py
**************

This is the python script aimed at calling the various compile/link stage.

During 2009, when uWSGI guidelines (and mantra) started to be defined, people agreed that autotools, cmake and friends
was not loved by the vast majority of sysadmins. Albeit they are pretty standardized, the amount of packages needed and the incompatibility
between them (expecially in the autotools world) was a problem for a project with fast development/evolution where "compile from sources" was, is and very probably will be the best way
to get the best from the product.

For such a reason, to compile uWSGI you only need to have a c compiler suite (gcc, clang...) and a python interpreter. Someone could argue that perl
could have been a better choice, and maybe it is the truth (it is generally installed by default in lot of operating systems), but we decided to stay with python mainly
because when uWSGI started it was a python-only application. (Obviously if you want to develop an alternative build system you are free to do it)

The uwsgiconfig.py basically detect the availabel features in the system and build a uwsgi binary (and eventually its plugins) using the
so called 'build profile'

build profiles
**************

First example
*************

CC and CPP
**********

CPUCOUNT
********

UWSGI_FORCE_REBUILD
*******************

Plugins and uwsgiplugin.py
**************************

UWSGI_INCLUDES
**************

UWSGI_EMBED_PLUGINS
*******************

UWSGI_BIN_NAME
**************

CFLAGS and LDFLAGS
******************

UWSGICONFIG_* for plugins
*************************

libuwsgi.so
***********

uwsgibuild.log
**************

uwsgibuild.lastcflags
*********************

cflags and uwsgi.h magic
************************

embedding files
***************

The fake make
*************
