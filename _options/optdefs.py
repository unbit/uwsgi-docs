# -- encoding: UTF-8 --
from optutil import Config, _Optional as optional
o_str = optional(str)
o_int = optional(int)

def core_options():
	config = Config("Core")


	with config.section("Networking/sockets") as s:
		s.o(("socket", "uwsgi-socket"), str, u"Bind to the specified socket using default protocol (see `protocol`)", short_name="s")
		s.o("http-socket", str, u"Bind to the specified socket using HTTP")
		s.o("fastcgi-socket", str, u"Bind to the specified socket using FastCGI")
		s.o(("protocol", "socket-protocol"), str, "Force the specified protocol (`uwsgi`, `http`, `fastcgi`) for default sockets")
		s.o("shared-socket", str, "Create a shared socket for advanced jailing or IPC purposes")
		s.o("listen", int, "set the socket listen queue size", short_name="l")
		s.o("abstract-socket", True, "force UNIX socket into abstract mode (Linux only)")
		s.o("chmod-socket", o_str, "chmod socket", short_name='C')
		s.o("chown-socket", str, "chown UNIX sockets")
		s.o("umask", str, "set UNIX socket umask")
		s.o("freebind", True, "put socket in freebind mode (Linux only)")
		s.o("map-socket", [str], "map sockets to specific workers")
		s.o(("zeromq", "zmq", "zeromq-socket", "zmq-socket"), str, "create a zeromq pub/sub pair")
		s.o("udp", str, "run the udp server on the specified address")
		s.o("reuse-port", True, "enable REUSE_PORT flag on socket (BSD only)")

	with config.section("Process Management") as s:
		s.o(("workers", "processes"), int, "spawn the specified number of workers/processes", short_name="p")
		s.o("harakiri", int, "Harakiri timeout in seconds")
		s.o("harakiri-verbose", True, "Enable verbose Harakiri mode")
		s.o(("harakiri-no-arh", "no-harakiri-arh", "no-harakiri-after-req-hook"), True, "Disallow Harakiri killings during after-request-hook")
		s.o("mule-harakiri", int, "Set harakiri timeout for mule tasks")
		s.o("master", True, "Enable uWSGI master process", short_name='M')
		s.o("reaper", True, "call waitpid(-1,...) after each request to get rid of zombies", short_name="r")
		s.o("max-requests", int, "reload workers after the specified amount of managed requests (avoid memory leaks)", short_name='R')
		s.o("limit-as", int, "limit process address space (vsz) (in megabytes)")
		s.o("limit-nproc", int, "limit the number of spawnable processes")
		s.o("reload-on-as", int, "reload if address space is higher than specified megabytes (in megabytes)")
		s.o("reload-on-rss", int, "reload if rss memory is higher than specified megabytes (in megabytes)")
		s.o("evil-reload-on-as", int, "force the master to reload a worker if its address space is higher than specified megabytes (in megabytes)")
		s.o("evil-reload-on-rss", int, "force the master to reload a worker if its rss memory is higher than specified megabytes (in megabytes)")
		s.o("threads", int, "run each worker in prethreaded mode with the specified number of threads")
		s.o(("thread-stacksize", "threads-stacksize", "thread-stack-size", "threads-stack-size"), int, "set threads stacksize")
		s.o("check-interval", int, "set the interval (in seconds) of master checks")

	with config.section("Process Management - Emperor", docs = ["Emperor"]) as s:
		s.o("emperor", [str], "run as the Emperor")
		s.o("emperor-freq", int, "set the Emperor scan frequency (default 3 seconds)")
		s.o("emperor-required-heartbeat", int, "set the Emperor tolerance about heartbeats")
		s.o("emperor-pidfile", str, "write the Emperor pid in the specified file")
	 	s.o("emperor-tyrant", True, "put the Emperor in Tyrant mode")
		s.o(("emperor-stats", "emperor-stats-server"), str, "run the Emperor stats server")
	 	s.o("early-emperor", True, "spawn the emperor as soon as possibile")
		s.o("emperor-broodlord", int, "run the emperor in BroodLord mode")
		s.o("emperor-throttle", int, "set throttling level (in milliseconds) for bad behaving vassals (default 1000)")
		s.o("emperor-max-throttle", int, "set max throttling level (in milliseconds) for bad behaving vassals (default 3 minutes)")
	 	s.o("emperor-magic-exec", True, "prefix vassals config files with exec as s:// if they have the executable bit")
	 	s.o(("imperial-monitor-list", "imperial-monitors-list"), True, "list enabled imperial monitors")
		s.o("vassals-inherit", [str], "add given config templates to vassals' config")
		s.o("vassals-start-hook", str, "run the specified command before each vassal starts")
		s.o("vassals-stop-hook", str, "run the specified command after vassal's death")
		s.o("vassal-sos-backlog", int, "ask emperor for sos if backlog queue has more items than the value specified")
		s.o("heartbeat", int, "announce healtness to the emperor")
		s.o("auto-snapshot", o_int, "automatically make workers snapshot after reload")
		s.o("reload-mercy", int, "set the maximum time (in seconds) a worker can take to reload/shutdown")

	with config.section("Process Management - Zerg", docs = ["Zerg"]) as s:
		s.o("zerg", [str], "attach to a zerg server")
		s.o("zerg-fallback", True, "fallback to normal sockets if the zerg server is not available")
		s.o("zerg-server", str, "enable the zerg server on the specified UNIX socket")
		s.o(("zergpool", "zerg-pool"), [str], "start a zergpool on specified address for specified address (zergpool plugin)")


	with config.section("Debugging") as s:
		s.o("backtrace-depth", int, "Set backtrace depth")
		s.o("memory-report", True, "enable memory report", short_name="m")
		s.o("profiler", str, "enable the specified profiler")
		s.o("dump-options", True, "dump the full list of available options")
		s.o("show-config", True, "show the current config reformatted as ini")
		s.o("print", str, "simple print (for your convenience)")
		s.o("cflags", True, "report uWSGI CFLAGS (useful for building external plugins)")
		s.o("version", True, "print uWSGI version")		
		s.o("allowed-modifiers", str, "comma separated list of allowed modifiers")
		s.o("connect-and-read", "str", "connect to a socket and wait for data from it")

	with config.section("Configuration", docs = ["Configuration"]) as s:
		s.o("set", str, "Set a custom placeholder for configuration")
		s.o("declare-option", str, "Declare a new custom uWSGI option")
		s.o("inherit", str, u"Use the specified file as configuration template")
		s.o(("plugins", "plugin"), int, "load uWSGI plugins")
		s.o(("plugins-dir", "plugin-dir"), [str], "add a directory to uWSGI plugin search path")
		s.o(("plugins-list", "plugin-list"), True, "list enabled plugins")
		s.o("autoload", True, "try to automatically load plugins when unknown options are found")
		s.o("dlopen", str, "blindly load a shared library")

		s.o("ini", int, "load config from ini file")
		s.o(("xml", "xmlconfig"), str, "Load XML file as configuration", short_name="x")
		s.o(("yaml", "yal"), str, "load config from yaml file", short_name="y")
		s.o(("json", "js"), str, "load config from json file", short_name="j")
		s.o(("sqlite3", "sqlite"), int, "load config from sqlite3 db")
		s.o("ldap", int, "load configuration from ldap server", docs = ["LDAP"])
		s.o("ldap-schema", True, "dump uWSGI ldap schema", docs = ["LDAP"])
		s.o("ldap-schema-ldif", True, "dump uWSGI ldap schema in ldif format", docs = ["LDAP"])
		



	with config.section("Config logic", docs = ["ConfigLogic"]) as s:
		s.o("for", str, "For cycle")
		s.o("endfor", optional(str), "End for cycle")
		s.o("if-opt", str, "Check for option")
		s.o("if-not-opt", str, "Check for lack of option")
		s.o(("if-env", "ifenv"), str, "Check for environment variable")
		s.o("if-not-env", str, "Check for lack of environment variable")
		s.o("if-reload", str, "Check for reload")
		s.o("if-not-reload", str, "Check for lack of reload")
		s.o(("if-exists", "ifexists"), str, "Check for file/directory existence")
		s.o("if-not-exists", str, "Check for file/directory inexistence")
		s.o("if-file", str, "Check for file existence")
		s.o("if-not-file", str, "Check for file inexistence")
		s.o(("if-dir", "ifdir", "if-directory"), str, "Check for directory existence")
		s.o("if-not-dir", str, "Check for directory inexistence")
		s.o("endif", optional(str), "End if block")

	with config.section("Logging", docs = ["Logging"]) as s:
		s.o("disable-logging", True, "disable request logging", short_name="L")
		s.o("ignore-sigpipe", True, "do not report (annoying) SIGPIPE")
		s.o("ignore-write-errors", True, "do not report (annoying) write()/writev() errors")
		s.o("write-errors-tolerance", int, "set the maximum number of allowed write errors (default: no tolerance)")
		s.o("write-errors-exception-only", True, "only raise an exception on write errors giving control to the app itself")
		s.o("disable-write-exception", True, "disable exception generation on write()/writev()")
		s.o("logto", str, "set logfile/udp address")
		s.o("logto2", str, "log to specified file or udp address after privileges drop")
		s.o(("log-format", "logformat"), str, "set advanced format for request logging")
		s.o(("logformat-strftime", "log-format-strftime"), True, "apply strftime to logformat output")
		s.o("logfile-chown", True, "chown logfiles")
		s.o("logfile-chmod", str, "chmod logfiles")
		s.o("log-syslog", o_str, "Log to syslog")
		s.o("log-socket", str, "Send logs to the specified socket")
		s.o("logger", [str], "Set/append a logger")
		s.o(("logger-list", "loggers-list"), True, "list enabled loggers")
		s.o("threaded-logger", True, "offload log writing to a thread")
		s.o("log-drain", ["regexp"], "drain (do not show) log lines matching the specified regexp")
		s.o("log-zeromq", str, "send logs to a ZeroMQ server")
		s.o("log-master", True, "delegate logging to master process")
		s.o("log-master-bufsize", int, "Set the buffer size for the master logger. Log messages larger than this will be truncated.")
		s.o("log-reopen", True, "reopen log after reload")
		s.o("log-truncate", True, "truncate log on startup")
		s.o("log-maxsize", int, "set maximum logfile size")
		s.o("log-backupname", str, "set logfile name after rotation")
		s.o(("log-prefix", "logdate", "log-date"), o_str, "prefix logs with date (without argument) or a strftime string")
		s.o("log-zero", True, "log responses without body")
		s.o("log-slow", int, "log requests slower than the specified number of milliseconds")
		s.o("log-4xx", True, "log requests with a 4xx response")
		s.o("log-5xx", True, "log requests with a 5xx response")
		s.o("log-big", int, "log requestes bigger than the specified size in bytes")
		s.o("log-sendfile", True, "log sendfile requests")
		s.o("log-micros", True, "report response time in microseconds instead of milliseconds")
		s.o("log-x-forwarded-for", True, "use the ip from X-Forwarded-For header instead of REMOTE_ADDR")
		s.o(("stats", "stats-server"), str, "enable the stats server on the specified address")
		s.o("ssl-verbose", True, "be verbose about SSL errors")
		s.o("snmp", [str], "Enable the embedded SNMP server")
		s.o("snmp-community", str, "Set the SNMP community string")

	with config.section("Alarms", docs = ["Alarms"]) as s:
		s.o("alarm", [str], "Create a new alarm. Syntax: <alarm> <plugin:args>")
		s.o("alarm-freq", int, "tune the alarm anti-loop system (default 3 seconds)")
		s.o("log-alarm", [str], "raise the specified alarm when a log line matches the specified regexp, syntax: <alarm>[,alarm...] <regexp>")
		s.o(("alarm-list", "alarms-list"), True, "list enabled alarms")


	with config.section("uWSGI Process") as s:
		s.o("daemonize", "logfile", "daemonize uWSGI, write messages into given log file or UDP socket address")
		s.o("daemonize2", "logfile", "daemonize uWSGI after loading application, write messages into given log file or UDP socket address")
		s.o("stop", "pidfile", "send the stop (SIGINT) signal to the instance described by the pidfile")
		s.o("reload", "pidfile", "send the reload (SIGHUP) signal to the instance described by the pidfile")
		s.o("pause", "pidfile", "send the pause (SIGTSTP) signal to the instance described by the pidfile")
		s.o("suspend", "pidfile", "send the suspend (SIGTSTP) signal to the instance described by the pidfile")
		s.o("resume", "pidfile", "send the resume (SIGTSTP) signal to the instance described by the pidfile")
		s.o("auto-procname", True, "Automatically set process name to something meaningful")
		s.o("procname-prefix", str, "Add prefix to process names")
		s.o("procname-prefix-spaced", str, "Add spaced prefix to process names")
		s.o("procname-append", str, "Append string to process names")
		s.o("procname", str, "Set process name")
		s.o("procname-master", str, "Set master process name")
		s.o("pidfile", str, "create pidfile (before privileges drop)")
		s.o("pidfile2", str, "create pidfile (after privileges drop)")
		s.o("chroot", str, "chroot() to the specified directory")
		s.o("uid", "username|uid", "setuid to the specified user/uid")
		s.o("gid", "groupname|gid", "setgid to the specified grooup/gid")
		s.o("no-initgroups", True, "disable additional groups set via initgroups()")
		s.o("cap", str, "set process capability")
		s.o("unshare", str, "unshare() part of the processes and put it in a new namespace")
		s.o("exec-pre-jail", [str], "run the specified command before jailing")
		s.o("exec-post-jail", [str], "run the specified command after jailing")
		s.o("exec-in-jail", [str], "run the specified command in jail after initialization")
		s.o("exec-as-root", [str], "run the specified command before privileges drop")
		s.o("exec-as-user", [str], "run the specified command after privileges drop")
		s.o("exec-as-user-atexit", [str], "run the specified command before app exit and reload")
		s.o("exec-pre-app", [str], "run the specified command before app loading")
		s.o("cgroup", [str], "put the processes in the specified cgroup")
		s.o("cgroup-opt", [str], "set value in specified cgroup option")
		s.o(("namespace", "ns"), str, "run in a new namespace under the specified rootfs")
		s.o("namespace-keep-mount", [str], "keep the specified mountpoint in your namespace")
		s.o(("namespace-net", "ns-net"), str, "add network namespace")
		s.o("forkbomb-delay", int, "sleep for the specified number of seconds when a forkbomb is detected")
		s.o("binary-path", str, "force binary path")
		s.o("privileged-binary-patch", str, "patch the uwsgi binary with a new command (before privileges drop)")
		s.o("unprivileged-binary-patch", str, "patch the uwsgi binary with a new command (after privileges drop)")
		s.o("privileged-binary-patch-arg", str, "patch the uwsgi binary with a new command and arguments (before privileges drop)")
		s.o("unprivileged-binary-patch-arg", str, "patch the uwsgi binary with a new command and arguments (after privileges drop)")
		s.o("async", int, "enable async mode with specified cores")
		s.o("max-fd", int, "set maximum number of file descriptors (requires root privileges)")
		s.o("master-as-root", True, "leave master process running as root")
		

	with config.section("Miscellaneous") as s:
		s.o("skip-zero", True, "skip check of file descriptor 0")
		s.o("need-app", True, "exit if no app can be loaded")
		s.o("exit-on-reload", True, "force exit even if a reload is requested")
		s.o("die-on-term", True, "exit instead of brutal reload on SIGTERM")
		s.o("no-fd-passing", True, "disable file descriptor passing")
		s.o("single-interpreter", True, "do not use multiple interpreters (where available)", short_name="i")
		s.o("max-apps", int, "set the maximum number of per-worker applications")
		s.o("sharedarea", int, "create a raw shared memory area of specified pages", short_name="A")
		s.o("cgi-mode", True, "force CGI-mode for plugins supporting it", short_name="c")
		s.o("buffer-size", int, "set internal buffer size", short_name="b")
		s.o("enable-threads", True, "enable threads", short_name="T")
		s.o(("signal-bufsize", "signals-bufsize"), int, "set buffer size for signal queue")
		s.o("socket-timeout", int, "Set internal sockets timeout", short_name='z')
		s.o("max-vars", int, "Set the amount of internal iovec/vars structures", short_name='v')
		s.o("weight", int, "weight of the instance (used by clustering/lb/subscriptions)")
		s.o("auto-weight", int, "set weight of the instance (used by clustering/lb/subscriptions) automatically")
		s.o("no-server", True, "force no-server mode")
		s.o("command-mode", True, "force command mode")
		s.o("no-defer-accept", True, "disable deferred-accept on sockets")
		s.o("so-keepalive", True, "enable TCP KEEPALIVEs")
		s.o("never-swap", True, "lock all memory pages avoiding swapping")
		s.o("ksm", [int], "enable Linux KSM")
		s.o("touch-reload", [str], "reload uWSGI if the specified file is modified/touched")
		s.o("touch-logrotate", [str], "trigger logrotation if the specified file is modified/touched")
		s.o("touch-logreopen", [str], "trigger log reopen if the specified file is modified/touched")
		s.o("propagate-touch", True, "over-engineering option for system with flaky signal mamagement")
		s.o("no-orphans", True, "automatically kill workers if master dies (can be dangerous for availability)")
		s.o("prio", int, "set processes/threads priority")
		s.o("cpu-affinity", int, "set cpu affinity")
		s.o("remap-modifier", str, "remap request modifier from one id to another")
		s.o("env", str, "set environment variable (key=value)")
		s.o("unenv", str, "set environment variable (key)")
		s.o("close-on-exec", True, "set close-on-exec on sockets (could be required for spawning processes in requests)")
		s.o("mode", str, "set uWSGI custom mode")
		s.o("vacuum", True, "try to remove all of the generated files/sockets upon exit")
		s.o("cron", str, "Add a cron task")
		s.o("worker-exec", str, "run the specified command as worker")
		s.o("attach-daemon", str, "Attach a command/daemon to the master process (the command has to remain in foreground)")
		s.o("smart-attach-daemon", "pidfile", "Attach a command/daemon to the master process managed by a pidfile (the command must daemonize)")
		s.o("smart-attach-daemon2", "pidfile", "Attach a command/daemon to the master process managed by a pidfile (the command must NOT daemonize)")

	with config.section("Locks") as s:
		s.o("locks", int, "create the specified number of shared locks")
		s.o("lock-engine", str, "set the lock engine")
		s.o("ftok", str, "set the ipcsem key via ftok() for avoiding duplicates")
		s.o("flock", str, "lock the specified file before starting, exit if locked")
		s.o("flock-wait", str, "lock the specified file before starting, wait if locked")
		s.o("flock2", str, "lock the specified file after logging/daemon setup, exit if locked")
		s.o("flock-wait2", str, "lock the specified file after logging/daemon setup, wait if locked")

	with config.section("Cache", docs=["Caching"]) as s:	
		s.o("cache", int, "create a shared cache containing given elements")
		s.o("cache-blocksize", int, "set cache blocksize")
		s.o("cache-store", str, "enable persistent cache to disk")
		s.o("cache-store-sync", int, "set frequency of sync for persistent cache")
		s.o("cache-server", str, "enable the threaded cache server")
		s.o("cache-server-threads", int, "set the number of threads for the cache server")
		s.o("cache-no-expire", True, "disable auto sweep of expired items")
		s.o("cache-expire-freq", int, "set the frequency of cache sweeper scans (default 3 seconds)")
		s.o("cache-report-freed-items", True, "constantly report the cache item freed by the sweeper (use only for debug)")

	with config.section("Queue", docs=["Queue"]) as s:
		s.o("queue", int, "Enable the shared queue with the given size.")
		s.o("queue-blocksize", int, "Set the block size for the queue")
		s.o("queue-store", "filename", "Enable periodical persisting of the queue to disk")
		s.o("queue-store-sync", int, "Set periodical persisting frequency in seconds")

	with config.section("Spooler", docs=["Spooler"]) as s:
		s.o("spooler", str, "run a spooler on the specified directory", short_name='Q')
		s.o("spooler-external", str, "map spooler requests to a spooler directory managed by an external instance")
		s.o("spooler-ordered", True, "try to order the execution of spooler tasks")
		s.o("spooler-chdir", str, "chdir() to specified directory before each spooler task")
		s.o("spooler-processes", int, "set the number of processes for spoolers")
		s.o("spooler-quiet", True, "do not be verbose with spooler tasks")
		s.o("spooler-max-tasks", int, "set the maximum number of tasks to run before recycling a spooler")
	 	s.o("spooler-harakiri", int, "set harakiri timeout for spooler tasks")

	with config.section("Mules", docs=["Mules"]) as s:
		s.o("mule", [str], "add a mule (signal-only mode without argument)")
		s.o("mules", int, "add the specified number of mules")
		s.o("farm", str, "add a mule farm")
		s.o("signal", str, "send a uwsgi signal to a server")

	with config.section("Application loading") as s:
		s.o("chdir", str, "chdir to specified directory before apps loading")
		s.o("chdir2", str, "chdir to specified directory after apps loading")
		s.o("lazy", True, "set lazy mode (load apps in workers instead of master)")
		s.o("lazy-apps", True, "load apps in each worker instead of the master")
		s.o("cheap", True, "set cheap mode (spawn workers only after the first request)")
		s.o("cheaper", int, "set cheaper mode (adaptive process spawning)")
		s.o("cheaper-initial", int, "set the initial number of processes to spawn in cheaper mode")
		s.o("cheaper-algo", str, "choose to algorithm used for adaptive process spawning)")
		s.o("cheaper-step", int, "number of additional processes to spawn at each overload")
		s.o("cheaper-overload", int, "increase workers after specified overload")
		s.o(("cheaper-algo-list", "cheaper-algos-list", "cheaper-list"), True, "list enabled 'cheaper' algorithms")
		s.o("idle", int, "set idle mode (put uWSGI in cheap mode after inactivity)")
		s.o("die-on-idle", True, "shutdown uWSGI when idle")
		s.o("mount", [str], "load application under mountpoint")
		s.o("worker-mount", [str], "load application under mountpoint in the specified worker or after workers spawn")
		s.o("grunt", True, "enable grunt mode (in-request fork)")

	with config.section("Request handling") as s:
		s.o("limit-post", int, "limit request body (bytes)")
		s.o("post-buffering", int, "enable post buffering past N bytes")
	 	s.o("post-buffering-bufsize", int, "set buffer size for read() in post buffering mode")
		s.o("upload-progress", str, "enable creation of .json files in the specified directory during a file upload")
		s.o("no-default-app", True, "do not fallback to default app")
		s.o("manage-script-name", True, "automatically rewrite SCRIPT_NAME and PATH_INFO")
		s.o("ignore-script-name", True, "ignore SCRIPT_NAME")
		s.o("catch-exceptions", True, "report exception as HTTP output (discouraged -- this is a security risk)")
		s.o("reload-on-exception", True, "reload a worker when an exception is raised")
		s.o("reload-on-exception-type", [str], "reload a worker when a specific exception type is raised")
		s.o("reload-on-exception-value", [str], "reload a worker when a specific exception value is raised")
		s.o("reload-on-exception-repr", [str], "reload a worker when a specific exception type+value (language-specific) is raised")
		s.o("add-header", [str], "automatically add HTTP headers to response")
		s.o("vhost", True, "enable virtualhosting mode (based on SERVER_NAME variable)")
		s.o("vhost-host", True, "enable virtualhosting mode (based on HTTP_HOST variable)")
	
	with config.section("Clustering") as s:
		s.o("multicast", str, "subscribe to specified multicast group")
		s.o("multicast-ttl", int, "set multicast ttl")
		s.o("cluster", str, "join specified uWSGI cluster")
		s.o("cluster-nodes", str, "get nodes list from the specified cluster")
		s.o("cluster-reload", str, "send a reload message to the cluster")
		s.o("cluster-log", str, "send a log line to the cluster")
	
	with config.section("Subscriptions", docs=["SubscriptionServer"]) as s:
		s.o("subscriptions-sign-check", str, "set digest algorithm and certificate directory for secured subscription system")
		s.o("subscriptions-sign-check-tolerance", int, "set the maximum tolerance (in seconds) of clock skew for secured subscription system")
		s.o("subscription-algo", str, "set load balancing algorithm for the subscription system")
		s.o("subscription-dotsplit", True, "try to fallback to the next part (dot based) in subscription key")
		s.o(("subscribe-to", "st", "subscribe"), [str], "subscribe to the specified subscription server")
		s.o("subscribe-freq", int, "send subscription announce at the specified interval")
		s.o("subscription-tolerance", int, "set tolerance for subscription servers")
		s.o("unsubscribe-on-graceful-reload", True, "force unsubscribe request even during graceful reload")
	
	with config.section("Router", docs=["InternalRouting"]) as s:
		s.o("route", [str], "add a route")
		s.o("route-host", [str], "add a route based on Host header")
		s.o("route-uri", [str], "add a route based on REQUEST_URI")
		s.o("route-qs", [str], "add a route based on QUERY_STRING")
		s.o(("router-list", "routers-list"), True, "list enabled routers")
		
	with config.section("Static files") as s:
		s.o(("static-check", "check-static"), [str], "check for static files in the specified directory")
		s.o("check-static-docroot", True, "check for static files in the requested DOCUMENT_ROOT")
		s.o("static-map", [str], "map mountpoint to static directory (or file)")
		s.o("static-map2", [str], "map mountpoint to static directory (or file), completely appending the requested resource to the docroot")
		s.o("static-skip-ext", [str], "skip specified extension from staticfile checks")
		s.o("static-index", [str], "search for specified file if a directory is requested")
		s.o(("mimefile", "mime-file"), [str], "set mime types file path (default /etc/mime.types)")
		s.o("static-expires-type", [str], "set the Expires header based on content type (syntax: Content-type=Expires)")
		s.o("static-expires-type-mtime", [str], "set the Expires header based on content type and file mtime (syntax: Content-type=Expires)")
		s.o("static-expires", [str], "set the Expires header based on filename regexp (syntax x=y)")
		s.o("static-expires-mtime", [str], "set the Expires header based on filename regexp and file mtime (syntax x=y)")
		s.o("static-expires-uri", [str], "set the Expires header based on REQUEST_URI regexp (syntax x=y)")
		s.o("static-expires-uri-mtime", [str], "set the Expires header based on REQUEST_URI regexp and file mtime (syntax x=y)")
		s.o("static-expires-path-info", [str], "set the Expires header based on PATH_INFO regexp (syntax x=y)")
		s.o("static-expires-path-info-mtime", [str], "set the Expires header based on PATH_INFO regexp and file mtime (syntax x=y)")
		s.o("static-offload-to-thread", int, "offload static file serving to a thread (upto the specified number of threads)")
		s.o("file-serve-mode", str, "set static file serving mode (x-sendfile, nginx, ...)")
		s.o("check-cache", True, "check for response data in the cache")
	
	with config.section("Clocks") as s:
		s.o("clock", str, "set a clock source")
		s.o(("clock-list","clocks-list"), True, "list enabled clocks")

	with config.section("Loop engines") as s:
		s.o("loop", str, "select the uWSGI loop engine")
		s.o(("loop-list", "loops-list"), True, "list enabled loop engines")

	return config

