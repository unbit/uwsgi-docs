Benchmarks for the PyPy plugin
==============================

.. note::

   this benchmark is now (november 2013) very outdated, most of the numbers here have changed (in better) with newer PyPy releases

This is mainly targeted at PyPy developers to spot slow paths or to fix corner-case bugs.

uWSGI stresses lot of areas of PyPy (most of them rarely used in pure-Python apps), so making these benchmarks is good both for uWSGI and PyPy.

* Results are rounded for ease of reading. Each test is executed 10 times on an 8-core Intel i7-3615QM CPU @ 2.30GHz.
* The CPython version is 2.7.5, PyPy is latest tip at 2013-05-23.
* Tests are run with logging disabled.
* Tests are run without thunder locking
* The client suite introduces ad-hoc errors and disconnections, so numbers are way lower that what you can get with 'ab' or 'httperf'

Generally the command lines are:

.. code-block:: sh

   uwsgi --http-socket :9090 --wsgi hello --disable-logging
   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-wsgi hello --disable-logging

Simple Hello World
^^^^^^^^^^^^^^^^^^

The most useless of the tests (as it shows only how uWSGI performs instead of the chosen Python engine).

.. code-block:: py

   def application(e, sr):
       sr('200 Ok', [('Content-Type', 'text/html')])
       return "ciao"

CPython: 6500 RPS, memory used 7MB (no leak detected)

Syscalls used:

.. code-block:: sh

   0.000403 gettimeofday({1369293059, 218207}, NULL) = 0
   0.000405 read(5, "GET / HTTP/1.1\r\nUser-Agent: curl/7.30.0\r\nHost: ubuntu64.local:9090\r\nAccept: */*\r\n\r\n", 4096) = 83
   0.000638 write(5, "HTTP/1.1 200 Ok\r\nContent-Type: text/html\r\n\r\n", 44) = 44
   0.000678 write(5, "ciao", 4)       = 4
   0.000528 gettimeofday({1369293059, 220477}, NULL) = 0
   0.000394 close(5)

PyPy: 6560 RPS, memory used 71MB (no leak detected)

Syscalls: No differences with CPython

Considerations:

* There is only slightly (read: irrelevant) better performance in PyPy.
* Memory usage is 10x higher with PyPy. 
  This is caused by the difference in the binary size (about 4 megs for libpython, about 50 for stripped libpypy-c).
  It is important to note that this 10x increase is only on startup, after the app is loaded memory allocations are really different.
  It looks like the PyPy team is working on reducing the binary size too.

CPU bound test (fibonacci)
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. code-block:: py

   def fib(n):
      if n == 0:
          return 0
      if n == 1:
          return 1
      return fib(n-1) + fib(n-2)

   def application(e, sr):
      sr('200 Ok', [('Content-Type', 'text/html')])
      fib(36)
      return "ciao"

This is where PyPy shines.

* CPython: time-to-complete 6400 milliseconds, memory used 65 MB
* PyPy: time-to-complete 900 milliseconds, memory used 71 MB

* The response time here is astonishing, there is no debate about how much better PyPy can be for CPU intensive (and/or highly recursive) tasks.
* More interesting is how the memory usage of PyPy remains the same of the simple hello world, while CPython's increased tenfold.
* Syscall usage is again the same.

Werkzeug testapp
^^^^^^^^^^^^^^^^

You may think this is not very different from the Hello World example, but this specific application does actually call lots of Python functions
and inspects the entire WSGI ``environ`` dictionary. This is very near to a standard application without I/O.

CPython: 600 RPS, memory usage 13MB

Syscalls:

