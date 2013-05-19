The uWSGI cheaper subsystem -- adaptive process spawning
========================================================

uWSGI allows to dynamically scale the number of running workers using pluggable algorithms.
This allows to run only required number of workers based on some algorithm specific criteria.

Use ``uwsgi --cheaper-algos-list`` to get the list of available algorithms. 

Usage
-----

To enable cheaper mode You need to add ``cheaper = N`` option to uWSGI configuration file, where N is the minimum number of workers uWSGI can run.
``cheaper`` value needs to be lower than the maximum number of configured workers (``workers`` or ``processes`` option).

.. code-block:: ini

   # set cheaper algorithm to use, if not set default will be used
   cheaper-algo = spare

   # minimum number of workers to keep at all times
   cheaper = 2
   
   # number of workers to spawn at startup
   cheaper-initial = 5

   # maximum number of workers that can be spawned
   workers = 10

   # how many workers should be spawned at a time
   cheaper-step = 1


This will tell uWSGI to run up to 10 workers under load, if app is idle uWSGI will stop workers but it will always leave at least 2 of them running.
With ``cheaper-initial`` you can control how many workers should be spawned at startup. If your average load requires more than minimum number of workers you can have them spawned right away and then cheaped (killed off) if load is low enough.
When the cheaper algorithm decides that it needs more workers it will spawn ``cheaper-step`` of them. This is useful if you have a high maximum number of workers -- in the occasion a sudden load spike hits your app it could otherwise take a lot of time to spawn enough workers one by one.

``spare`` cheaper algorithm
---------------------------

This is the default algorithm.
If all workers are busy for ``cheaper_overload`` seconds then uWSGI will spawn new workers. When the load is gone it will begin stopping processes one at a time.

``backlog`` cheaper algorithm
-----------------------------

.. note:: ``backlog`` is only available on Linux and only on TCP sockets (not UNIX domain sockets).

If the socket's listen queue has more than ``cheaper_overload`` requests waiting to be processed uWSGI will spawn new workers.
If the backlog is lower it will start to stop processes one at a time.

``cheaper`` busyness algorithm
--------------------------

.. note:: This algorithm is optional, it is only available if the ``cheaper_busyness`` plugin is compiled and loaded.

This plugin implements a cheaper algorithm that adds or remove workers based on average utilization for given time period. It's goal is to keep more workers than the minimum needed available at any given time, so that the app will always have some room for new requests. If you want to run only minimum number of workers then use the spare or backlog algorithms.

This plugin exists mostly because the way spare and backlog plugins work causes very aggressive scaling behavior. If you set a low ``cheaper`` value (for example 1), then uWSGI will keep only 1 worker running and spawn new workers only when that running worker is overloaded.
If your app requires more workers, then uWSGI will be spawning and stopping workers all the time, only during times of very low load (such as nights) the minimum number of workers will be enough.
The Busyness algorithm tries to do the opposite: spawn as many workers as needed and stop some of them only when there is a good chance that they are not needed. This should lead to a more stable worker count and much less respawns, and since for most of the time we have little more workers than actually needed, average application respond times should be lower than with other plugins.

Options:

cheaper-overload
****************

Specify intervals (in seconds) for tracking average busyness of workers. Example:

.. code-block:: ini

   cheaper-overload = 30

will to check busyness every 30 seconds. If during the last 30 seconds all workers were running for 3 seconds and idle for the remaining 27 seconds the calculated busyness will be 10% (3/30). This value will decide how fast uWSGI can respond to load spikes. New workers will be spawned at most every ``cheaper-overload`` seconds (unless you are running uWSGI on Linux -- see ``cheaper-busyness-backlog-alert`` for details).
If you want to react to load spikes faster then keep this value low, so that busyness will be calculated more often and proper action can be taken.Keep in mind though that this might cause workers to be started/stopped more often than required since every minor spike may spawn new workers. With a high ``cheaper-overload`` value the worker count will change much less since longer cycles will eat all short spikes of load and extreme values.

cheaper-step
************

How many workers to spawn when any cheaper algorithm decide that it is needed. Default is 1.

cheaper-initial
***************

How many workers should be started when starting the application. After the app is started cheaper algorithm can stop or start workers if needed.

cheaper-busyness-max
********************

