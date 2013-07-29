The GlusterFS plugin
====================

Available from uWSGI 1.9.15

official modifier1: 27

The 'glusterfs' plugin allows you to serve files stored in glusterfs filesystems directly using the glusterfs api
available starting from GlusterFS 3.4

This approach (compared to serving via fuse or nfs) has various advantages in terms of performances and ease of deployment.


Step1: glusterfs installation
=============================

we build glusterfs from official sources, installing it in /opt/glusterfs on 3 nodes (192.168.173.1, 192.168.173.2, 192.168.173.3).

.. code-block:: sh

   ./configure --prefix=/opt/glusterfs
   make
   make install
   
now start the configuration/control daemon with:

.. code-block:: sh

   /opt/glusterfs/sbin/glusterd
   
from now on we can start configuring our cluster

Step2: the first cluster
========================

run the control client to access the glusterfs shell:

.. code-block:: sh

   /opt/glusterfs/sbin/gluster
   
the first step is "discovering" the other nodes:

.. code-block:: sh

   # do not run on node1 !!!
   peer probe 192.168.173.1
   # do not run on node2 !!!
   peer probe 192.168.173.2
   # do not run on node3 !!!
   peer probe 192.168.173.3

remember, you do not need to run "peer probe" for the same address of the machine on which you are running
the glusterfs console. You have to repeat the procedure on each node of the cluser.

Now we can create a replica volume (/exports/brick001 dir has to exist in every node):

.. code-block:: sh

   volume create unbit001 replica 3 192.168.173.1:/exports/brick001 192.168.173.2:/exports/brick001 192.168.173.3:/exports/brick001
   
and start it:

.. code-block:: sh

   volume start unbit001
   
Now you should be able to mount your glusterfs filesystem and start writing files in it (you can use nfs or fuse)
