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

By default uWSGI creates a lot of metrics (and mores are planned) so before adding your own, be sure uWSGI does not already expose the one you need.

Metric names and oids
*********************

Each metric must have a name (containing only numbers, letters, underscores, dashes and dots) and an optional oid.

The oid is required if you want to map a metrics to :doc:`SNMP`

Metric types
************

Before dealing with metrics you need to understand the various types represented by each metric:


COUNTER (type 0)
^^^^^^^^^^^^^^^^

this is a generally-growing up number (like the number of requests)

GAUGE (type 1)
^^^^^^^^^^^^^^

this is a number that can increase or decrease dinamically (like the memory used by a worker)

ABSOLUTE (type 2)
^^^^^^^^^^^^^^^^^

this is an absolute number, like the memory of the whole server, or the size of the hard disk.

ALIAS (type 3)
^^^^^^^^^^^^^^

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

You can define additional metrics you can manage from your app.

The ``--metric`` option allows you to add more metrics.

It has a double syntax: simplified and keyval

.. code-block:: sh

   uwsgi --http-socket :9090 --metric foobar
   
will create a metric 'foobar' with type 'counter' and no oid.

For creating advanced metrics you need the keyval way:

.. code-block:: sh

   uwsgi --http-socket :9090 --metric name=foobar,type=gauge,oid=100.100.100
   
The following keys are available:

``name`` set the metric name

``oid`` set the metric oid

``type`` set the metric type, can be ``counter``,``gauge``,``absolute``,``alias``

``initial_value`` set the metric to a specific value on startup

``freq`` set the collection frequency in seconds (default to 1)

``children`` maps children to the metric (see below)

``alias`` the metric will be a simple alias for the specified one (--metric name=foobar,alias=worker.0.requests)

``arg1`` .. ``arg3`` string based arguments (see below)

``arg1n`` .. ``arg3n`` number bused arguments (see below)

``collector`` set the collector, can be ``ptr``,``file``,``sum``, ``func`` or anything exposed by plugins. Not specifying a collector means the metric is manual (your app needs to update it).

The ptr is currently unimplemented, while the other collector requires a bit of additional configuration:

``collector=file`` requires ``arg1`` for the filename and an optional ``arg1n`` for the so-called split value.

.. code-block:: sh

   uwsgi --metric name=loadavg,type=gauge,collector=file,arg1=/proc/loadavg,arg1n=1,freq=3
   
this will add a 'loadavg` metric, of type gauge, updated every 3 seconds with the content of /proc/loadavg. The content is splitted (using \n, \t, spaces, \r and zero as separator) and the item 1 (the returned array is zero-based) used as value.

the splitter is very powerful, so you could gather infos from more complex files, like /proc/meminfo

.. code-block:: sh

   uwsgi --metric name=memory,type=gauge,collector=file,arg1=/proc/meminfo,arg1n=4,freq=3
   
once splitted, the /proc/meminfo has the MemFree value in the 4th slot

``collector=sum`` requires the list of metrics that must be summed up. Each metric has the concept of 'children'. The sum collector
will sum the values of all of its children:

.. code-block:: sh

   uwsgi --metric name=reqs,collector=sum,children=worker.1.requests;worker.2.requests
   
this will sum the value of worker.1.requests and worker.2.requests every second

``collector=func`` is a commodity colelctor avoiding you to write a whole plugin for adding a new collector.

Let's define a C function (call the file mycollector.c or whatever you want):

.. code-block:: c

   int64_t my_collector(void *metric) {
           return 173;
   }
   
and build it as a shared library

.. code-block:: sh

   gcc -shared -o mycollector.so mycollector.c
   
now run uWSGI

.. code-block:: sh

   uwsgi --dlopen ./mycollector.so --metric name=mine,collector=func,arg1=my_collector,freq=10
   
this will call the C function my_collector every 10 seconds and will set the value of the metric 'mine' to its return value.

The function must returns an int64_t value. The argument it takes is a uwsgi_metric pointer. You generally do not need to parse it, so casting to void will avoid headaches.


The metrics directory
*********************

UNIX sysadmins love text files. They are generally the things they have to work on most of the time. If you want to make a UNIX sysadmin happy, just give him some text file to play with.

The metrics subsystem can expose all of its metrics in the form of text files in a directory:

.. code-block:: uwsgi

   uwsgi --metrics-dir mymetrics ...
   
(the mymetric dir must exists)

this will create a text file for each metric in the 'mymetrics' directory. The conent of each file is the value of the metric (updated in realtime).

Each file is mapped in the process address space, so do not worry if your virtual memory increases.


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

socket
^^^^^^

type: raw

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

The :doc:`SNMP` server exposes metrics under the

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
 
 * mule/8 (namespace for mules, example mule.1.signals)
 
 * spooler/9 (namespace for spoolers, example spooler.1.signals)
