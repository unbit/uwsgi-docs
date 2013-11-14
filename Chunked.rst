The Chunked input api
=====================

An api for managing HTTP chunked input requests has been added in uWSGI 1.9.13

The api is very low-level to allows easy integration with standard apps.

There are only two functions exposed:

* chunked_read([timeout])

* chunked_read_nb()

The api is supported (as uWSGI 1.9.20) on CPython, PyPy and Perl


Reading chunks
**************


Tuning the chunks buffer
************************


Integration with proxies
************************

