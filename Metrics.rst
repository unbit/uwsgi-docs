The Metrics subsystem
=====================

(available from 1.9.19)

The uWSGI metrics subsystem allows you to manage "numbers" from your app.

While the caching subsystem got math capabilities during 1.9 development cycle, the metrics subsystem
is optimized by design for storing numbers and applying functions over them. So compared to the caching subsystem is way faster
and requires a fraction of the memory.

When enabled, the metric subsystem configures a vast amount of metrics (like requests per-core, memory usage...) but, in addition to this, you can configure your own metrics
(for example you can account the number users or the hit of a particular url, as well as the memory consumption of your app or the whole server)

To enable the metrics subsystem just add ``--enable-metrics`` to your options, or configure a stats pusher (see below).

Metric types
************

Before dealing with metrics you need to understand the various types represented by each metric:


COUNTER
^^^^^^^

this is a generally-growing up number (like the number of requests)

GAUGE
^^^^^

this is a number that can increase or decrease dinamically (like the memory used by a worker)

ABSOLUTE
^^^^^^^^

this is an absolute number, like the memory of the whole server, or the size of the hard disk.

ALIAS
^^^^^

this is a virtual metric pointing to another one (you can use it to give different names to already existent metrics)

Metric collectors
*****************

Once you define a metric type, you need to tell uWSGI how to 'collect' the specific metric.

There are various ''collectors'' available (and new can be added via plugins)

"ptr"
^^^^^

the value is collected from a memory pointer

"file"
^^^^^^

the value is collected from a file

"sum"
^^^^^

the value is the sum of other metrics

"func"
^^^^^^

the value is computed calling a specific function every time

"manual" (the NULL collector)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

the value must be updated manually from applications using the metrics api

Custom metrics
**************

The metrics directory
*********************

Restoring metrics (persistent metrics)
**************************************

API
***

metric_get

metric_set

metric_inc

metric_dec

metric_mul

metric_div

metrics (tuple/array of metric keys, should be immutable and not-callable)

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

Alarms/Thresholds
*****************

You can configure one or more "thresholds" to each metric.

Once this limit is reached the specified alarm (see :doc:`AlarmSubsystem`) is triggered.

Once the alarm is delivered you may choose to reset the counter to aspecfic value (generally 0), or continue triggering alarms
with a specified rate.

.. code-block:: ini

   [uwsgi]
   ...
   metric-alarm = key=worker.0.avg_response_time,value=2000,alarm=overload,rate=30
   metric-alarm = key=loadavg,value=3,alarm=overload,rate=120
   metric-threshold = key=mycounter,value=1000,reset=0
   ...
   
Note: --metric-threshold and --metric-alarm are the same option

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
