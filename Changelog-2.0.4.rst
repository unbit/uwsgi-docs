uWSGI 2.0.4
===========

Changelog [20140422]

Bugfixes
========

- fixed "mime" routing var (Steve Stagg)
- allow duplicate headers in http parsers
- faster on_demand Emperor management
- fixed UWSGI_ADDITIONAL_SOURCES build option
- merge duplicated headers when SPDY is enabled (Łukasz Mierzwa)
- fixed segfault for unnamed loggers
- --need-app works in lazy-apps mode
- fixed fatal hooks management


New features
============

The experimental asyncio loop engine (CPython >= 3.4)
*****************************************************

httprouter advanced timeout management
**************************************

allow disabling cache warnings in --cache2
******************************************

purge LRU cache feature by Yu Zhao (getcwd)
*******************************************

support embedded config on FreeBSD
**********************************

rpc hook
********

setmodifier1 and setmodifier2 routing actions
*********************************************

no_headers option for static router
***********************************

Availability
------------
