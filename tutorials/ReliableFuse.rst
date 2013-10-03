Reliably use Fuse filesystem for uWSGI vassals (with Linux)
===========================================================


Requirements: uWSGI 1.9.18, Linux kernel with fuse support.

Fuse is a technology allowing the implementation of filesystems in user space.

There are hundreds of high quality available Fuse filesystems so having your application relying on them is a common situation.

Fuse filesystems are normal system processes, so as every processes in the system they can crash (or you can involuntary kill them).

In addition to this, if you host multiple applications, each one requiring a Fuse mountpoint, you may want to avoid polluting the main mounpoints namespace and, more important,
not having unused mounpoints in your system (ie an instance is completely removed and you do not want its fuse mountpoint to be still available in the system)

The purpose of this tutorial is configuring an Emperor and a series of vassal, each one mounting a Fuse filesystem.


A Zip filesystem
****************

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
allows the uWSGI master to be the "init" process (pid 1) of the vassal. Being pid 1 means that wehn you die all of your children will die. In our scenario (where our vassal launch a Fuse process on startup) it means that when
the vassal is destroyed the Fuse process is destroyed to as well as its mountpoint.

A Vassal
********


Monitoring mountpoints
**********************