def python_options():
	config = Config("Python")
	with config.section("Python", docs = ["Python"]) as s:
		s.o(("wsgi-file", "file"), str, "load .wsgi file")
		s.o("eval", str, "eval python code")
		s.o(("module", "wsgi"), str, "load a WSGI module", short_name="w")
		s.o("callable", str, "set default WSGI callable name")
		s.o("test", str, "test a module import", short_name="J")
		s.o(("home", "virtualenv", "venv", "pyhome"), str, "set PYTHONHOME/virtualenv", short_name="H")
		s.o(("py-programname", "py-program-name"), str, "set python program name")
		s.o(("pythonpath", "python-path", "pp"), ['directory/glob'], "add directory (or glob) to pythonpath")
		s.o("pymodule-alias", [str], "add a python alias module")
		s.o("post-pymodule-alias", [str], "add a python module alias after uwsgi module initialization")
		s.o(("import", "pyimport", "py-import", "python-import"), [str], "import a python module")
		s.o(("shared-import", "shared-pyimport", "shared-py-import", "shared-python-import"), [str], "import a python module in all of the processes")
		s.o(("spooler-import", "spooler-pyimport", "spooler-py-import", "spooler-python-import"), [str], "import a python module in the spooler")
		s.o("pyargv", str, "manually set sys.argv")
		s.o("optimize", int, "set python optimization level", short_name="O")
		s.o("paste", str, "load a paste.deploy config file")
		s.o("paste-logger", True, "enable paste fileConfig logger")
		s.o("web3", str, "load a web3 app")
		s.o("pump", str, "load a pump app")
		s.o("wsgi-lite", str, "load a wsgi-lite app")
		s.o("ini-paste", 'paste .INI', "load a paste.deploy config file containing uwsgi section")
		s.o("ini-paste-logged", 'paste .INI', "load a paste.deploy config file containing uwsgi section (load loggers too)")
		s.o("reload-os-env", True, "force reload of os.environ at each request")
		s.o("no-site", True, "Do not import site module")
		s.o("pyshell", True, "Run an interactive Python shell in the uWSGI environment")
		s.o("pyshell-oneshot", True, "Run an interactive Python shell in the uWSGI environment (one-shot variant)")
		s.o(("python", "py", "pyrun"), '.py file', "Run a Python script in the uWSGI environment")
		s.o("py-tracebacker", str, "enable the uWSGI Python tracebacker")
		s.o(("py-auto-reload", "py-autoreload", "python-auto-reload", "python-autoreload"), int, "Monitor Python modules' modification times to trigger reload (use only in development)")
		s.o("py-auto-reload-ignore", [str], "ignore the specified module during auto-reload scan")
		s.o(("wsgi-env-behaviour", "wsgi-env-behavior"), str, "set the strategy for allocating/deallocating the WSGI env")
		s.o("start_response-nodelay", True, "send WSGI http headers as soon as possible (PEP violation)")
	return config

