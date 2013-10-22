The Metrics subsystem
=====================

Metric types
************

COUNTER

GAUGE

ABSOLUTE

ALIAS

Metric collectors
*****************

"ptr"
^^^^^

"file"
^^^^^^

"sum"
^^^^^

"func"
^^^^^^

"manual" (the NULL collector)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Custom metrics
**************

API
***

metric_get

metric_set

metric_inc

metric_dec

metric_mul

metric_div

Stats pushers
*************

Collected metrics can be sent to external systems for analysis or graphs generation.

Stats pushers are plugins aimed at sending metrics to those systems.

There are two kinds of stats pusher: json and raw.

json stats pusher send the whole json stats blob (the same you get from the stats server), while 'raw' ones send the metrics list.

Currently available stats pushers:

rrdtool
^^^^^^^

type: raw

statsd
^^^^^^

type: raw

carbon
^^^^^^

type: raw

zabbix
^^^^^^

type: raw

mongodb
^^^^^^^

type: json

file
^^^^

type: json


SNMP integration
****************

Internal Routing integration
****************************

Request logging
***************


Officially Registered Metrics
*****************************

 * worker/3 (exports information about workers, example worker.1.requests [or 3.1.1] reports the number of requests served by worker 1)
 
 * plugin/4 (namespace for metrics automatically added by plugins, example plugins.foo.bar)
 
 * core/5 (namespace for general instance informations)
 
 * router/6 (namespace for corerouters, example router.http.active_sessions)
 
 * socket/7 (namespace for sockets, example socket.0.listen_queue)
