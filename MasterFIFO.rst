The Master FIFO
===============

Available from uWSGI 1.9.17

You can tell the master to create a UNIX named pipe (fifo) you can use to issue commands to the master.

Generally you use UNIX signals to manage the master, but we are run out of signals numbers and (more important) not needing to mess with pids
simplify the implementation of external management scripts.

To create the fifo just add `--master-fifo <filename>` then start issuing commands to it:

.. code-block:: sh

   echo r > /tmp/yourfifo

Available commands
******************

* 'c' trigger chain reload
* 'f' re-fork the master (dangerous, but very powerful)
* 'l' reopen log file (need --log-master and --logto/--logto2)
* 'L' trigger log rotation (need --log-master and --logto/--logto2)
* 'p' pause/resume the instance
* 'q' gracefully shutdown the instance
* 'Q' brutally shutdown the instance
* 'r' send graceful reload
* 'R' send brutal reload
* 's' print stats in the logs
* 'w' gracefully reload workers

Notes
*****

The FIFO is created in non-blocking modes and recreated by the master every time a client disconnects.

You can override (or add) commands using the global array uwsgi_fifo_table via plugins or c hooks