def carbon_options():
	config = Config("Carbon")
	with config.section("Carbon", docs = ["Carbon"]) as s:
		s.o("carbon", [str], "push statistics to the specified carbon server")
		s.o("carbon-timeout", int, "set carbon connection timeout in seconds (default 3)")
		s.o("carbon-freq", int, "set carbon push frequency in seconds (default 60)")
		s.o("carbon-id", str, "set carbon id")
		s.o("carbon-no-workers", True, "disable generation of single worker metrics")
		s.o("carbon-max-retry", int, "set maximum number of retries in case of connection errors (default 1)")
		s.o("carbon-retry-delay", int, "set connection retry delay in seconds (default 7)")
	return config

def cgi_options():
	config = Config("CGI")
	with config.section("Config", docs = ["CGI"]) as s:
		s.o("cgi", 'add cgi', "add a cgi mountpoint/directory/script")
		s.o(("cgi-map-helper", "cgi-helper"), 'add cgi maphelper', "add a cgi map-helper")
		s.o("cgi-from-docroot", True, "blindly enable cgi in DOCUMENT_ROOT")
		s.o("cgi-buffer-size", 'set 64bit', "set cgi buffer size")
		s.o("cgi-timeout", int, "set cgi script timeout")
		s.o("cgi-index", [str], "add a cgi index file")
		s.o("cgi-allowed-ext", [str], "cgi allowed extension")
		s.o("cgi-unset", [str], "unset specified environment variables")
		s.o("cgi-loadlib", [str], "load a cgi shared library/optimizer")
		s.o(("cgi-optimize", "cgi-optimized"), True, "enable cgi realpath() optimizer")
		s.o("cgi-path-info", True, "disable PATH_INFO management in cgi scripts")
	return config

