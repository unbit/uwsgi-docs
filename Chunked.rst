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

To read a chunk (in blocking way) just run

.. code-block:: perl

   my $msg = uwsgi::chunked_read
   
if no timeout is specified the default one will be used, so if you do not get a chunk in time, the function will croak
(or will raise an exception when under python).

In non-blocking/async engines you may want to use

.. code-block:: perl

   my $msg = uwsgi::chunked_read_nb
   
the function will soon return 'undef' (or None on python) if no chunks are available (and will croak/rais an exception on error)


A full PSGI streaming echo example:

.. code-block:: perl

   # simple PSGI echo app reading chunekd input
   sub streamer {
        $responder = shift;
        # generate the headers and start streaming the response
        my $writer = $responder->( [200, ['Content-Type' => 'text/plain']]);

        while(1) {
                my $msg = uwsgi::chunked_read;
                last unless $msg;
                $writer->write($msg);
        }

        $writer->close;
   }

   my $app = sub {
        return \&streamer;
   };


Tuning the chunks buffer
************************


Integration with proxies
************************

Notes
*****

Calling chunked api functions after having consumed even a single byte of the request body is wrong (this includes post buffering)