This is maximum busyness we allow, every time current calculated busyness for last ``cheaper-overload`` seconds is higher than this value, than uWSGI will spawn new workers (``cheaper-step`` value tells uWSGI how many workers will be spawned).
Default is 50.

cheaper-busyness-min
********************

This is minimum busyness, if current calculated busyness is below this value, than it is considered idle cycle and uWSGI will start counting. Once we reach needed number of subsequent idle cycles than uWSGI will cheap one worker.
Default is 25.

cheaper-busyness-multiplier
***************************

This option tells uWSGI how many subsequent idle cycles we need before stopping (cheaping) one worker. After reaching required number of idle cycles and stopping one worker, we reset this counter so to stop next worker we need to wait the same amount of time.

Example:

.. code-block:: ini
   
   cheaper-overload = 10
   cheaper-busyness-multiplier = 20
   cheaper-busyness-min = 25

If average worker busyness is under 25% for 20 checks in a row, executed every 10 seconds (so we need to wait 200 seconds, 10*20), then one worker will be stopped. The idle cycles counter will be reset if average busyness jumps above ``cheaper-busyness-max`` and we spawn new worker. If during idle cycle counting the average busyness jumps above ``cheaper-busyness-min`` but still below ``cheaper-busyness-max``, then the idle cycles counter is adjusted and we need to wait extra one idle cycle. If during idle cycle counting the average busyness jumps above ``cheaper-busyness-min`` but still below ``cheaper-busyness-max`` three times in a row, then the idle cycle counter is reset.

cheaper-busyness-penalty
************************

uWSGI will automatically tune number of idle cycles needed to stop worker when worker is stopped due to enough idle cycles and then spawned back to fast (less than the same time we need to cheap worker), then we will increment the ``cheaper-busyness-multiplier`` value this value.
Default is 1.

Example:

.. code-block:: ini

   cheaper-overload = 10
   cheaper-busyness-multiplier = 20
   cheaper-busyness-min = 25
   cheaper-busyness-penalty = 2

If average worker busyness is under 25% for 20 checks in a row, executed every 10 seconds (so we need to wait 200 seconds, 10*20), then one worker will be stopped. If new worker is spawned in less than 200 seconds (counting from the time when we spawned the last worker before it), then the ``cheaper-busyness-multiplier`` value will be incremented up to 22 (20+2). Now we will need to wait 220 seconds (22*10) to cheap another worker.

This option is used to prevent workers from being started and stopped all the time since once we stop one worker, busyness might jump up enough to hit ``cheaper-busyness-max``, and a new worker will be spawned and once we have new worker busyness will go down and another worker will be stopped.

cheaper-busyness-verbose
************************

This option will enable debug logs from the ``cheaper_busyness`` plugin, helping you to debug and understand it.

cheaper-busyness-backlog-alert
******************************

This option is only available on Linux. It is used to allow quick response to load spikes even with high ``cheaper-overload`` values. On 
every uWSGI master cycle (default 1 second) the current listen queue is checked. If it is higher than this value, an emergency worker is spawned. When using this option it is safe to use high ``cheaper-overload`` values to have smoother scaling of worker count. Default is 33.

cheaper-busyness-backlog-multiplier
***********************************

This option is only available on Linux. It works just like ``cheaper-busyness-multiplier`` except that it is used only for emergency workers spawned when listen queue was higher than ``cheaper-busyness-backlog-alert``.

Emergency workers are spawned in case of big load spike to prevent currently running workers from being overloaded (it takes some time to spawn new workers due to high average busyness), and sometimes those load spike are random, short and they can spawn a lot of such workers. In such case we would need to wait many cycles before cheaping all those workers, so to cheap them faster we use different multiplier in such case.
Default is 3.

cheaper-busyness-backlog-step
*****************************

This option is only available on Linux. It sets the number of emergency workers spawned when listen queue is higher than ``cheaper-busyness-backlog-alert``. Defaults to 1.

cheaper-busyness-backlog-nonzero
********************************

This option is only available on Linux. It will spawn new emergency worker(s) if request listen queue is > 0 for more than N seconds.
It is used to protect the server from the corner case where there is only single worker running (others are cheaped) and the single worker is handling a long running request. If uWSGI receives new requests they would stay in the request queue until that long running request is completed. With this option we can detect such a condition and spawn new worker to prevent queued requests from being timed out.
Default is 60.