def cheaper_options():
	config = Config("Cheaper")
	with config.section("Busyness Cheaper algorithm", docs = ["Cheaper"]) as s:
		s.o("cheaper-busyness-max", long, "set the cheaper busyness high percent limit, above that value worker is considered loaded (default 50)")
		s.o("cheaper-busyness-min", long, "set the cheaper busyness low percent limit, belowe that value worker is considered idle (default 25)")
		s.o("cheaper-busyness-multiplier", long, "set initial cheaper multiplier, worker needs to be idle for cheaper-overload*multiplier seconds to be cheaped (default 10)")
		s.o("cheaper-busyness-penalty", long, "penalty for respawning workers to fast, it will be added to the current multiplier value if worker is cheaped and than respawned back too fast (default 2)")
		s.o("cheaper-busyness-verbose", True, "enable verbose log messages from busyness algorithm")
		s.o("cheaper-busyness-backlog-alert", int, "spawn emergency worker if anytime listen queue is higher than this value (default 33) (Linux only)")
		s.o("cheaper-busyness-backlog-multiplier", long, "set cheaper multiplier used for emergency workers (default 3) (Linux only)")
		s.o("cheaper-busyness-backlog-step", int, "number of emergency workers to spawn at a time (default 1) (Linux only)")
	return config

