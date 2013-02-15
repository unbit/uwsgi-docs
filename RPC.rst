uWSGI RPC Stack
===============

uWSGI includes an embedded RPC stack that abstracts away having to use the lower level functions of uWSGI's API to do RPC.

What's really neat about uWSGI's RPC is that it allows you to call functions even between separate nodes and languages.

.. note:: RPC functions receive arguments in the form of binary strings, so every RPC exportable function must assume that each argument is a string. Every RPC function returns a string of 0 or more characters.

Learning by example
-------------------

Let's start with a simple RPC call from ``10.0.0.1:3031`` to ``10.0.0.2:3031``.

So let's export a "hello" function on ``.2``.

.. code-block:: py

    import uwsgi
    
    def hello_world():
        return "Hello World"
    
    uwsgi.register_rpc("hello", hello_world)

This uses :py:meth:`uwsgi.register_rpc` to declare a function called "hello" to be exported. We'll start the server with ``--server :3031``.

On the caller's side, on ``10.0.0.1``, let's declare the world's (second) simplest WSGI app.

.. code-block:: py

    import uwsgi
    
    def application(env, start_response):
        start_response('200 Ok', [('Content-Type', 'text/html')]
        return uwsgi.rpc('10.0.0.2:3031', 'hello')

That's it!

If you are a member of an uWSGI cluster, you can use :meth:`uwsgi.cluster_best_node` to distribute RPC load (more) evenly.

.. code-block:: py

    import uwsgi
    
    def application(env, start_response):
        start_response('200 Ok', [('Content-Type', 'text/html')]
        return uwsgi.rpc(uwsgi.cluster_best_node(), 'hello')

What about, let's say, Lua? 
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Glad you asked. If you want to export functions in Lua, simply do:

.. code-block:: lua

    function hello_with_args(arg1, arg2)
        return 'args are '..arg1..' '..arg2
    end
    
    uwsgi.register_rpc('hellolua', hello_with_args)

And in your Python WSGI app:

.. code-block:: py

    import uwsgi
    
    def application(env, start_response):
        start_response('200 Ok', [('Content-Type', 'text/html')]
        return uwsgi.rpc('10.0.0.2:3031', 'hellolua', 'foo', 'bar')


Doing RPC locally
-----------------

Doing RPC locally may sound a little silly, but if you need to call a Lua function from Python with the absolute least possible overhead, uWSGI RPC is your man.

If you want to call a RPC defined in the same server (governed by the same master, etc.), simply set the first parameter of :py:meth:`uwsgi.rpc`` to None or nil, or use the convenience function :py:meth:`uwsgi.call`.


Doing RPC from nginx
--------------------

As Nginx supports low-level manipulation of the uwsgi packets sent to upstream uWSGI servers, you can do RPC directly through it. Madness!

.. code-block:: nginx

    location /call {
        uwsgi_modifier1 173;
        uwsgi_modifier2 1;
        
        uwsgi_param hellolua foo
        uwsgi_param bar ""
    
        uwsgi_pass 10.0.0.2:3031;
    
        uwsgi_pass_request_headers off;
        uwsgi_pass_request_body off;
    }

Zero size strings will be ignored by the uWSGI array parser, so you can safely use them when the numbers of parameters + function_name is not even. 

Modifier2 is set to 1 to inform that raw strings (HTTP responses in this case) are received. Otherwise the RPC subsystem would encapsulate the output in an uwsgi protocol packet, and nginx isn't smart enough to read those.
