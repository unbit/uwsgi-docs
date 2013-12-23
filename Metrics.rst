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

The metrics subsystem is totally thread-safe

By default uWSGI creates a lot of metrics (and mores are planned) so before adding your own, be sure uWSGI does not already expose the one you need.

Metric names and oids
*********************

Each metric must have a name (containing only numbers, letters, underscores, dashes and dots) and an optional oid.

The oid is required if you want to map a metric to :doc:`SNMP`

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

"avg"
^^^^^

added in 1.9.20

compute the math average of the children

"accumulator"
^^^^^^^^^^^^^

always add the sum of children to the final value.

Ex:

round1: child1 = 22, child2 = 17 -> metric_value = 39

round2: child1 = 26, child2 = 30 -> metric_value += 56

'multiplier"
^^^^^^^^^^^^

multiply the sum of children for the specified arg1n

child1 = 22, child2 = 17, arg1n = 3 -> metric_value = (22+17)*3

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
   
will create a metric 'foobar' with type 'counter', manual collector and no oid.

For creating advanced metrics you need the keyval way:

.. code-block:: sh

   uwsgi --http-socket :9090 --metric name=foobar,type=gauge,oid=100.100.100
   
The following keys are available:

``name`` set the metric name

``oid`` set the metric oid

``type`` set the metric type, can be ``counter``, ``gauge``, ``absolute``, ``alias``

``initial_value`` set the metric to a specific value on startup

``freq`` set the collection frequency in seconds (default to 1)

``children`` maps children to the metric (see below)

``alias`` the metric will be a simple alias for the specified one (--metric name=foobar,alias=worker.0.requests,type=alias)

``arg1`` .. ``arg3`` string based arguments (see below)

``arg1n`` .. ``arg3n`` number based arguments (see below)

``collector`` set the collector, can be ``ptr``, ``file``, ``sum``, ``func`` or anything exposed by plugins. Not specifying a collector means the metric is manual (your app needs to update it).

The ptr is currently unimplemented, while the other collector requires a bit of additional configuration:

``collector=file`` requires ``arg1`` for the filename and an optional ``arg1n`` for the so-called split value.

.. code-block:: sh

   uwsgi --metric name=loadavg,type=gauge,collector=file,arg1=/proc/loadavg,arg1n=1,freq=3
   
this will add a 'loadavg` metric, of type gauge, updated every 3 seconds with the content of /proc/loadavg. The content is splitted (using \\n, \\t, spaces, \\r and zero as separator) and the item 1 (the returned array is zero-based) used as value.

the splitter is very powerful, so you could gather infos from more complex files, like /proc/meminfo

.. code-block:: sh

   uwsgi --metric name=memory,type=gauge,collector=file,arg1=/proc/meminfo,arg1n=4,freq=3
   
once splitted, the /proc/meminfo has the MemFree value in the 4th slot

``collector=sum`` requires the list of metrics that must be summed up. Each metric has the concept of 'children'. The sum collector
will sum the values of all of its children:

.. code-block:: sh

   uwsgi --metric name=reqs,collector=sum,children=worker.1.requests;worker.2.requests
   
this will sum the value of worker.1.requests and worker.2.requests every second

``collector=func`` is a commodity collector avoiding you to write a whole plugin for adding a new collector.

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

this will create a text file for each metric in the 'mymetrics' directory. The content of each file is the value of the metric (updated in realtime).

Each file is mapped in the process address space, so do not worry if your virtual memory increases.


Restoring metrics (persistent metrics)
**************************************

When you restart a uWSGI instance, all of its metrics are reset.

This is generally the best thing to do, but if you want you can restore the previous situation, abusing the values stored in the metrics
directory defined before.

Just add the ``--metrics-dir-restore`` option to force the metric subsystem to read-back the values from the metric directory before
starting collecting values.

API
***

Your language plugins should expose at least the following api functions. Currently they are implemented in Perl, CPython, PyPy and Ruby

metric_get(name)

metric_set(name, value)

metric_inc(name[, delta])

metric_dec(name[, delta])

metric_mul(name[, delta])

metric_div(name[, delta])

metrics (tuple/array of metric keys, should be immutable and not-callable, currently unimplemented)

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

plugin: rrdtool (builtin by default)

requires: librrd.so (dynamically detected on startup, not needed when building)

this will store an rrd file for each metric in the specified directory. Eacch rrd file has a single data source named 'metric'

Usage:

.. code-block:: sh

   uwsgi --rrdtool my_rrds ...
   
or

.. code-block:: sh

   uwsgi --stats-push rrdtool:my_rrds ...
   