def erlang_options():
	config = Config("Erlang")
	with config.section("Erlang", docs = ["Erlang"]) as s:
		s.o("erlang", str, "spawn an Erlang c-node")
		s.o("erlang-cookie", str, "set Erlang cookie")
	return config

def fastrouter_options():
	config = Config("Fastrouter")
	with config.section("Fastrouter", docs = ["Fastrouter"]) as s:
		s.o("fastrouter", 'corerouter', "run the fastrouter on the specified port")
		s.o(("fastrouter-processes", "fastrouter-workers"), int, "prefork the specified number of fastrouter processes")
		s.o("fastrouter-zerg", 'corerouter zerg', "attach the fastrouter to a zerg server")
		s.o("fastrouter-use-cache", True, "use uWSGI cache as hostname->server mapper for the fastrouter")
		s.o("fastrouter-use-pattern", 'corerouter use pattern', "use a pattern for fastrouter hostname->server mapping")
		s.o("fastrouter-use-base", 'corerouter use base', "use a base dir for fastrouter hostname->server mapping")
		s.o("fastrouter-fallback", [str], "fallback to the specified node in case of error")
		s.o("fastrouter-use-cluster", True, "load balance to nodes subscribed to the cluster")
		s.o("fastrouter-use-code-string", 'corerouter cs', "use code string as hostname->server mapper for the fastrouter")
		s.o("fastrouter-use-socket", optional('corerouter use socket'), "forward request to the specified uwsgi socket")
		s.o("fastrouter-to", [str], "forward requests to the specified uwsgi server (you can specify it multiple times for load balancing)")
		s.o("fastrouter-gracetime", int, "retry connections to dead static nodes after the specified amount of seconds")
		s.o("fastrouter-events", int, "set the maximum number of concurrent events")
		s.o("fastrouter-quiet", True, "do not report failed connections to instances")
		s.o("fastrouter-cheap", True, "run the fastrouter in cheap mode")
		s.o("fastrouter-subscription-server", 'corerouter ss', "run the fastrouter subscription server on the specified address")
		s.o("fastrouter-timeout", int, "set fastrouter timeout")
		s.o("fastrouter-post-buffering", long, "enable fastrouter post buffering")
		s.o("fastrouter-post-buffering-dir", str, "put fastrouter buffered files to the specified directory")
		s.o(("fastrouter-stats", "fastrouter-stats-server", "fastrouter-ss"), str, "run the fastrouter stats server")
		s.o("fastrouter-harakiri", int, "enable fastrouter harakiri")
	return config


