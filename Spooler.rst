The uWSGI Spooler
=================

Updated to uWSGI 2.0.1

The Spooler is a queue manager built into uWSGI that works like a printing/mail system. 

You can enqueue massive sending of emails, image processing, video encoding, etc. and let the spooler do the hard work in background while your users get their requests served by normal workers.

A spooler works by defining a directory in which "spool files" will be written, every time the spooler find a file in its directory it will parse it and will run a specific function.

You can have multiple spoolers mapped to different directories and even multiple spoolers mapped to the same one.

The ``--spooler <directory>`` option allows you to generate a spooler process, while the ``--spooler-processes <n>`` allows you to set how many processes to spawn for every spooler.

The spooler is able to manage uWSGI signals too, so you can use it as a target for your handlers.

This configuration will generate a spooler for your instance (myspool directory must exists)

.. code-block:: ini

   [uwsgi]
   spooler = myspool
   ...
   
while this one will create two spoolers:

.. code-block:: ini

   [uwsgi]
   spooler = myspool
   spooler = myspool2
   ...

having multiple spoolers allows you to prioritize tasks (and eventually parallelize them)

Setting the spooler function/callable
-------------------------------------

Enqueing requests to a spooler
------------------------------

External spoolers
-----------------

Networked spoolers
------------------


Post-poning tasks
-----------------

The 'body' magic key
--------------------

Priorities
----------

Options
-------
spooler=directory 
run a spooler on the specified directory

spooler-external=directory
map spoolers requests to a spooler directory managed by an external instance

spooler-ordered
try to order the execution of spooler tasks (uses scandir instead of readdir)

spooler-chdir=directory
call chdir() to specified directory before each spooler task

spooler-processes=##
set the number of processes for spoolers

spooler-quiet
do not be verbose with spooler tasks

spooler-max-tasks=##
set the maximum number of tasks to run before recycling a spooler (to help alleviate memory leaks)

spooler-harakiri=##
set harakiri timeout for spooler tasks, see [harakiri] for more information.

Tips and tricks
---------------

You can re-enqueue a spooler request by returning ``uwsgi.SPOOL_RETRY`` in your callable:

.. code-block:: py

    def call_me_again_and_again(env):
        return uwsgi.SPOOL_RETRY
    
You can set the spooler poll frequency using :py:func:`uwsgi.set_spooler_frequency`, where N is the number of seconds to sleep before redoing a spooler scan.

You can use this to build a cron-like system.

.. code-block:: py

    # run function every 22 secs
    s_freq = 22
    
    def emu_cron(env):
        # run your function
        long_func("Hello World")
        # and re-enqueue it
        return uwsgi.SPOOL_RETRY
    
    uwsgi.set_spooler_frequency(s_freq)
    uwsgi.spooler = emu_cron
    # start the emu_cron
    uwsgi.send_to_spooler({'Name':'Alessandro'})

* You can also schedule spool a task to be specified only after a specific UNIX timestamp has passed by specifying the 'at' argument.
  
  .. code-block:: py
  
      import time, uwsgi
      
      # uwsgi.spool is a synonym of uwsgi.send_to_spooler
      uwsgi.spool(foo='bar',at=time.time()+60) # Let's do something in a minute, okay?

* You can attach a binary ``body`` larger than the dictionary size limit with the ``body`` parameter. (Remember that it will be loaded into memory in the spooler though.)

  .. code-block:: py

     uwsgi.spool({"body": my_pdf_data})

* You could use the :doc:`Caching <caching framework>` as shared memory to send progress data, etc. back to your application.