.. code-block:: sh

   0.000363 gettimeofday({1369294531, 360307}, NULL) = 0
   0.000421 read(5, "GET / HTTP/1.1\r\nUser-Agent: curl/7.30.0\r\nHost: ubuntu64.local:9090\r\nAccept: */*\r\n\r\n", 4096) = 83
   0.002046 getcwd("/root/uwsgi", 1024) = 12
   0.000483 stat("/root/uwsgi/.", {st_mode=S_IFDIR|0755, st_size=12288, ...}) = 0
   0.000602 stat("/usr/local/lib/python2.7/dist-packages/greenlet-0.4.0-py2.7-linux-x86_64.egg", {st_mode=S_IFDIR|S_ISGID|0755, st_size=4096, ...}) = 0
   0.000530 stat("/usr/local/lib/python2.7/dist-packages/gevent-1.0dev-py2.7-linux-x86_64.egg", {st_mode=S_IFDIR|S_ISGID|0755, st_size=4096, ...}) = 0
   0.000506 stat("/usr/lib/python2.7", {st_mode=S_IFDIR|0755, st_size=28672, ...}) = 0
   0.000440 stat("/usr/lib/python2.7/plat-x86_64-linux-gnu", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000463 stat("/usr/lib/python2.7/lib-tk", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000624 stat("/usr/lib/python2.7/lib-old", 0x7fffb70da6a0) = -1 ENOENT (No such file or directory)
   0.000434 stat("/usr/lib/python2.7/lib-dynload", {st_mode=S_IFDIR|0755, st_size=12288, ...}) = 0
   0.000515 stat("/usr/local/lib/python2.7/dist-packages", {st_mode=S_IFDIR|S_ISGID|0775, st_size=4096, ...}) = 0
   0.000569 stat("/usr/lib/python2.7/dist-packages", {st_mode=S_IFDIR|0755, st_size=12288, ...}) = 0
   0.000387 stat("/usr/lib/python2.7/dist-packages/gtk-2.0", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000347 stat("/usr/lib/pymodules/python2.7", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000675 write(5, "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 7554\r\n\r\n", 81) = 81
   0.000575 write(5, "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\n  \"http://www.w3.org/TR/html4/loose.dtd\">\n<title>WSGI Information</title>\n<style type=\"text/css\">\n  @import url(http://fonts.googleapis.com/css?family=Ubuntu);\n\n  body       { font-family: 'Lucida Grande', 'Lucida Sans Unicode', 'Geneva',\n               'Verdana', sans-serif; background-color: white; color: #000;\n               font-size: 15px; text-align: center; }\n  #logo      { float: right; padding: 0 0 10px 10px; }\n  div.box    { text-align: left; width: 45em; margin: auto; padding: 50px 0;\n               background-color: white; }\n  h1, h2     { font-family: 'Ubuntu', 'Lucida Grande', 'Lucida Sans Unicode',\n               'Geneva', 'Verdana', sans-serif; font-weight: normal; }\n  h1         { margin: 0 0 30px 0; }\n  h2         { font-size: 1.4em; margin: 1em 0 0.5em 0; }\n  table      { width: 100%; border-collapse: collapse; border: 1px solid #AFC5C9 }\n  table th   { background-color: #AFC1C4; color: white; font-size: "..., 7554) = 7554
   0.000469 gettimeofday({1369294531, 370471}, NULL) = 0
   0.000391 close(5)                  = 0

PyPy: 1500 RPSs, memory usage 74MB

Syscalls:

.. code-block:: sh

   0.000397 gettimeofday({1369294713, 743204}, NULL) = 0
   0.000431 read(5, "GET / HTTP/1.1\r\nUser-Agent: curl/7.30.0\r\nHost: ubuntu64.local:9090\r\nAccept: */*\r\n\r\n", 4096) = 83
   0.003217 gettimeofday({1369294713, 746909}, NULL) = 0
   0.000660 gettimeofday({1369294713, 747509}, NULL) = 0
   0.000958 gettimeofday({1369294713, 748463}, NULL) = 0
   0.000359 gettimeofday({1369294713, 748832}, NULL) = 0
   0.000586 gettimeofday({1369294713, 749427}, NULL) = 0
   0.000660 gettimeofday({1369294713, 750077}, NULL) = 0
   0.000626 gettimeofday({1369294713, 750695}, NULL) = 0
   0.000318 gettimeofday({1369294713, 751010}, NULL) = 0
   0.000598 gettimeofday({1369294713, 751586}, NULL) = 0
   0.000782 gettimeofday({1369294713, 752391}, NULL) = 0
   0.000738 gettimeofday({1369294713, 753129}, NULL) = 0
   0.000355 gettimeofday({1369294713, 753483}, NULL) = 0
   0.000617 gettimeofday({1369294713, 754156}, NULL) = 0
   0.000502 gettimeofday({1369294713, 754649}, NULL) = 0
   0.000484 gettimeofday({1369294713, 755139}, NULL) = 0
   0.000513 gettimeofday({1369294713, 755674}, NULL) = 0
   0.001537 getcwd("/opt/uwsgi", 256) = 12
   0.000641 stat("/opt/uwsgi/.", {st_mode=S_IFDIR|0755, st_size=12288, ...}) = 0
   0.000668 stat("/opt/pypy/site-packages/setuptools-0.6c11-py2.7.egg", {st_mode=S_IFREG|0644, st_size=332005, ...}) = 0
   0.000766 stat("/opt/pypy/site-packages/pip-1.3.1-py2.7.egg", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000652 stat("/opt/pypy/lib_pypy/__extensions__", 0x7ff66a446030) = -1 ENOENT (No such file or directory)
   0.000570 stat("/opt/pypy/lib_pypy", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000688 stat("/opt/pypy/lib-python/2.7", {st_mode=S_IFDIR|0755, st_size=12288, ...}) = 0
   0.000592 stat("/opt/pypy/lib-python/2.7/lib-tk", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000534 stat("/opt/pypy/lib-python/2.7/plat-linux2", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000840 stat("/opt/pypy/site-packages", {st_mode=S_IFDIR|0755, st_size=4096, ...}) = 0
   0.000592 stat("/opt/uwsgi/.", {st_mode=S_IFDIR|0755, st_size=12288, ...}) = 0
   0.001014 write(5, "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\nContent-Length: 4915\r\n\r\n", 81) = 81
   0.000510 write(5, "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.01 Transitional//EN\"\n  \"http://www.w3.org/TR/html4/loose.dtd\">\n<title>WSGI Information</title>\n<style type=\"text/css\">\n  @import url(http://fonts.googleapis.com/css?family=Ubuntu);\n\n  body       { font-family: 'Lucida Grande', 'Lucida Sans Unicode', 'Geneva',\n               'Verdana', sans-serif; background-color: white; color: #000;\n               font-size: 15px; text-align: center; }\n  #logo      { float: right; padding: 0 0 10px 10px; }\n  div.box    { text-align: left; width: 45em; margin: auto; padding: 50px 0;\n               background-color: white; }\n  h1, h2     { font-family: 'Ubuntu', 'Lucida Grande', 'Lucida Sans Unicode',\n               'Geneva', 'Verdana', sans-serif; font-weight: normal; }\n  h1         { margin: 0 0 30px 0; }\n  h2         { font-size: 1.4em; margin: 1em 0 0.5em 0; }\n  table      { width: 100%; border-collapse: collapse; border: 1px solid #AFC5C9 }\n  table th   { background-color: #AFC1C4; color: white; font-size: "..., 4915) = 4915
   0.000729 gettimeofday({1369294713, 766079}, NULL) = 0
   0.000616 close(5)                  = 0

Considerations:

* This test stresses standard function calls. We have about 2.5x improvement with PyPy, while memory usage is pretty similar (considering the 62MB base difference).
* There is a syscall "problem" with PyPy, soon before starting the path checks it calls a blast of ``gettimeofday()`` syscalls. Without these, the RPS could increase a bit.

Werkzeug testapp with multithreading
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

It looks like Armin Rigo will soon be able to remove the GIL from PyPy. While he works on this, we can compare multithreading CPython and PyPy.

Multithreading for Python webapps is a good approach, the GIL is generally released during the blocking parts, so you can safely punch the face
of people ranting on the slowness of Python threads without knowing the context.

We spawn 8 threads (with Linux default stack size), and we stress test with a concurrency of 10.

* CPython: 200 RPSs, memory usage 14MB
* PyPy: 1100 RPSs, memory usage 88 MB

Here we have a problem. To avoid the possibility of a uWSGI threading bug we added a comparative test with ``mod_wsgi`` in embedded mode
(as uWSGI's threading model is based on ``mod_wsgi``). Results are the same (between 160 and 190 in apache2+mod_wsgi). So it looks like
multithreading in PyPy is way better.

We cannot, however, exclude other problems (testing threads is really hard).

Memory usage is a bit higher on PyPy (about 1.5 megs per thread compared to less than 200k in cpython)

Syscalls report will be hard to print, but the same blast of ``gettimeofday`` can be noted on PyPy, while lock contention
seems the same between uWSGI/mod_wsgi and PyPy.

RPC
^^^

uWSGI RPC is good for testing string manipulation. RPC parsing is done in C with the CPython plugin and in Python in PyPy.
RPC is called using the internal routing system (as the PyPy plugin does not export the :func:`uwsgi.rpc()` API function yet).

The option added to both command lines is:

.. code-block:: sh

   --route-run "rpc myfunc:one two threee four five six seven"
   
while the function is registered as:

.. code-block:: py

   import uwsgi

   def myfunc(*args):
       return '|'.join(reversed(args))

   uwsgi.register_rpc('myfunc', myfunc)
   

The results are pretty similar to the "hello world" one.

* CPython: 6400 RPSs, 8MB memory usage
* PyPy: 6500 RPSs, 71MB memory usage

PyPy has a small, "irrelevant" advantage in term of performance, but do remember its string parsing is done in pure Python.

RPC (multithread)
^^^^^^^^^^^^^^^^^

Here we have very interesting results:

* CPython: 6300 RPSs, 8MB memory usage
* PyPy: 6000 RPSs, 71MB memory usage

This time it is easy to understand what is going on. In PyPy the GIL is held 99% of the time in RPC mode (as message parsing is done in Python), while
the CPython version we have the GIL only for 10% of the whole request time.

Rewriting the RPC parsing in ``cffi`` will probably change the results to look more like the Werkzeug numbers. Something to look at in the future, unless Armin manages to remove the GIL.

Notes
^^^^^

* Testing multiprocessing is useless, do not ask for it.
* The uWSGI PyPy plugin still does not support all of the features of the CPython based plugin, we cannot exclude a little drop in performance while we add features.
* These numbers might look low to you if you have already made (or read) benchmarks. This is because the test tool injects bad requests in the stream to test server robustness.
* Again, this tests are only useful for the PyPy and uWSGI teams, do not base your choice between CPython and PyPy on them! (Your app's requirements will always be unique, and it's very possible that your app won't even run on PyPy even though it chugs along fine on CPython.)
