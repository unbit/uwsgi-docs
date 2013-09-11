uWSGI 1.9.16
============

Changelog [201309xx]


Important change in the gevent plugin shutdown/reload procedure !!!
*******************************************************************


Bugfixes/Improvements
*********************

- fixed CPython reference counting bug in rpc and signal handlers
- improved smart-attach-daemon for slow processes
- follow Rack specifications for QUERY_STRING,SCRIPT_NAME,SERVER_NAME and SERVER_PORT
- report missing internal routing support (it is only a warning when libpcre is missing)
- better ipcsem support during shutdown and zerg mode (added --persistent-ipcsem as special case)
- fixed fastcgi bug exposed by apache mod_fastcgi
- do not call pre-jail hook on reload
- force linking with -lrt on solaris
- report thunder lock status


New features
************


Availability
************