by default the rrd files are updated every 300 seconds, you can tune this value with ``--rrdtool-freq``

The librrd.so library is detected at runtime. If you need you can specify its absolute path with ``--rrdtool-lib``

statsd
^^^^^^

type: raw

plugin: stats_pusher_statsd

push metrics to a statsd server

syntax: --stats-push statsd:address[,prefix]

example:

.. code-block:: sh

    uwsgi --stats-push statsd:127.0.0.1:8125,myinstance ...

carbon
^^^^^^

type: raw

plugin: carbon (builtin by default)

see :doc:`Carbon`

zabbix
^^^^^^

type: raw

plugin: zabbix

push metrics to a zabbix server

syntax: --stats-push zabbix:address[,prefix]

example: 

.. code-block:: sh

   uwsgi --stats-push zabbix:127.0.0.1:10051,myinstance ...
   
The plugin exposes a ``--zabbix-template`` option that will generate a zabbix template (on stdout or in the specified file) containing all of the exposed metrics as trapper items.

Note: on some zabbox version you need to authorize the ip addresses allowed to push items

mongodb
^^^^^^^

type: json

plugin: stats_pusher_mongodb

required: libmongoclient.so

push statistics (as json) the the specified mongodb database

syntax (keyval): --stats-push mongodb:addr=<addr>,collection=<db>,freq=<freq>

file
^^^^

type: json

plugin: stats_pusher_file

example plugin storing stats json in a file

socket
^^^^^^

type: raw

plugin: stats_pusher_socket (builtin by default)

push metrics to a udp server with the following format:

<metric> <type> <value>

(<type> is in the numeric form previously reported)

syntax: --stats-push socket:address[,prefix]

Example:

.. code-block:: sh

   uwsgi --stats-push socket:127.0.0.1:8125,myinstance ...

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
   
Specifying an alarm is not required, using the threshold value to automatically reset a metric is perfectly valid
   
Note: --metric-threshold and --metric-alarm are the same option

SNMP integration
****************

The :doc:`SNMP` server exposes metrics starting from the 1.3.6.1.4.1.35156.17.3 OID.

For example to get the value of worker.0.requests:

.. code-block:: sh

   snmpget -v2c -c <snmp_community> <snmp_addr>:<snmp_port> 1.3.6.1.4.1.35156.17.3.0.1
   
Remember: only metrics with an associated OID can be used via SNMP

Internal Routing integration
****************************

The ''router_metrics'' plugin (builtin by default) adds a series of actions to the internal routing subsystem.

``metricinc:<metric>[,value]`` increase the <metric>

``metricdec:<metric>[,value]`` decrease the <metric>

``metricmul:<metric>[,value]`` multiply the <metric>

``metricdiv:<metric>[,value]`` divide the <metric>

``metricset:<metric>,<value>`` set <metric> to <value>

in addition to action a route var named "metric" is added

Example:

.. code-block:: ini

   [uwsgi]
   metric = mymetric
   route = ^/foo metricinc:mymetric
   route-run = log:the value of the metric 'mymetric' is ${metric[mymetric]}
   log-format = %(time) - %(metric.mymetric)

Request logging
***************

You can access metrics values from your request logging format using the %(metric.xxx) placeholder:

.. code-block:: ini

   [uwsgi]
   log-format = [hello] %(time) %(metric.worker.0.requests)

Officially Registered Metrics
*****************************

This is a work in progress, best way to know which default metrics are exposed is enabling the stats server and querying it (or adding the --metrics-dir option)

 * worker/3 (exports information about workers, example worker.1.requests [or 3.1.1] reports the number of requests served by worker 1)
 
 * plugin/4 (namespace for metrics automatically added by plugins, example plugins.foo.bar)
 
 * core/5 (namespace for general instance informations)
 
 * router/6 (namespace for corerouters, example router.http.active_sessions)
 
 * socket/7 (namespace for sockets, example socket.0.listen_queue)
 
 * mule/8 (namespace for mules, example mule.1.signals)
 
 * spooler/9 (namespace for spoolers, example spooler.1.signals)
 
 * system/10 (namespace for system metrics, like loadavg or free memory)
 
OID assigment for plugins
*************************

If you want to write plugin that will expose metrics, please first add OID namespace that you are going to use to the list below and make a pull request.
This will ensure that all plugins are using unique OID namespaces.
Prefix all plugin metric names with plugin name to ensure no conflicts if same keys are used in multiple plugins (example plugin.myplugin.foo.bar, worker.1.plugin.myplugin.foo.bar)

 * (3|4).100.1 - cheaper_busyness

External tools
**************

Check https://github.com/unbit/unbit-bars
