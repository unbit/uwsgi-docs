Benchmarks for the PyPy plugin
==============================

This is mainly targeted at PyPy developers to spot slow paths or to fix corner-case bug.

uWSGI stresses lot of areas of PyPy (most of them rarely abused in pure-python apps), so making benchmarks is good both for uWSGI and PyPy

Results are rounded for easy of read, each test is executed 10 times on a Intel i7-3615QM CPU @ 2.30GHz

Tests are run with logging disabled

Generally the command lines are:

.. code-block:: sh

   uwsgi --http-socket :9090 --wsgi hello --disable-logging
   
and

.. code-block:: sh

   uwsgi --http-socket :9090 --pypy-home /opt/pypy --pypy-wsgi hello --disable-logging

Simple Hello World
^^^^^^^^^^^^^^^^^^

The most useless of the tests (as it shows only how uWSGI performs instead of the python engine).

.. code-block:: py

   def application(e, sr):
       sr('200 Ok', [('Content-Type', 'text/html')])
       return "ciao"

CPython: 6500 requests per-second, memory used 7MB (no leak detected)

syscalls:

.. code-block:: sh

   0.000403 gettimeofday({1369293059, 218207}, NULL) = 0
   0.000405 read(5, "GET / HTTP/1.1\r\nUser-Agent: curl/7.30.0\r\nHost: ubuntu64.local:9090\r\nAccept: */*\r\n\r\n", 4096) = 83
   0.000638 write(5, "HTTP/1.1 200 Ok\r\nContent-Type: text/html\r\n\r\n", 44) = 44
   0.000678 write(5, "ciao", 4)       = 4
   0.000528 gettimeofday({1369293059, 220477}, NULL) = 0
   0.000394 close(5)

PyPy: 6560 requests per-second, memory used 71MB (no leak detected)

syscalls:

no differences with CPython

Considerations:

there is only slightly (read: irrelevant) better performance in PyPy, but memory usage is 10x higher with PyPy. It needs to be investigated.


CPU-Bound test (fibonacci)
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

CPython: time-to-complete 6400 milliseconds, memory used 65 MB

PyPy: time-to-complete 900 milliseconds, memory used 71 MB

Response time is astonishing, there is no debate about how PyPy is better for CPU intensive tasks (and with high grade of recursion)
, but more interesting is how the memory usage of PyPy remains the same of the simple hello world, while CPython increased 10x

Syscall usage is again the same
