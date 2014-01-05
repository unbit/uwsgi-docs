The uWSGI Spooler
=================

Updated to uWSGI 2.0.1

Supported on: Perl, Python, Ruby

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

Spool files
-----------

Spool files are serialized hash/dictionary of strings. The spooler will parse them and pass the resulting hash/dictionary to the spooler function (see below).

The serialization format is the same used for the 'uwsgi' protocol, so you are limited to 64k (even if there is a trick for passing bigger values, see the 'body' magic key below). The modifier1
for spooler packets is the 17, so a {'hello' => 'world'} hash will be encoded as:

========= ============== ==============
header    key1           value1
========= ============== ==============
17|14|0|0 |5|0|h|e|l|l|o |5|0|w|o|r|l|d
========= ============== ==============

A locking system allows you to safely manually remove spool files if something goes wrong, or to move them between spoolers directory.

Spool dirs over NFS are allowed, but if you do not have proper NFS locking in place, avoid mapping the same spooler NFS directory to spooler on different machines.

Setting the spooler function/callable
-------------------------------------

To have a fully operation spooler you need to define a "spooler function/callable".

Independently by the the number of configured spoolers, the same function will be executed. It is up to the developer
to instruct it to recognize tasks.

This function must returns an integer value:

-2 (SPOOL_OK) the task has been completed, the spool file will be removed

-1 (SPOOL_RETRY) something is temporarely wrong, the task will be retried at the next spooler iteration

0 (SPOOL_IGNORE) ignore this task, if multiple languages are loaded in the instance all of the will fight for magaing the task. This return values allows you to skip a task in specific languages.

any other value will be mapped as -1 (retry)


Each language plugin has its way to define the spooler function:

Perl:

.. code-block:: pl

   uwsgi::spooler(
       sub {
           my ($env) = @_;
           print $env->{foobar};
           # SPOOL_OK
           return -2;
       }
   );
   
Python:

.. code-block:: py

   import uwsgi
   
   def my_spooler(env):
       print env['foobar']
       # SPOOL_OK
       return uwsgi.SPOOL_OK
       
    uwsgi.spooler = my_spooler
    
Ruby:

.. code-block:: rb

   module UWSGI
        module_function
        def spooler(env)
                puts env.inspect
                return UWSGI::SPOOL_OK
        end
    end


Spooler function must be defined in the master process, so if you are in lazy-apps mode, be sure to place it in a file that is parsed
early in the server setup. (in python you can use --shared-import, in ruby --shared-require, in perl --perl-exec).

Some language plugin could have support for importing code directly in the spooler. Currently only python supports it with the --spooler-import option.


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