Notes regarding Busyness
************************

* Experiment with settings, there is no one golden rule of what values should be used for everyone. Test and pick values that are best for you. Following uWSGI stats (via Carbon, for instance) will make it easy to decide on good values.
* Don't expect busyness to be constant value, it will change a lot jumping up and down. In the end, real users interact with your apps in very random way. It's recommended to use longer --cheaper-overload values (>=30) to have less spikes.
* If you want to run some benchmarks with this plugin, you should use tools that add randomness to the work load
* With a low number of workers (2-3) starting new worker or stopping one might affect busyness a lot, if You have 2 workers with busyness of 50%, than stopping one of them will increase busyness to 100%. Keep that in mind when picking min and max levels, with only few workers running most of the time max should be more than double of min, otherwise every time one worker is stopped it might increase busyness to above max level.
* With a low number of workers (1-4) and default settings expect that this plugin will keep average busyness below min level, adjust levels to compensate that
* With a higher number of workers required to handle load, workers count should stabilize somewhere near minimum busyness level, jumping a little bit around this value
* When experimenting with this plugin it is advised to enable ``--cheaper-busyness-verbose`` to get an idea of what it is doing. An example log follows.

  .. code-block::

     # These messages are logged at startup to show current settings
     [busyness] settings: min=20%, max=60%, overload=20, multiplier=15, respawn penalty=3
     [busyness] backlog alert is set to 33 request(s)

     # With --cheaper-busyness-verbose enabled You can monitor calculated busyness
     [busyness] worker nr 1 20s average busyness is at 11%
     [busyness] worker nr 2 20s average busyness is at 11%
     [busyness] worker nr 3 20s average busyness is at 20%
     [busyness] 20s average busyness of 3 worker(s) is at 14%

     # Average busyness is under 20%, we start counting idle cycles
     # we have overload=20 and multiplier=15 so we need to wait 300 seconds before we can stop worker
     # cycle we just had was counted as idle so we need to wait another 280 seconds
     # 1 missing second below is just from rounding, master cycle is every 1 second but it also takes some time, this is normal
     [busyness] need to wait 279 more second(s) to cheap worker

     # We waited long enough and we can stop one worker
     [busyness] worker nr 1 20s average busyness is at 6%
     [busyness] worker nr 2 20s average busyness is at 22%
     [busyness] worker nr 3 20s average busyness is at 19%
     [busyness] 20s average busyness of 3 worker(s) is at 15%
     [busyness] 20s average busyness is at 15%, cheap one of 3 running workers

     # After stopping one worker average busyness is now higher, which is no surprise
     [busyness] worker nr 2 20s average busyness is at 36%
     [busyness] worker nr 3 20s average busyness is at 24%
     [busyness] 20s average busyness of 2 worker(s) is at 30%
     # 30% is above our minimum (20%), but it's still far from our maximum (60%)
     # since this is not idle cycle uWSGI will ignore it when counting when to stop worker
     [busyness] 20s average busyness is at 30%, 1 non-idle cycle(s), adjusting cheaper timer

     # After a while our average busyness is still low enough, so we stop another worker
     [busyness] 20s average busyness is at 3%, cheap one of 2 running workers

     # With only one worker running we won't see per worker busyness since it's the same as total average
     [busyness] 20s average busyness of 1 worker(s) is at 16%
     [busyness] 20s average busyness of 1 worker(s) is at 17%

     # Shortly after stopping second worker and with only one running we have load spike that is enough to hit our maximum level
     # this was just few cycles after stopping worker so uWSGI will increase multiplier
     # now we need to wait extra 3 cycles before stopping worker
     [busyness] worker(s) respawned to fast, increasing cheaper multiplier to 18 (+3)

     # Initially we needed to wait only 300 seconds, now we need to have 360 subsequent seconds when workers busyness is below minimum level
     # 10*20 + 3*20 = 360
     [busyness] worker nr 1 20s average busyness is at 9%
     [busyness] worker nr 2 20s average busyness is at 17%
     [busyness] worker nr 3 20s average busyness is at 17%
     [busyness] worker nr 4 20s average busyness is at 21%
     [busyness] 20s average busyness of 4 worker(s) is at 16%
     [busyness] need to wait 339 more second(s) to cheap worker
