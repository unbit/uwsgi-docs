The RADOS plugin
====================

Available from uWSGI 1.9.16

official modifier1: 28

Author: Javier Guerra

The 'rados' plugin allows you to serve objects stored in a Ceph cluster directly using the librados API.

Note that it's not the CephFS filesystem, nor the 'radosgw' S3/Swift-compatible layer; RADOS is the bare object-storage layer.


Step1: Ceph cluster and content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you want to try a minimal Ceph instalation, you can follow this guide: http://ceph.com/docs/master/start/. note that
you only need the OSD and MON daemons, the MDS are needed only for CephFS filesystems.

Once you get it running, you should have a configuration file (by default on /etc/ceph/ceph.con), and should be able to use the `rados` utility.

.. code-block:: sh

   rados lspools

by default, you should have at least the 'data', 'metadata' and 'rbd' pools.  Now add some content to the 'data' pool.
For example, if you have a 'list.html' file and images 'first.jpeg', 'second.jpeg' on a subdirectory 'imgs/':

.. code-block:: sh

   rados -p data put list.html list.html
   rados -p data put imgs/first.jpeg imgs/first.jpeg
   rados -p data put imgs/second.jpeg imgs/second.jpeg
   rados -p data ls -

note that RADOS doesn't have a concept of directories, but the object names can contain a slash.


Step2: uWSGI
^^^^^^^^^^^^

A build profile, named 'rados' is already available, so you can simply do:

.. code-block:: sh

   python uwsgiconfig.py --build rados


You can now start your HTTP to serve RADOS objects:

.. code-block:: ini

   [uwsgi]
   ; bind on port 9090
   http-socket = :9090
   ; set the default modifier1 to the rados one
   http-socket-modifier1 = 28
   ; mount our rados pool
   rados-mount = mountpoint=/rad/,pool=data,config=/etc/ceph/ceph.conf
   ; spawn 30 threads
   threads = 30

the 'rados-mount' parameter takes three subparameters:

 - mountpoint: required, the URL prefix on which the RADOS objects will appear.
 - pool: required, the RADOS pool to serve.
 - config: optional, the path to the ceph config file.

in this example, your content will be served at http://localhost:9090/rad/list.html, http://localhost:9090/rad/imgs/first.jpeg
and http://localhost:9090/rad/imgs/second.jpeg.


High availability
^^^^^^^^^^^^^^^^^

The RADOS storage system is fully distributed, just starting several uWSGI workers on several machines with the same
'ceph.conf', all will see the same pools.  If they all serve on the same mountpoint, you get a failure-resistant
RADOS-HTTP gateway.


Multiple mountpoints
^^^^^^^^^^^^^^^^^^^^

You can issue several 'rados-mount' entries, each one will define a new mountpoint.  This way you can expose different
RADOS pools at different URLs.


Notes:
^^^^^^

The plugin automatically enables the mime type engine.

There is no directory index support

Async support is on work
