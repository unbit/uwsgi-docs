The Symcall plugin
==================

The symcall plugin (modifier 18) is a commodity plugin allowing you to write native uWSGI request handlers without the need of developing a full uWSGI plugin.

You tell it which symbol to load on startup and then it will run it at every request.

Step 1: preparing the environment
*********************************

The uwsgi binary by itself allows you to develop plugins and library without the need of external development packages or headers.

The first step is getting the ``uwsgi.h`` C/C++ header:

.. code-block:: sh

   uwsgi --dot-h > uwsgi.h
   
Now, in the current directory, we have uwsgi.h ready to be included.

Step 2: our first request handler:
**********************************

.. code-block:: c

   #include "uwsgi.h"

   int mysym_function(struct wsgi_request *wsgi_req) {
   
        // read request variables
        if (uwsgi_parse_vars(wsgi_req)) {
                return -1;
        }
        
        // get REMOTE_ADDR
        uint16_t vlen = 0;
        char *v = uwsgi_get_var(wsgi_req, "REMOTE_ADDR", 11, &vlen);
        
        // send status
        if (uwsgi_response_prepare_headers(wsgi_req, "200 OK", 6)) return -1;
        // send content_type
        if (uwsgi_response_add_content_type(wsgi_req, "text/plain", 10)) return -1;
        // send a custom header
        if (uwsgi_response_add_header(wsgi_req, "Foo", 3, "Bar", 3)) return -1;
        
        // send the body
        if (uwsgi_response_write_body_do(wsgi_req, v, vlen)) return -1;
        
        return UWSGI_OK;
   }
