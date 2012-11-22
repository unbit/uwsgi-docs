The uWSGI Spooler
=================



The Spooler is a queue manager built in to uWSGI that works like a printing/mail system. For example you can enqueue massive sending of emails, image processing, video encoding, etc. and let the spooler do the hard work in background while your users get their requests served by normal workers. Using the message passing feature of the uWSGI server you can even send your spool request to a remote uWSGI server.

You choose a directory (or directories) as a spool. uWSGI will then repeatedly look for files in this spool directory and use them as arguments for callables. After the callable returns, the file is removed.

To use the spooler you need to pass the ``-Q`` argument (``spooler`` option), followed by the directory you want to use as your spool scratch space.

.. code-block:: sh

    ./uwsgi -Q myspool -s /tmp/uwsgi.sock --buffer-size 8192 --wsgi testapp --sharedarea 10

If you think you'll be passing large messages, set a bigger buffer size using the ``buffer-size`` (``-b``) option.

Setting the spooler callable
----------------------------

Add a new function to your script:

.. code-block:: py

    def myspooler(env):
        print env
        for i in range(1,100):
                time.sleep(1)
        return uwsgi.SPOOL_OK
    
    uwsgi.spooler = myspooler
    
Using the uwsgi.spooler attribute you will set the callable to execute for every spool/queue/message file.

.. warning:: Using ``uwsgi.spooler`` is a low-level approach. Use the Python decorators or the Ruby DSL if you use those languages.

To enqueue a request (a dictionary of strings!) use :func:`uwsgi.send_to_spooler`:

.. code-block:: py

    uwsgi.send_to_spooler({'Name':'Serena', 'System':'Linux', 'Tizio':'Caio'})


How does the uWSGI server recognize a spooler request?
------------------------------------------------------

The queue/message/spool files are normally dictionaries that contain only strings encoded in the uwsgi protocol format. This also means that can use the uWSGI server to manage remote messaging.
Setting the uwsgi modifier 1 to ``UWSGI_MODIFIER_SPOOL_REQUEST`` (numeric value 17) you will inform the uWSGI server that the request is a spooling request. 
This is what ``uwsgi.send_to_spooler`` does in the background, but you can use your webserver support for uwsgi_modifiers for doing funny things like passing spooler message without using your wsgi apps resource but only the spooler.

An example of just this, using Nginx:

.. code-block:: nginx

     location /sendmassmail {
        uwsgi_pass 192.168.1.1:3031;
        uwsgi_modifier1 17;
        uwsgi_param ToGroup  customers;
     }

Supposing you have a callable that sends email to a group specified in the ``ToGroup`` dictionary key, this would allow you to enqueue mass mails using Nginx only.

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