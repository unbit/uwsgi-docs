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

A Vassal
********


Monitoring mountpoints
**********************
