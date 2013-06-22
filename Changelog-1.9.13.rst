uWSGI 1.9.13
============

Changelog [20130622]

Bugfixes
^^^^^^^^

- Fixed a corner case bug when response offloading is enabled, but no request plugin is loaded
- Fixed harakiri routing when multiple rules are in place (return NEXT instead of CONTINUE)
- Fixed curl crashing master on slow dns responses (Łukasz Mierzwa)
- Removed PTRACE check in uwsgi.h (it is no more needed since uWSGI 1.0)
- Fixed --print-sym
- Added a newline in --cflags
- Improved python3 detection and compilation
- Fixed Coro::AnyEvent loop engine (John Berthels)
- Rack api functions are now static
- Better fastcgi handling of big uploads
- Improved GCC usage on Darwin for Python non-apple builds
- Fixed XCLIENT usage in rawrouter
- Use the clang preprocessor instead of hardcoded 'cpp' when CC=clang is used
- Set 16bit options to 65535 when higher values are requested
- Fixed virtualhosting (it is now compatible with 1.4 configurations)

New features
^^^^^^^^^^^^

PyPy performance and features improvents
****************************************

Chunked input api
*****************

Toward better third-party plugins management: the --dot-h option
****************************************************************

setmethod, seturi and setpathinfo routing action
************************************************

UWSGI_INCLUDES
**************


Improved set_user_harakiri api function
***************************************