def http_options():
	config = Config("HTTP support")
	with config.section("HTTP", docs = ["HTTP"]) as s:
		s.o("http", 'address', "add an http router/server on the specified address")
		s.o(("http-processes", "http-workers"), int, "set the number of http processes to spawn")
		s.o("http-var", [str], "add a key=value item to the generated uwsgi packet")
		s.o("http-to", [str], "forward requests to the specified node (you can specify it multiple time for lb)")
		s.o("http-zerg", 'corerouter zerg', "attach the http router to a zerg server")
		s.o("http-fallback", [str], "fallback to the specified node in case of error")
		s.o("http-modifier1", int, "set uwsgi protocol modifier1")
		s.o("http-use-cache", True, "use uWSGI cache as key->value virtualhost mapper")
		s.o("http-use-pattern", 'corerouter use pattern', "use the specified pattern for mapping requests to unix sockets")
		s.o("http-use-base", 'corerouter use base', "use the specified base for mapping requests to unix sockets")
		s.o("http-use-cluster", True, "load balance to nodes subscribed to the cluster")
		s.o("http-events", int, "set the number of concurrent http async events")
		s.o("http-subscription-server", 'corerouter ss', "enable the subscription server")
		s.o("http-timeout", int, "set internal http socket timeout")
		s.o("http-manage-expect", True, "manage the Expect HTTP request header")
		s.o("http-keepalive", True, "support HTTP keepalive (non-pipelined) requests (requires backend support)")
		s.o("http-raw-body", True, "blindly send HTTP body to backends (required for WebSockets and Icecast support)")
		s.o("http-use-code-string", 'corerouter cs', "use code string as hostname->server mapper for the http router")
		s.o("http-use-socket", optional('corerouter use socket'), "forward request to the specified uwsgi socket")
		s.o("http-gracetime", int, "retry connections to dead static nodes after the specified amount of seconds")
		s.o("http-quiet", True, "do not report failed connections to instances")
		s.o("http-cheap", True, "run the http router in cheap mode")
		s.o(("http-stats", "http-stats-server", "http-ss"), str, "run the http router stats server")
		s.o("http-harakiri", int, "enable http router harakiri")

	with config.section("HTTPS", docs = ["HTTPS"]) as s:
		s.o("https", 'https config', "add an https router/server on the specified address with specified certificate and key")
		s.o("https-export-cert", True, "export uwsgi variable HTTPS_CC containing the raw client certificate")
		s.o("http-to-https", 'address', "add an HTTP router/server on the specified address and redirect all of the requests to HTTPS")
	return config

