uWSGI 2.0.4
===========

Changelog [20140422]

Bugfixes
--------

- fixed "mime" routing var (Steve Stagg)
- allow duplicate headers in http parsers
- faster on_demand Emperor management
- fixed UWSGI_ADDITIONAL_SOURCES build option
- merge duplicated headers when SPDY is enabled (Łukasz Mierzwa)
- fixed segfault for unnamed loggers
- --need-app works in lazy-apps mode
- fixed fatal hooks management


New features
------------

The experimental asyncio loop engine (CPython >= 3.4)
*****************************************************

asyncio (also known as 'tulip') is the new infrastructure for writing non-blocking/async/callback-based code with Python 3.

This plugin (experimental) allows you to use asyncio as the uWSGI loop engine

Docs: http://uwsgi-docs.readthedocs.org/en/latest/asyncio.html

httprouter advanced timeout management
**************************************

The http router got 2 new specific timeout:

--http-headers-timeout <n> ; defines the timeout while waiting for http headers

--http-connect-timeout <n> ; defines the timeout when connecting to backend instances

they should help the sysadmin in improving security and availability

Credits: Łukasz Mierzwa

allow disabling cache warnings in --cache2
******************************************

Author: Łukasz Mierzwa

the 'ignore_full' keyval option has beed added to cache2. This will disable warnings when a cache is full

purge LRU cache feature by Yu Zhao (getcwd)
*******************************************

This new mode allows you to configure a cache to automatically expires least recently used (LRU) items when it is full.

Just add purge_lru=1 to your cache2 directive

support embedded config on FreeBSD
**********************************

You can now embed config on FreeBSD systems: 

http://uwsgi-docs.readthedocs.org/en/latest/Embed.html#step-2-embedding-the-config-file

rpc hook
********

Two new hooks have been added:

'rpc' -> call the specified rpc function (fails on error)

'rpcretry' -> call the specified rpc function (retry on error)


setmodifier1 and setmodifier2 routing actions
*********************************************

having to load the 'uwsgi' routing plugin just for setting modifiers was really annoying. This two routing actions (embedded in the core)
allows you to dinamically set modifiers.

no_headers option for static router
***********************************

keyval based static routing action can now avoid to rewrite response headers (useful for X-Sendfile), just add no_headers=1 to your keyval options.

Availability
------------

uWSGI 2.0.4 has been released on 20140422, you can download it from:

http://projects.unbit.it/downloads/uwsgi-2.0.4.tar.gz


