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

.. code-block:: ini

   [uwsgi]
   ; every two hours
   cron = -1 -2 -1 -1 -1 /usr/bin/backup_my_home --recursive

Legion crons
************

When your instance is part of a :doc:`Legion`, you can configure it to run crons only if it is the Lord of the specified Legion:

.. code-block:: ini

   [uwsgi]
   legion = mycluster 225.1.1.1:1717 100 bf-cbc:hello
   legion-node = mycluster 225.1.1.1:1717
   ; every two hours
   legion-cron = mycluster -1 -2 -1 -1 -1 /usr/bin/backup_my_home --recursive

Unique crons
************

Available since 1.9.11
Some commands can take long time to finish or just hang, sometime it's fine, but there are also cases when running multiple instances of a command can be dangerous.
For such cases ``unique-cron`` and ``unique-legion-cron`` options were added, syntax is the same as with ``cron`` and ``legion-cron``, the difference is that uWSGI will delay next execution until previous was completed.

Example:

.. code-block:: ini

   [uwsgi]
   cron = -1 -1 -1 -1 -1 sleep 70

Would execute ``sleep 70`` every minute, since sleep command will be running longer than our execution interval, we will end up with growing number of sleep processes.
To fix this we can simply replace ``cron`` with ``unique-cron`` and uWSGI will make sure that only single sleep process is running, new process will be started right after previous had finished.

Harakiri
********

Available since 1.9.11
Using ``--cron-harakiri`` will enforce time limit on executed commands, if any command is taking longer it will be killed.

.. code-block:: ini

   [uwsgi]

   cron = sleep 30
   cron-harakiri = 10

Will kill cron command after 10 seconds. Note that ``cron-harakiri`` is a global limit, it affects all cron commands, to set per command time limit use ``cron2`` option (see below).

New syntax for cron options
***************************

Available since 1.9.11
To allow better control over crons new option was added in uWSGI, syntax:

.. code-block:: ini

   [uwsgi]
   cron2 = option1=value,option2=value command to execute

Example:

.. code-block:: ini

   [uwsgi]

   cron2 = minute=-2,unique=1 sleep 130

Will spawn unique cron command ``sleep 130`` every 2 minutes.

Option list is optional, available options for every cron:

**minute** - minute part of crontab entry, default is -1 (interpreted as *)

**hour** - hour part of crontab entry, default is -1 (interpreted as *)

**day** - day part of crontab entry, default is -1 (interpreted as *)

**month** - month part of crontab entry, default is -1 (interpreted as *)

**week** - week part of crontab entry, default is -1 (interpreted as *)

**unique** - marks cron command as unique (see above), default is 0 (not unique)

**harakiri** - set harakiri timeout (in seconds) for this cron command, default is 0 (no harakiri)

**legion** - set legion name for use with this cron command, cron legions are only executed on the legion lord node.

Note that you cannot use spaces in options list (``minute=1, hour=2`` will not work, but ``minute=1,hour=2`` will work just fine).
If any option is missing default value is used, examples:

.. code-block:: ini

   [uwsgi]
   cron2 = my command

Will execute ``my command`` every minute (-1 -1 -1 -1 -1 crontab).

.. code-block:: ini

   [uwsgi]
   cron2 = minute=30,hour=5,unique=1 /usr/local/bin/backup.sh

Will execute unique command ``/usr/local/bin/backup.sh`` at 5:30 every day.

.. code-block:: ini

   [uwsgi]
   legion = mycluster 225.1.1.1:1717 100 bf-cbc:hello
   legion-node = mycluster 225.1.1.1:1717
   cron2 = minute=-10,legion=mycluster my command

Will execute ``my command`` every 10 minutes on ``mycluster`` legion lord node.

.. code-block:: ini

   [uwsgi]
   cron-harakiri = 10
   cron2 = harakiri=0 my command
   cron2 = my second command

Will disable harakiri for ``my command``, but other cron commands will still be killed after 10 seconds.