def jvm_options():
	config = Config("JVM")
	with config.section("JVM", docs = ["JVM"]) as s:
		s.o("jvm-main-class", str, "load the specified class")
		s.o("jvm-classpath", [str], "add the specified directory to the classpath")
	return config

def lua_options():
	config = Config("Lua")
	
	with config.section("Lua", docs = ["Lua"]) as s:
		s.o("lua", str, "load lua wsapi app")
	
	return config


def nagios_options():
	config = Config("Nagios")
	
	with config.section("Nagios output", docs = ["Nagios"]) as s:
		s.o("nagios", True, "Output Nagios-friendly status check information")
	
	return config


def pam_options():
	config = Config("PAM")
	
	with config.section("PAM", docs = ["PAM"]) as s:
		s.o("pam", str, "set the pam service name to use")
		s.o("pam-user", str, "set a fake user for pam")
	
	return config


def php_options():
	config = Config("PHP")
	
	with config.section("PHP", docs = ["PHP"]) as s:
		s.o(("php-ini", "php-config"), 'php ini', "set php.ini path")
		s.o(("php-ini-append", "php-config-append"), [str], "set php.ini path (append mode)")
		s.o("php-set", [str], "set a php config directive")
		s.o("php-index", [str], "list the php index files")
		s.o("php-docroot", str, "force php DOCUMENT_ROOT")
		s.o("php-allowed-docroot", [str], "list the allowed document roots")
		s.o("php-allowed-ext", [str], "list the allowed php file extensions")
		s.o("php-server-software", str, "force php SERVER_SOFTWARE")
		s.o("php-app", str, "force the php file to run at each request")
		s.o("php-dump-config", True, "dump php config (if modified via --php-set or append options)")
	
	return config


