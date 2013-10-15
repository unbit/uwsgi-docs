The Metrics subsystem
=====================

Metric types
************

COUNTER

GAUGE

ABSOLUTE

Metric collectors
*****************

PTR

FILE

MANUAL

SUM

ALIAS

FUNC


Officially Registered Metrics
*****************************

 * worker/3 (exports information about workers, example worker.1.requests [or 3.1.1] reports the number of requests served by worker 1)
 
 * plugin/4 (namespace for metrics automatically added by plugins, example plugins.foo.bar)
 
 * core/5 (namespace for general instance informations)
 
 * router/6 (namespace for corerouters, example router.http.active_sessions)
