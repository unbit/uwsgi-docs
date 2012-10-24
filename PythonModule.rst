The uwsgi Python module
=======================

The uWSGI server automagically adds a ``uwsgi`` module into your Python apps.

This is useful for configuring the uWSGI server, use its internal functions and get statistics.

.. note:: Many of these functions are currently woefully undocumented.

Module-level globals
--------------------

.. default-domain:: py

.. module:: uwsgi

.. data:: numproc

   The number of processes/workers currently running.

.. data:: buffer_size 

   The current configured buffer size in bytes.

.. data:: started_on (int)

   The Unix timestamp of uWSGI's startup.

.. data:: fastfuncs

   This is the dictionary used to define :doc:`FastFuncs`.

.. data:: applist

   This is the list of applications currently configured.

.. TODO: Practical use cases for applist?

.. data:: applications

   This is the dynamic applications dictionary.

   .. seealso:: :ref:`PythonAppDict`

.. data:: message_manager_marshal

   The callable to run when the uWSGI server receives a marshalled message.

.. TODO: What _is_ this?


Cache functions
---------------

	
.. function:: cache_set()


.. function:: cache_update()


.. function:: cache_del()


.. function:: cache_exists()


.. function:: cache_clear()

Queue functions
---------------

.. function:: queue_get()


.. function:: queue_set()


.. function:: queue_last()


.. function:: queue_push()


.. function:: queue_pull()


.. function:: queue_pop()


.. function:: queue_slot()


.. function:: queue_pull_slot()


SNMP functions
--------------

.. function:: snmp_set_counter32()


.. function:: snmp_set_counter64()


.. function:: snmp_set_gauge()


.. function:: snmp_set_community()

Spooler functions
-----------------

.. function:: send_to_spooler()

   Send data to the :doc:`Spooler`.

.. function:: spool()


.. function:: set_spooler_frequency()


.. function:: spooler_jobs()


.. function:: spooler_pid()


Advanced methods
----------------

.. function:: send_message()

   Send a generic message using :doc:`Protocol`.

   .. note:: Until version `2f970ce58543278c851ff30e52758fd6d6e69fdc` this function was called ``send_uwsgi_message()``.


.. function:: route()


.. function:: send_multi_message()

   Send a generic message to multiple recipients using :doc:`Protocol`.

   .. note:: Until version `2f970ce58543278c851ff30e52758fd6d6e69fdc` this function was called ``send_multi_uwsgi_message()``.

   .. seealso:: :doc:`Clustering` for examples



.. function:: reload()

   Gracefully reload the uWSGI server stack.

   .. seealso:: :doc:`Reload`


.. function:: stop()


.. function:: workers() -> dict

   Get a statistics dictionary of all the workers for the current server. A dictionary is returned.


.. function:: masterpid() -> int

   Return the process identifier (PID) of the uWSGI master process.


.. function:: total_requests() -> int
 
   Returns the total number of requests managed so far by the pool of uWSGI workers.

.. function:: get_option()

   Also available as `getoption()`.

.. function:: set_option()

   Also available as `setoption()`.


.. function:: sorry_i_need_to_block()


.. function:: request_id()


.. function:: worker_id()


.. function:: mule_id()


.. function:: log()


.. function:: log_this_request()


.. function:: set_logvar()


.. function:: get_logvar()


.. function:: disconnect()


.. function:: grunt()


.. function:: lock()


.. function:: is_locked()


.. function:: unlock()


.. function:: cl()


.. function:: setprocname()


.. function:: listen_queue()


.. function:: register_signal()


.. function:: signal()


.. function:: signal_wait()


.. function:: signal_registered()


.. function:: signal_received()


.. function:: add_file_monitor()


.. function:: add_timer()


.. function:: add_probe()


.. function:: add_rb_timer()


.. function:: add_cron()



.. function:: register_rpc()


.. function:: rpc()


.. function:: rpc_list()


.. function:: call()


.. function:: sendfile()


.. function:: set_warning_message()


.. function:: mem()


.. function:: has_hook()


.. function:: logsize()


.. function:: send_multicast_message()


.. function:: cluster_nodes()


.. function:: cluster_node_name()


.. function:: cluster()


.. function:: cluster_best_node()


.. function:: connect()


.. function:: connection_fd()


.. function:: is_connected()


.. function:: send()


.. function:: recv()


.. function:: recv_block()


.. function:: recv_frame()


.. function:: close()


.. function:: i_am_the_spooler()


.. function:: fcgi()


.. function:: parsefile()


.. function:: embedded_data()


.. function:: extract()


.. function:: mule_msg()


.. function:: farm_msg()


.. function:: mule_get_msg()


.. function:: farm_get_msg()


.. function:: in_farm()


.. function:: ready()


.. function:: set_user_harakiri()


Async functions
---------------


.. function:: async_sleep()


.. function:: async_connect()


.. function:: async_send_message()


.. function:: green_schedule()


.. function:: suspend()


.. function:: wait_fd_read()


.. function:: wait_fd_write()


SharedArea functions
--------------------

.. seealso:: :doc:`SharedArea`

.. function:: sharedarea_read() -> string

   Read a byte string from the uWSGI :doc:`SharedArea`.


.. function:: sharedarea_write()

   Write a byte string into the uWSGI :doc:`SharedArea`.


.. function:: sharedarea_readbyte()

   Read a single byte from the uWSGI :doc:`SharedArea`.


.. function:: sharedarea_writebyte()

   Write a single byte into the uWSGI :doc:`SharedArea`.

.. function:: sharedarea_readlong()

   Read a 64-bit (8-byte) long from the uWSGI :doc:`SharedArea`.

.. function:: sharedarea_writelong()
   
   Write a 64-bit (8-byte) long into the uWSGI :doc:`SharedArea`.

.. function:: sharedarea_inclong()
   
   Atomically increment a 64-bit long value in the uWSGI :doc:`SharedArea`.