def ping_options():
	config = Config("Ping")
	
	with config.section("Ping", docs = ["Ping"]) as s:
		s.o("ping", str, "ping specified uwsgi host")
		s.o("ping-timeout", int, "set ping timeout")
	
	return config


def perl_options():
	config = Config("Perl (PSGI plugin)")
	
	with config.section("Perl", docs = ["Perl"]) as s:
		s.o("psgi", str, "load a psgi app")
		s.o("perl-no-die-catch", True, "do not catch $SIG{__DIE__}")
		s.o("perl-local-lib", str, "set perl locallib path")
	
	return config


def ruby_options():
	config = Config("Ruby")
	
	with config.section("Ruby", docs = ["Ruby"]) as s:
		s.o("rails", str, "load a Ruby on Rails <= 2.x app")
		s.o("rack", str, "load a Rack app")
		s.o(("ruby-gc-freq", "rb-gc-freq"), int, "set Ruby GC frequency")
		s.o(("rb-require", "ruby-require", "rbrequire", "rubyrequire", "require"), [str], "import/require a Ruby module/script")
		s.o(("shared-rb-require", "shared-ruby-require", "shared-rbrequire", "shared-rubyrequire", "shared-require"), [str], "import/require a Ruby module/script (shared)")
		s.o(("gemset", "rvm"), str, "load the specified gemset (rvm)")
		s.o("rvm-path", [str], "search for rvm in the specified directory")
		s.o("rbshell", optional(True), "run a Ruby/irb shell")
		s.o(("rb-threads", "rbthreads", "ruby-threads"), int, "set the number of Ruby threads to run (Ruby 1.9+)")
	
	return config


def rawrouter_options():
	config = Config("Rawrouter")
	
	with config.section("Rawrouter", docs = ["Rawrouter"]) as s:
		s.o("rawrouter", 'corerouter', "run the rawrouter on the specified port")
		s.o(("rawrouter-processes", "rawrouter-workers"), int, "prefork the specified number of rawrouter processes")
		s.o("rawrouter-zerg", 'corerouter zerg', "attach the rawrouter to a zerg server")
		s.o("rawrouter-use-cache", True, "use uWSGI cache as address->server mapper for the rawrouter")
		s.o("rawrouter-use-pattern", 'corerouter use pattern', "use a pattern for rawrouter address->server mapping")
		s.o("rawrouter-use-base", 'corerouter use base', "use a base dir for rawrouter address->server mapping")
		s.o("rawrouter-fallback", [str], "fallback to the specified node in case of error")
		s.o("rawrouter-use-cluster", True, "load balance to nodes subscribed to the cluster")
		s.o("rawrouter-use-code-string", 'corerouter cs', "use code string as address->server mapper for the rawrouter")
		s.o("rawrouter-use-socket", optional('corerouter use socket'), "forward request to the specified uwsgi socket")
		s.o("rawrouter-to", [str], "forward requests to the specified uwsgi server (you can specify it multiple times for load balancing)")
		s.o("rawrouter-gracetime", int, "retry connections to dead static nodes after the specified amount of seconds")
		s.o("rawrouter-events", int, "set the maximum number of concurrent events")
		s.o("rawrouter-quiet", True, "do not report failed connections to instances")
		s.o("rawrouter-cheap", True, "run the rawrouter in cheap mode")
		s.o("rawrouter-subscription-server", 'corerouter ss', "run the rawrouter subscription server on the spcified address")
		s.o("rawrouter-timeout", int, "set rawrouter timeout")
		s.o(("rawrouter-stats", "rawrouter-stats-server", "rawrouter-ss"), str, "run the rawrouter stats server")
		s.o("rawrouter-harakiri", int, "enable rawrouter harakiri")
	
	return config


def rrdtool_options():
	config = Config("RRDtool")
	
	with config.section("RRDtool", docs = ["RRDtool"]) as s:
		s.o("rrdtool", [str], "collect request data in the specified rrd file")
		s.o("rrdtool-freq", int, "set collect frequency")
		s.o("rrdtool-max-ds", int, "set maximum number of data sources")
	
	return config


def async_options():
	config = Config("Async engines")
	
	with config.section("Greenlet", docs = ["Greenlet"]) as s:
		s.o("greenlet", True, "enable greenlet as suspend engine")
	
	with config.section("Gevent", docs = ["Gevent"]) as s:
		s.o("gevent", int, "a shortcut enabling gevent loop engine with the specified number of async cores and optimal parameters")
	
	with config.section("Stackless", docs = ["Stackless"]) as s:
		s.o("stackless", True, "use stackless as suspend engine")

	with config.section("uGreen", docs = ["uGreen"]) as s:
		s.o("ugreen", True, "enable ugreen coroutine subsystem")
		s.o("ugreen-stacksize", int, "set ugreen stack size in pages")
	
	return config
