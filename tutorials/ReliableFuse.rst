Reliably use Fuse filesystem for uWSGI vassals (with Linux)
===========================================================


Requirements: uWSGI 1.9.18, Linux kernel with fuse and namespaces support.

Fuse is a technology allowing the implementation of filesystems in user space.

There are hundreds of high quality available Fuse filesystems so having your application relying on them is a common situation.

Fuse filesystems are normal system processes, so as every processes in the system they can crash (or you can involuntary kill them).

In addition to this, if you host multiple applications, each one requiring a Fuse mountpoint, you may want to avoid polluting the main mounpoints namespace and, more important,
not having unused mounpoints in your system (ie an instance is completely removed and you do not want its fuse mountpoint to be still available in the system)

The purpose of this tutorial is configuring an Emperor and a series of vassal, each one mounting a Fuse filesystem.


A Zip filesystem
^^^^^^^^^^^^^^^^

fuse-zip (https://code.google.com/p/fuse-zip/) is a Fuse process exposing a zip file as a filesystem.

Our objective is storing our whole app in a zip archive and instruct uWSGI to mount it as a filesystem (via Fuse) under /app


The Emperor 
***********

.. code-block:: ini

   [uwsgi]
   emperor = /etc/uwsgi/vassals
   emperor-use-clone = fs,pid
   
The trick here is using Linux namespaces to create vassals in a new pid and filesystem namespace.

The first one (fs) allows mountpoint created by the vassal to be available only in the vassal (without messing with the main system), while the pid one
allows the uWSGI master to be the "init" process (pid 1) of the vassal. Being pid 1 means that when you die all of your children will die. In our scenario (where our vassal launch a Fuse process on startup) it means that when
the vassal is destroyed the Fuse process is destroyed too as well as its mountpoint.

A Vassal
********

.. code-block:: ini

   [uwsgi]
   uid = user001
   gid = user001
   
   ; mount fuse filesystem under /app (but only if it is not a reload)
   if-not-reload =
     exec-as-user = fuse-zip -r /var/www/app001.zip /app
   endif =
   
   http-socket = :9090
   psgi = /app/myapp.pl
   
here we use the -r option of the fuse-zip command for a read-only mount


Monitoring mountpoints
**********************

The problem with the current setup, is that if the fuse-zip process dies the instance will no more be able to access /app until it is respawned 

uWSGI 1.9.18 added the --mountpoint-check option. It forces the master to constantly verify the specified filesystem. If it fails the whole instance is bruttaly destroyed.

As we are under The Emperor, soon after the vassal is destroyed it will be restarted in a clean state (allowing the Fuse mountpoint to be started again)


.. code-block:: ini

   [uwsgi]
   uid = user001
   gid = user001
   
   ; mount fuse filesystem under /app (but only if it is not a reload)
   if-not-reload =
     exec-as-user = fuse-zip -r /var/www/app001.zip /app
   endif =
   
   http-socket = :9090
   psgi = /app/myapp.pl
   
   mountpoint-check = /app
