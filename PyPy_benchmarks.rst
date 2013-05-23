Benchmarks for the PyPy plugin
==============================

This is mainly targeted at PyPy developers to spot slow paths or to fix corner-case bug.

uWSGI stresses lot of areas of PyPy (most of them rarely abused in pure-python apps), so making benchmarks is good both for uWSGI and PyPy
