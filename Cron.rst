The uWSGI cron-like interface
=============================

uWSGI's :term:`master` has an internal cron-like facility that can generate events at predefined times.

You can use it

* via the uWSGI API, in which case cron events will generate uWSGI signals
* directly via options, in which case events will run shell commands

uWSGI signal based
------------------

The :meth:`uwsgi.add_cron` function is the interface to the uWSGI signal cron facility.

The syntax is 

.. code-block:: py

    uwsgi.add_cron(signal, minute, hour, day, month, weekday)

The last 5 arguments work similarly to a standard crontab, but instead of "*", use -1, and instead of "*/2", "*/3", etc. use -2 and -3, etc.

.. code-block:: py

    import uwsgi
    
    def five_o_clock_on_the_first_day_of_the_month(signum):
        print "It's 5 o'clock of the first day of the month."
    
    uwsgi.register_signal(99, "", five_o_clock_on_the_first_day_of_the_month)
    uwsgi.add_cron(99, 0, 5, 1, -1, -1)


Timers vs. cron
---------------

As usual, you should choose the right tool for the job.

Recurring events not related to specific dates should use timers/rb_timers, and when you are interested in a specific date/hour use cron.

For example,

.. code-block:: py

    uwsgi.add_cron(99, -1, -1, -1, -1, -1) # ugly, bad and inefficient way to run signal 99 every minute :(
    uwsgi.add_timer(99, 60) # much better.

Notes
-----

* ``day`` and ``weekday`` are ORed as the original crontab specifications.
* By default, you can define up to 64 signal-based cron jobs per master. This value may be increased in :file:`uwsgi.h`.

Option-based cron
-----------------

You can define cron tasks directly in configuration with the ``cron`` option.

You can specify an unlimited number of option-based cron records. The syntax is the same of the signal-based ones.

For example,

.. code-block:: ini

    [uwsgi]
    cron = 59 2 -1 -1 -1 /usr/bin/backup_my_home --recursive
    cron = 9 11 -1 -1 2 /opt/dem/bin/send_reminders

.. code-block:: xml

    <uwsgi>
        <cron>59 2 -1 -1 -1 /usr/bin/backup_my_home --recursive</cron>
        <cron>9 11 -1 -1 2 /opt/dem/bin/send_reminders</cron>
    </uwsgi>

..code-block:: ini

   [uwsgi]
   ; every two hours
   cron = -1 /2 -1 -1 -1 /usr/bin/backup_my_home --recursive

Legion crons
************

When your instance is part of a Legion, you can configure it to run crons only if it is the Lord of the specified Legion:

..code-block:: ini

   [uwsgi]
   legion = mycluster 225.1.1.1:1717 100 bf-cbc:hello
   legion-node = mycluster 225.1.1.1:1717
   ; every two hours
   legion-cron = mycluster -1 /2 -1 -1 -1 /usr/bin/backup_my_home --recursive

