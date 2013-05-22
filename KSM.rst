Using Linux KSM in uWSGI
========================

Kernel Samepage Merging <http://www.linux-kvm.org/page/KSM> is a feature of
Linux kernels >= 2.6.32 which allows processes to share pages of memory with
the same content.  This is accomplished by a kernel task that scans specific
memory areas and compares periodically, and when possible, merges them.  Born
as an enhancement for KVM it can be used for processes using common data such
as uWSGI processes with language interpreters and standard libraries.

If you are lucky, using KSM could exponentially reduce the memory usage of your
uWSGI instances. Especially in massive :doc:`Emperor<Emperor>` deployments
enabling KSM in each vassal may result in massive memory savings.
KSM in uWSGI was the idea of Giacomo Bagnoli of Asidev s.r.l.
http://www.asidev.com/en/company.html .Many thanks to him.


Enabling the KSM daemon
-----------------------

To enable the KSM kernel daemon, simply set ``/sys/kernel/mm/ksm/run`` to 1,
like so:

.. code-block:: sh

    echo 1 > /sys/kernel/mm/ksm/run

.. note:: Remember to do this on machine startup, as the KSM daemon does not run by default.

.. note:: Note that KSM is an opt-in feature that has to be explicitly requested by processes, so just enabling KSM will not be a savior for everything on your machine.

Enabling KSM support in uWSGI
-----------------------------

If you have compiled uWSGI on a kernel with KSM support, you will be able to
use the ``ksm`` option.  This option will instruct uWSGI to register process
memory mappings to the KSM daemon after each request or master cycle.  If no
page mapping has changed from the last scan, no expensive syscalls are used.
(Each mapping requires a ``madvise`` call.)

Performance impact
------------------

Checking for process mappings requires parsing the /proc/self/maps file after
each request.  In some setups this may hurt performance. You can tune the
frequency of the uWSGI page scanner by passing an argument to the ``ksm``
option.

.. code-block:: sh

    # Scan for process mappings every 10 requests (or 10 master cycles)
    ./uwsgi -s :3031 -M -p 8 -w myapp --ksm=10


Check if KSM is working well
----------------------------

The /sys/kernel/mm/ksm/pages_shared and /sys/kernel/mm/ksm/pages_sharing files
contain statistics regarding KSM's efficiency.  Higher values means lesser
memory consumption for your uWSGI instances.


KSM statistics using collectd
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A simple bash script like this is useful for keeping an eye on KSM's efficiency.

.. code-block:: sh

    #!/bin/bash
    
    export LC_ALL=C
    
    if [ -e /sys/kernel/mm/ksm/pages_sharing ]; then
        pages_sharing=`cat /sys/kernel/mm/ksm/pages_sharing`;
        page_size=`getconf PAGESIZE`;
        saved=$(echo "scale=0;$pages_sharing * $page_size"|bc);
        echo "PUTVAL <%= cn %>/ksm/gauge-saved interval=60 N:$saved"
    fi

In your collectd configuration, add something like this.

.. code-block:: ini

    LoadPlugin exec
    <Plugin exec>
       Exec "nobody" "/usr/local/bin/ksm_stats.sh"
    </Plugin>
