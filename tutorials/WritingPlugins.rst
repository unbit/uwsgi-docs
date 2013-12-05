Writing uWSGI plugins
=====================

This tutorial will introduce you to uWSGI hacking. A bit of C knowledge and UNIX theory is required.

The simplified (and safe) build system used in the tutorial has been added in uWSGI 1.9.21, on older versions you need the raw
procedure (described at the end of the tutorial)

What a "uWSGI plugin" is ?
**************************

a uWSGI plugins is a standard shared library (with the classic .so extension) exposing a specific C structure named "uwsgi_plugin".

This structure exposes a bunch of handy informations (like the name of the plugin) and "hooks".

Hooks are simple functions registered to be run at specific server phases

The minimal plugin you can write it is something like that (the 'foobar' plugin)

.. code-block:: c

   #include <uwsgi.h>
   
   struct uwsgi_plugin foobar_plugin = {
           .name ="foobar",
   };
   
it announces itself as 'foobar' and exposes no hooks (yes, it is the most useless plugin out there).

Plugins are not required to define hooks, they can simply expose functions that can be called using uWSGI advanced facilities (read: :doc:`Hooks`)

Why (and when) plugins ?
************************

Albeit uWSGI is able to directly load

The first plugin
****************

The uwsgiplugin.py file
***********************


