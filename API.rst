The uWSGI api
=============

Language plugins should expose the following api. Each language has its conventions, limits and strength's point.

When porting the api to a specific language try to be friendly to the language style.

This is the "official" list of functions exposed by the uWSGI api, functions not appearing here are not standardized
so they could change their semanthics in future uWSGI relases.


The syntax proposed here is a pseudo-python, each language will expose each function with its specific style

When not_defined is used, it means the language-specific NULL representation (like None in python or undef in perl)

uwsgi.signal(signum)
********************

raise the specified uwsgi signal

uwsgi.register_rpc(name, func, argc=0)
**************************************

register the function "func" as an RPC one with the specified "name"

argc will force the accepted number of arguments

uwsgi.rpc(node, name, *args)
****************************

call the uWSGI RPC function "name" on server "node" with the supplied args (if any)

if node is not_defined a "local" RPC will be made

uwsgi.call(name, *args)
***********************

call the uWSGI RPC function "name" locally with the supplied args (if any)

uwsgi.cache_get(key[, cache])
*****************************

get "key" from the specified "cache". If "cache" is not_defined, the default local cache will be used.

To get an item from a remote cache use the cachename@addr:port syntax for the "cache" value

uwsgi.add_timer(signum, secs)
*****************************

register a timer raising "signum" every "secs"

uwsgi.add_rb_timer(signum, secs)
********************************

register a redblack timer raising "signum" every "secs"

uwsgi.lock(num=0)
*****************

acquire the specified user lock

uwsgi.unlock(num=0)
*******************

release the specified user lock
