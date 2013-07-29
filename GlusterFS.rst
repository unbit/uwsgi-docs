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
