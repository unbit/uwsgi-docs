Python support
==============

Configuration variables
-----------------------

.. seealso:: :doc:`OptionsPython`

Application dictionary
----------------------

.. code-block:: python

  import uwsgi
  import django.core.handlers.wsgi

  application = django.core.handlers.wsgi.WSGIHandler()

  def myapp(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    yield 'Hello World\n'

  uwsgi.applications = {
    '': application,
    '/django': 'application',
    '/myapp': myapp
  }


Passing this Python module name (that is, it should be importable and without the ``.py`` extension) to uWSGI's ``module`` / ``wsgi`` option, uWSGI will search the ``uwsgi.applications`` dictionary for the URL prefix/callable mappings.

The value of every item can be a callable, or its name as a string.

.. TODO: Where is the string looked up from?