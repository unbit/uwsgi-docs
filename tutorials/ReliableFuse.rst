Reliably use Fuse filesystems for uWSGI vassals (with Linux)
============================================================


Requirements: uWSGI 1.9.18, Linux kernel with fuse and namespaces support.

Fuse is a technology allowing the implementation of filesystems in user space.

There are hundreds of high quality available Fuse filesystems, so having your application relying on them is a common situation.

Fuse filesystems are normal system processes, so as every process in the system they can crash (or you can involuntary kill them).

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

uWSGI 1.9.18 added the --mountpoint-check option. It forces the master to constantly verify the specified filesystem. If it fails the whole instance will be brutally destroyed.

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
   
   
Going Heavy Metal: A CoW rootfs (unionfs-fuse)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

unionfs-fuse (http://podgorny.cz/moin/UnionFsFuse) is a user space implementation of a union filesystem.

A union filesystem is a stack of multiple filesystem, so directory with same name are merged in a single view.

Union filesystems are more than this and one of the most useful features is copy on write.

Enabling copy on writes means you will have an immutable/read-only mountpoint base and all of the modifications to it will go in another mountpoint.

Our objective is having a readonly rootfs shared by all of our customers, and a writable mountpoint (configured as cow) for each customer, in which every modification will be stored.

The Emperor
***********

There is no modification in the Emperor, the previous configuration can be used.

What we need to do is prepare our filesystems.

The layout will be:

.. code-block:: c

   /ufs (where we initially mount our unionfs for each vassal)
   /ns
     /ns/precise (the shared rootfs)
     /ns/lucid (an alternative rootfs for old-fashioned customers)
     /ns/saucy (another shared rootfs based on ubuntu saucy)
     
     /ns/cow (the customers writable areas)
       /ns/cow/user001
       /ns/cow/user002
       /ns/cow/userXXX
       ...
       
we create our rootfs:

.. code-block:: sh

   debootstrap precise /ns/precise
   debootstrap lucid /ns/lucid
   debootstrap saucy /ns/saucy
   
and we create the .old_root directory in each one (it is required for pivot_root , see below)

.. code-block:: sh

   mkdir /ns/precise/.old_root
   mkdir /ns/lucid/.old_root
   mkdir /ns/saucy/.old_root
   
   
be sure to install the required libraries in each of them (expecially the libraries required for your language).

The uwsgi binary must be able to be executed in this rootfs, so you have to invest a bit of time in it (a good approach is having a language plugin
compiled for each distribution and placed on a common directory, for example each rootfs could have an /opt/uwsgi/plugins/psgi_plugin.so file and so on)

A Vassal
********

Here things get a bit more complicated. We need to launch the unionfs process (as root as it must be our new rootfs) and then call pivot_root (a more advanced chroot available on Linux)

:doc:`Hooks` are the best way to run custom commands (or function) in the various uWSGI startup phases.

In our example we will run Fuse processes in the "pre-jail" phase, and deal with mountpoints in the "as-root" phase (that happens after pivot_root)

.. code-block:: ini

   [uwsgi]
   ; choose the approach that best suit for you here (plugins loading)
   ; this will be used for the first run ...
   plugins-dir = /ns/precise/opt/uwsgi/plugins
   ; and this after a reload (where our rootfs is already /ns/precise)
   plugins-dir = /opt/uwsgi/plugins
   plugin = psgi
   
   ; drop privileges
   uid = user001
   gid = user001
   
   ; chdir to / for avoiding problems after pivot_root
   hook-pre-jail = callret:chdir /
   ; run unionfs-fuse using chroot (it is required for avoiding deadlocks) and cow (we mount it under /ufs)
   hook-pre-jail = exec:unionfs-fuse -ocow,chroot=/ns,default_permissions,allow_other /precise=RO:/cow/%(uid)=RW /ufs

   ; change the rootfs to the unionfs one
   ; the .old_root directory is where the old rootfs is still available
   pivot_root = /ufs /ufs/.old_root
   
   ; now we are in the new rootfs and in 'as-root' phase
   ; remount the /proc filesystem
   hook-as-root = mount:proc none /proc
   ; bind mount the original /dev in the new rootfs (simplify things a lot)
   hook-as-root = mount:none /.old_root/dev /dev bind
   ; recursively un-mount the old rootfs
   hook-as-root = umount:/.old_root rec,detach
   
   ; common bind
   http-socket = :9090
   
   ; load the app (fix it with your requirements)
   psgi = /var/www/myapp.pl
   
   ; constantly check for the rootfs (seems odd but is is very useful)
   mountpoint-check = /
   
If your app tries to make some write to its filesystem, you will see all of the created/updated files to be available in its /cow directory.

