Running uWSGI in a Linux CGroup
===============================

Linux cgroups are an amazing feature available in recent Linux kernels. They allow you to "jail" your processes in constrained environments with limited CPU, memory, scheduling priority, IO, etc.

.. note:: uWSGI has to be run as root to use cgroups. ``uid`` and ``gid`` are very, very necessary.

Enabling cgroups
----------------

First of all you need to enable cgroup support in your system.

Create the :file:`/cgroup` directory and add this to your :file:`/etc/fstab`.

.. code-block:: sh

    none /cgroup cgroup cpu,cpuacct,memory

Then mount :file:`/cgroup`, and you'll have jails with controlled CPU and memory usage. There are other Cgroup subsystems, but CPU and memory usage are the most useful to constrain.

Let's run uWSGI in a cgroup:

.. code-block:: sh

    ./uwsgi -M -p 8 --cgroup /cgroup/jail001 -w simple_app -m --http :9090

Cgroups are simple directories -- now your uWSGI server and its workers are "jailed" in the :file:`cgroup/jail001` cgroup.

Make a bunch of requests to the server and you will see usage counters -- :file:`cpuacct.*` and :file:`memory.*` files in the cgroup directory growing.

You can also use pre-existing cgroups by specifying a directory that already exists.

A real world example: Scheduling QoS for your customers
-------------------------------------------------------

Suppose you're hosting apps for 4 customers.

Two of them are paying you $100 a month, one is paying $200, and the last, pulling out all the stops and bringing bread and butter to your table, is paying $400.

So to have a good Quality of Service implementation, the $100 apps should get 1/8, or 12.5% of your CPU power, the $200 app should get 1/4 (25%) and the last should get 50%. Right, let's implement this.

We have to create 4 cgroups, one for each app, and limit their scheduling weights.

.. code-block:: sh

    ./uwsgi --uid 1001 --gid 1001 -s /tmp/app1 -w app1 --cgroup /cgroup/app1 --cgroup-opt cpu.shares=1024
    ./uwsgi --uid 1002 --gid 1002 -s /tmp/app2 -w app1 --cgroup /cgroup/app2 --cgroup-opt cpu.shares=1024
    ./uwsgi --uid 1003 --gid 1003 -s /tmp/app3 -w app1 --cgroup /cgroup/app3 --cgroup-opt cpu.shares=2048
    ./uwsgi --uid 1004 --gid 1004 -s /tmp/app4 -w app1 --cgroup /cgroup/app4 --cgroup-opt cpu.shares=4096
    
    
The ``cpu.shares`` values are simply computed relative to each other, so you can use whatever scheme you like, such as (125, 125, 250, 500) or even (1, 1, 2, 4).

Right, so that's CPU usage limited. What about memory?

Let's use the same scheme as before, with a maximum of 2 GB for all apps altogether.    
    
.. code-block:: sh

    ./uwsgi --uid 1001 --gid 1001 -s /tmp/app1 -w app1 --cgroup /cgroup/app1 --cgroup-opt cpu.shares=125 --cgroup-opt memory.limit_in_bytes=268435456
    ./uwsgi --uid 1002 --gid 1002 -s /tmp/app2 -w app1 --cgroup /cgroup/app2 --cgroup-opt cpu.shares=125 --cgroup-opt memory.limit_in_bytes=268435456
    ./uwsgi --uid 1003 --gid 1003 -s /tmp/app3 -w app1 --cgroup /cgroup/app3 --cgroup-opt cpu.shares=250 --cgroup-opt memory.limit_in_bytes=536870912
    ./uwsgi --uid 1004 --gid 1004 -s /tmp/app4 -w app1 --cgroup /cgroup/app4 --cgroup-opt cpu.shares=500 --cgroup-opt memory.limit_in_bytes=1067459584
