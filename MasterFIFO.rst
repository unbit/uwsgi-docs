The Master FIFO
===============

Available from uWSGI 1.9.17

You can tell the master to create a UNIX named pipe (fifo) you can use to issue commands to the master.

Generally you use UNIX signals to manage the master, but we are run out of signals numbers and (more important) not needing to mess with pids
simplify the implementation of external management scripts.

To create the fifo just add ``--master-fifo <filename>`` then start issuing commands to it:

.. code-block:: sh

   echo r > /tmp/yourfifo
   
you can send multiple commands in one shot:

.. code-block:: sh

   echo +++s > /tmp/yourfifo
   
will add 3 workers and will print stats

Available commands
******************

* '0' to '9' set the fifo slot (see below)
* '-' decrease the number of workers when in cheaper mode (add ``--cheaper-algo manual`` for full control)
* '+' increase the number of workers when in cheaper mode (add ``--cheaper-algo manual`` for full control)
* 'c' trigger chain reload
* 'C' set cheap mode
* 'E' trigger an Emperor rescan
* 'f' re-fork the master (dangerous, but very powerful)
* 'l' reopen log file (need --log-master and --logto/--logto2)
* 'L' trigger log rotation (need --log-master and --logto/--logto2)
* 'p' pause/resume the instance
* 'P' update pidfiles (can be useful after master re-fork)
* 'q' gracefully shutdown the instance
* 'Q' brutally shutdown the instance
* 'r' send graceful reload
* 'R' send brutal reload
* 's' print stats in the logs
* 'S' block/unblock subscriptions
* 'w' gracefully reload workers
* 'W' brutally reload workers

FIFO slots
**********

uWSGI supports up to 10 different fifo files. By default the first specified is bound (mapped as '0').

During the whole instance lifetime you can change from one fifo file to another simply sending the number of the fifo slot to use:

.. code-block:: ini

   [uwsgi]
   master-fifo = /tmp/fifo0
   master-fifo = /tmp/fifo1
   master-fifo = /var/run/foofifo
   processes = 2
   ...

By default /tmp/fifo0 will be allocated, but after sending:

.. code-block:: sh

   echo 1 > /tmp/fifo0
   
the /tmp/fifo1 file will be bound

This is very useful to map fifo files to specific instance when you abuse the 'fork the master' command (the 'f' one):

.. code-block:: sh

   echo 1fp > /tmp/fifo0
   
after sending this command, a new uwsgi instance (inheriting all of the bound sockets) will be spawned, the old one will be put in "paused" mode (p command).

As we have sent the '1' command before 'f' and 'p' the old instance will now accepts commands on /tmp/fifo1 (the slot 1) will the new one will use the default one (the '0')

There are lot of tricks you can accomplish, and lot of way to abuse the forking of the master. Just take in account that corner-case problems
can raise all over the place, expecially if you use the most complex features of uWSGI.

Notes
*****

The FIFO is created in non-blocking modes and recreated by the master every time a client disconnects.

You can override (or add) commands using the global array uwsgi_fifo_table via plugins or c hooks

Only the uid running the master has write access to the fifo
