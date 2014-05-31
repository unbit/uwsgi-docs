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
        s.o("shared-socket", str, "Create a shared socket for advanced jailing or IPC purposes", help="""Advanced option for plugin writers or special needs. Allows you to create a socket early in the server's startup and use it after privileges drop or jailing. This can be used to bind to privileged (<1024) ports.""")
        s.o("listen", int, "set the socket listen queue size", short_name="l", default="100", help="""
        Every socket has an associated queue where request will be put waiting for a process to became ready to accept them. When this queue is full, requests will be rejected.

        The maximum value is system/kernel dependent.
        """)
        s.o("abstract-socket", True, "force UNIX socket into abstract mode (Linux only)")
        s.o("chmod-socket", o_str, "chmod socket", short_name='C', help="""
        UNIX sockets are filesystem objects that obey UNIX permissions like any other filesystem object.
        You can set the UNIX sockets' permissions with this option if your webserver would otherwise have no access to the uWSGI socket.
        When used without a parameter, the permissions will be set to 666. Otherwise the specified chmod value will be used.""")
        s.o("chown-socket", str, "chown UNIX sockets")
        s.o("umask", str, "set UNIX socket umask")
        s.o("freebind", True, "put socket in freebind mode (Linux only)", help="Allows binding to non-existent network addresses.")
        s.o("map-socket", [str], "map sockets to specific workers", help="""
        As you can bind a uWSGI instance to multiple sockets, you can use this option to map specific workers to specific sockets to implement a sort of in-process Quality of Service scheme.

        .. code-block:: ini

           [uwsgi]
           socket = /tmp/uwsgi0.sock
           socket = /tmp/uwsgi1.sock
           workers = 5
           map-socket = 0:1,2,3
           map-socket = 1:4,5

        This will map workers 1, 2 and 3 to the first socket and 4 and 5 to the second one.

        If you host multiple apps in the same uWSGI instance, you can easily dedicate resources to each of them.

        """)
        s.o(("zeromq", "zmq", "zeromq-socket", "zmq-socket"), str, "create a zeromq pub/sub pair")
        s.o("udp", str, "run the udp server on the specified address", help="Mainly useful for SNMP or shared UDP logging.", docs=["SNMP", "Logging"])
        s.o("reuse-port", True, "enable REUSE_PORT flag on socket to allow multiple instances binding on the same address (BSD only)")
        s.o("http-socket-modifier1", long, "force the specified modifier1 when using HTTP protocol")
        s.o("http-socket-modifier2", long, "force the specified modifier2 when using HTTP protocol")
        s.o("fastcgi-nph-socket", u'add socket', "bind to the specified UNIX/TCP socket using FastCGI protocol (nph mode)")
        s.o("fastcgi-modifier1", long, "force the specified modifier1 when using FastCGI protocol")
        s.o("fastcgi-modifier2", long, "force the specified modifier2 when using FastCGI protocol")
        s.o("scgi-socket", u'add socket', "bind to the specified UNIX/TCP socket using SCGI protocol")
        s.o("scgi-nph-socket", u'add socket', "bind to the specified UNIX/TCP socket using SCGI protocol (nph mode)")
        s.o("scgi-modifier1", long, "force the specified modifier1 when using SCGI protocol")
        s.o("scgi-modifier2", long, "force the specified modifier2 when using SCGI protocol")
        s.o("undeferred-shared-socket", u'add shared socket', "create a shared socket for advanced jailing or ipc (undeferred mode)")
        s.o("raw-socket", u'add socket no defer', "bind to the specified UNIX/TCP socket using RAW protocol")
        s.o("raw-modifier1", long, "force the specified modifier1 when using RAW protocol")
        s.o("raw-modifier2", long, "force the specified modifier2 when using RAW protocol")
        s.o("puwsgi-socket", u'add socket', "bind to the specified UNIX/TCP socket using persistent uwsgi protocol (puwsgi)")

    with config.section("Process Management") as s:
        s.o(("workers", "processes"), int, "Spawn the specified number of workers/processes.", short_name="p", help="""
        Set the number of workers for preforking mode.
        This is the base for easy and safe concurrency in your app. More workers you add, more concurrent requests you can manage.
        Each worker corresponds to a system process, so it consumes memory, choose carefully the right number. You can easily drop your system to its knees by setting a too high value.
        Setting ``workers`` to a ridiculously high number will *not* magically make your application web scale -- quite the contrary.
        """)

        s.o("harakiri", int, "Harakiri timeout in seconds", help="""
        Every request that will take longer than the seconds specified in the harakiri timeout will be dropped and the corresponding worker is thereafter recycled.""")

        s.o("harakiri-verbose", True, "Enable verbose Harakiri mode.", help="""
        When a request is killed by Harakiri you will get a message in the uWSGI log.
        Enabling this option will print additional info (for example, the current syscall will be reported on Linux platforms).
        """)

        s.o(("harakiri-no-arh", "no-harakiri-arh", "no-harakiri-after-req-hook"), True, "Disallow Harakiri killings during after-request hook methods.")
        s.o("mule-harakiri", int, "Set harakiri timeout for mule tasks")
        s.o("master", True, "Enable uWSGI master process", short_name='M')

        s.o("reaper", True, "call waitpid(-1,...) after each request to get rid of zombies", short_name="r", help="""
        Enables reaper mode. After each request the server will call ``waitpid(-1)`` to get rid of zombie processes.
        If you spawn subprocesses in your app and you happen to end up with zombie processes all over the place you can enable this option. (It really would be better if you could fix your application's process spawning usage though.)
        """)

        s.o("max-requests", int, "reload workers after the specified amount of managed requests (avoid memory leaks)", short_name='R', help="""
        When a worker reaches this number of requests it will get recycled (killed and restarted). You can use this option to "dumb fight" memory leaks.
        Also take a look at the ``reload-on-as`` and ``reload-on-rss`` options as they are more useful for memory leaks.

        Beware: The default min-worker-lifetime 60 seconds takes priority over `max-requests`.
        Do not use with benchmarking as you'll get stalls such as `worker respawning too fast !!! i have to sleep a bit (2 seconds)...`

        """)
        s.o("min-worker-lifetime", int, "A worker cannot be destroyed/reloaded unless it has been alive for N seconds (default 60). This is an anti-fork-bomb measure", since="1.9")
        s.o("max-worker-lifetime", int, "Reload workers after this many seconds. Disabled by default.", since="1.9")
        s.o("limit-as", int, "limit process address space (vsz) (in megabytes)", help="""
        Limits the address space usage of each uWSGI (worker) process using POSIX/UNIX ``setrlimit()``.
        For example, ``limit-as 256`` will disallow uWSGI processes to grow over 256MB of address space.
        Address space is the virtual memory a process has access to. It does *not* correspond to physical memory.
        Read and understand this page before enabling this option: http://en.wikipedia.org/wiki/Virtual_memory
        """)

        s.o("limit-nproc", int, "limit the number of spawnable processes")
        s.o("reload-on-as", int, "reload a worker if its address space usage is higher than the specified value (in megabytes)")
        s.o("reload-on-rss", int, "reload a worker if its physical unshared memory is higher than the specified value (in megabytes)")
        s.o("evil-reload-on-as", int, "force the master to reload a worker if its address space is higher than specified megabytes (in megabytes)")
        s.o("evil-reload-on-rss", int, "force the master to reload a worker if its rss memory is higher than specified megabytes (in megabytes)")
        s.o("threads", int, "Run each worker in prethreaded mode with the specified number of threads per worker.\n\nDo not use with ``gevent``.")
        s.o(("thread-stacksize", "threads-stacksize", "thread-stack-size", "threads-stack-size"), int, "set threads stacksize")
        s.o("check-interval", int, "set the interval (in seconds) of master checks", default=1, help="The master process makes a scan of subprocesses, etc. every N seconds. You can increase this time if you need to, but it's DISCOURAGED.")

    with config.section("Process Management - Emperor", docs=["Emperor"]) as s:
        s.o("emperor", [str], "run as the Emperor, using the given configuration method")
        s.o("emperor-freq", int, "Set the Emperor scanning frequency in seconds", default=3)
        s.o("emperor-pidfile", str, "write the Emperor pid in the specified file")
        s.o("emperor-tyrant", True, "put the Emperor in Tyrant (multi-user hosting) mode")
        s.o(("emperor-stats", "emperor-stats-server"), str, "run the imperial bureau of statistics on the given address:port")
        s.o("early-emperor", True, "spawn the emperor before jailing and privilege dropping")
        s.o("emperor-broodlord", int, "run the emperor in Broodlord mode", docs=["Broodlord"])
        s.o("emperor-throttle", int, "set throttling level (in milliseconds) for bad behaving vassals", default=1000)
        s.o("emperor-max-throttle", int, "set max throttling level (in milliseconds) for badly behaving vassals (default 3 minutes)", default=180000)
        s.o("emperor-magic-exec", True, "prefix vassals config files with exec as s:// if they have the executable bit")
        s.o(("imperial-monitor-list", "imperial-monitors-list"), True, "list enabled imperial monitors")
        s.o("vassals-inherit", [str], "Add given config templates to vassals' config.\n\nThis works by passing the ``inherit`` option when starting each vassal (which differs from the ``include`` option in that ``inherit`` *will not* replace placeholders etc.).")
        s.o("vassals-include", [str], "Add given config templates to vassals' config.\n\nThis works by passing the ``include`` option when starting each vassal (which differs from the ``inherit`` option in that ``include`` *will* replace placeholders etc.).")
        s.o("vassals-start-hook", str, "run the specified command before each vassal starts")
        s.o("vassals-stop-hook", str, "run the specified command after vassal's death")
        s.o("vassal-sos-backlog", int, "ask emperor for sos if backlog queue has more items than the value specified")
        s.o("heartbeat", int, "(Vassal option) Announce vassal health to the emperor every N seconds")
        s.o("emperor-required-heartbeat", int, "set the Emperor tolerance about heartbeats", help="When a vassal asks for 'heartbeat mode' the emperor will also expect a 'heartbeat' at least every <secs> seconds.", default=30)
        s.o("auto-snapshot", o_int, "Automatically make workers snapshot after reload", docs=["Snapshot"])
        s.o("reload-mercy", int, "set the maximum time (in seconds) a worker can take to reload/shutdown", help="For example ``reload-mercy 8`` would brutally kill every worker that will not terminate itself within 8 seconds during graceful reload")

    with config.section("Process Management - Zerg", docs=["Zerg"]) as s:
        s.o("zerg", [str], "attach to a zerg server")
        s.o("zerg-fallback", True, "fallback to normal sockets if the zerg server is not available")
        s.o("zerg-server", str, "enable the zerg server on the specified UNIX socket")
        s.o(("zergpool", "zerg-pool"), [str], "start a zergpool on specified address for specified address (zergpool plugin)")


    with config.section("Debugging") as s:
        s.o("backtrace-depth", int, "Set backtrace depth")
        s.o("memory-report", True, "enable memory usage report", short_name="m", help="When enabled, diagnostic information about RSS and address space usage will be printed in the request log.")
        s.o("profiler", str, "enable the specified profiler")
        s.o("dump-options", True, "dump the full list of available options")
        s.o("show-config", True, "show the current config reformatted as ini")
        s.o("print", str, "simple print (for your convenience)")
        s.o("cflags", True, "report uWSGI CFLAGS (useful for building external plugins)")
        s.o("version", True, "print uWSGI version")
        s.o("allowed-modifiers", str, "comma separated list of allowed modifiers for clients", help="``allowed-modifiers 0,111`` would allow access to only the WSGI handler and the cache handler.")
        s.o("connect-and-read", "str", "connect to a socket and wait for data from it")

    with config.section("Configuration", docs=["Configuration"]) as s:
        s.o("strict", True, "Enable strict configuration parsing. If any unknown option is encountered in a configuration file, an error is shown and uWSGI quits.\n\nTo use placeholder variables when using strict mode, use the ``set-placeholder`` option.")
        s.o("set", str, "Set a configuration option. This option was created to work around a specific problem with commandline options on Solaris and should not normally need to be used.")
        s.o("set-placeholder", str, "Set a placeholder variable. The value of this option should be in the form ``placeholder=value``. This option can be to set placeholders when the ``strict`` option is enabled.", since="1.9.18")
        s.o("declare-option", str, "Declare a new custom uWSGI option")
        s.o("inherit", str, u"Use the specified file as configuration template. The file type of the included file is automatically detected based on filename extension.\n\nNote that environment variables, external file includes and placeholders are *not* expanded inside the inherited configuration. Magic variables (*e.g.* ``%n``) are expanded normally.", docs=["ParsingOrder"])
        s.o("include", str, u"Include the specified file as if its configuration entries had been declared here. The file type of the included file is automatically detected based on filename extension.", since="1.3")
        s.o(("plugins", "plugin"), [str], "load uWSGI plugins (comma-separated)")
        s.o(("plugins-dir", "plugin-dir"), [str], "add a directory to uWSGI plugin search path")
        s.o(("plugins-list", "plugin-list"), True, "list enabled plugins")
        s.o("autoload", True, "try to automatically load plugins when unknown options are found")
        s.o("dlopen", str, "blindly load a shared library")
        s.o("ini", int, "load config from ini file")
        s.o(("xml", "xmlconfig"), str, "Load XML file as configuration", short_name="x")
        s.o(("yaml", "yal"), str, "load config from yaml file", short_name="y")
        s.o(("json", "js"), str, "load config from json file", short_name="j")
        s.o(("sqlite3", "sqlite"), int, "load config from sqlite3 db")
        s.o("ldap", int, "load configuration from ldap server", docs=["LDAP"])
        s.o("ldap-schema", True, "dump uWSGI ldap schema", docs=["LDAP"])
        s.o("ldap-schema-ldif", True, "dump uWSGI ldap schema in ldif format", docs=["LDAP"])

    with config.section("Config logic", docs=["ConfigLogic"]) as s:
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

    with config.section("Logging", docs=["Logging"]) as s:
        s.o("disable-logging", True, "disable request logging", short_name="L", help="When enabled, only uWSGI internal messages and errors are logged.")
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
        s.o("log-syslog", o_str, "Log to syslog", help="Passing a parameter makes uwsgi use the parameter as program-name in the syslog entry header.")
        s.o("log-socket", str, "Send logs to the specified socket")
        s.o("logger", [str], "Set/append a logger")
        s.o(("logger-list", "loggers-list"), True, "list enabled loggers")
        s.o("threaded-logger", True, "offload log writing to a thread")
        s.o("log-drain", ["regexp"], "drain (do not show) log lines matching the specified regexp")
        s.o("log-zeromq", str, "send logs to a ZeroMQ server")
        s.o("log-master", True, "delegate logging to master process", help="Delegate the write of the logs to the master process (this will put all of the logging I/O to a single process). Useful for system with advanced I/O schedulers/elevators.")
        s.o("log-master-bufsize", int, "Set the buffer size for the master logger. Log messages larger than this will be truncated.")
        s.o("log-reopen", True, "reopen log after reload")
        s.o("log-truncate", True, "truncate log on startup")
        s.o("log-maxsize", int, "set maximum logfile size")
        s.o("log-backupname", str, "set logfile name after rotation")
        s.o(("log-prefix", "logdate", "log-date"), o_str, "prefix log lines with date (without argument) or a strftime string")
        s.o("log-zero", True, "log responses without body (zero response size)")
        s.o("log-slow", int, "log requests slower than the specified number of milliseconds")
        s.o("log-4xx", True, "log requests with a 4xx response")
        s.o("log-5xx", True, "log requests with a 5xx response")
        s.o("log-big", int, "log requestes bigger than the specified size in bytes")
        s.o("log-sendfile", True, "log sendfile requests")
        s.o("log-micros", True, "report response time in microseconds instead of milliseconds")
        s.o("log-x-forwarded-for", True, "use the ip from X-Forwarded-For header instead of REMOTE_ADDR. Used when uWSGI is run behind multiple proxies.")
        s.o(("stats", "stats-server"), str, "enable the stats server on the specified address")
        s.o("ssl-verbose", True, "be verbose about SSL errors")
        s.o("snmp", [str], "Enable the embedded SNMP server", docs=["SNMP"])
        s.o("snmp-community", str, "Set the SNMP community string")

    with config.section("Alarms", docs=["AlarmSubsystem"]) as s:
        s.o("alarm", [str], "Create a new alarm. Syntax: <alarm> <plugin:args>")
        s.o("alarm-freq", int, "tune the alarm anti-loop system (default 3 seconds)")
        s.o("log-alarm", [str], "raise the specified alarm when a log line matches the specified regexp, syntax: <alarm>[,alarm...] <regexp>")
        s.o(("alarm-list", "alarms-list"), True, "list enabled alarms")


    with config.section("uWSGI Process") as s:
        s.o("daemonize", "logfile", "Daemonize uWSGI and write messages into given log file or UDP socket address", docs=["Logging"])
        s.o("daemonize2", "logfile", "Daemonize uWSGI after loading application, write messages into given log file or UDP socket address", docs=["Logging"])
        s.o("stop", "pidfile", "send the stop (SIGINT) signal to the instance described by the pidfile", docs=["Management"])
        s.o("reload", "pidfile", "send the reload (SIGHUP) signal to the instance described by the pidfile", docs=["Management"])
        s.o("pause", "pidfile", "send the pause (SIGTSTP) signal to the instance described by the pidfile", docs=["Management"])
        s.o("suspend", "pidfile", "send the suspend (SIGTSTP) signal to the instance described by the pidfile", docs=["Management"])
        s.o("resume", "pidfile", "send the resume (SIGTSTP) signal to the instance described by the pidfile", docs=["Management"])
        s.o("auto-procname", True, "Automatically set process name to something meaningful", help="Generated process names may be 'uWSGI Master', 'uWSGI Worker #', etc.")
        s.o("procname-prefix", str, "Add prefix to process names")
        s.o("procname-prefix-spaced", str, "Add spaced prefix to process names")
        s.o("procname-append", str, "Append string to process names")
        s.o("procname", str, "Set process name to given value")
        s.o("procname-master", str, "Set master process name to given value")
        s.o("pidfile", str, "create pidfile (before privileges drop)")
        s.o("pidfile2", str, "create pidfile (after privileges drop)")
        s.o("chroot", str, "chroot() to the specified directory")
        s.o("uid", "username|uid", "setuid to the specified user/uid")
        s.o("gid", "groupname|gid", "setgid to the specified group/gid")
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
        s.o("cgroup", [str], "put the processes in the specified cgroup (Linux only)", docs=["Cgroups"])
        s.o("cgroup-opt", [str], "set value in specified cgroup option", docs=["Cgroups"])
        s.o(("namespace", "ns"), str, "run in a new namespace under the specified rootfs", docs=["Namespaces"])
        s.o("namespace-keep-mount", "<mount>[:<jailed-mountpoint>]", "keep the specified mountpoint in your namespace, optionally renaming it", docs=["Namespaces"])
        s.o(("namespace-net", "ns-net"), str, "add network namespace")
        s.o("forkbomb-delay", int, "sleep for the specified number of seconds when a forkbomb is detected")
        s.o("binary-path", str, "force binary path", help="If you do not have uWSGI in the system path you can force its path with this option to permit the reloading system and the Emperor to easily find the binary to execute.")
        s.o("privileged-binary-patch", str, "patch the uwsgi binary with a new command (before privileges drop)")
        s.o("unprivileged-binary-patch", str, "patch the uwsgi binary with a new command (after privileges drop)")
        s.o("privileged-binary-patch-arg", str, "patch the uwsgi binary with a new command and arguments (before privileges drop)")
        s.o("unprivileged-binary-patch-arg", str, "patch the uwsgi binary with a new command and arguments (after privileges drop)")
        s.o("async", int, "enable async mode with specified cores", docs=["Async"])
        s.o("max-fd", int, "set maximum number of file descriptors (requires root privileges)")
        s.o("master-as-root", True, "leave master process running as root")

    with config.section("Miscellaneous") as s:
        s.o("thunder-lock", True, "serialize accept() usage (if possibie)")
        s.o("skip-zero", True, "skip check of file descriptor 0")
        s.o("need-app", True, "exit if no app can be loaded")
        s.o("exit-on-reload", True, "force exit even if a reload is requested")
        s.o("die-on-term", True, "exit instead of brutal reload on SIGTERM")
        s.o("no-fd-passing", True, "disable file descriptor passing")
        s.o("single-interpreter", True, "do not use multiple interpreters (where available)", short_name="i", help="""
        Some of the supported languages (such as Python) have the concept of "multiple interpreters".
        This feature allows you to isolate apps living in the same process. If you do not want this kind of feature use this option.
        """)
        s.o("max-apps", int, "set the maximum number of per-worker applications")
        s.o("sharedarea", int, "create a raw shared memory area of specified number of pages", short_name="A", docs=["SharedArea"], help="This enables the SharedArea. This is a low level shared memory. If you want a more usable/user-friendly system look at the caching framework.")
        s.o("cgi-mode", True, "force CGI-mode for plugins supporting it", short_name="c", help="When enabled, responses generated by uWSGI will not be HTTP responses, but CGI ones; namely, the ``Status:`` header will be added.")
        s.o("buffer-size", int, "Set the internal buffer size for uwsgi packet parsing.", short_name="b", default=4096, help="""If you plan to receive big requests with lots of headers you can increase this value up to 64k (65535).""")
        s.o("enable-threads", True, "enable threads", short_name="T", help="""
        Enable threads in the embedded languages. This will allow to spawn threads in your app.

        .. warning::

           Threads will simply *not work* if this option is not enabled. There will likely be no error, just no execution of your thread code.

        """)
        s.o(("signal-bufsize", "signals-bufsize"), int, "set buffer size for signal queue")
        s.o("socket-timeout", int, "Set internal sockets timeout in seconds", short_name='z', default=4)
        s.o("max-vars", int, "Set the amount of internal iovec/vars structures for uwsgi clients (web servers, etc.)", short_name='v', help="This is only a security measure you will probably never need to touch.")
        s.o("weight", int, "weight of the instance (used by clustering/lb/subscriptions)")
        s.o("auto-weight", int, "set weight of the instance (used by clustering/lb/subscriptions) automatically")
        s.o("no-server", True, "initialize the uWSGI server but exit as soon as the initialization is complete (useful for testing)")
        s.o("command-mode", True, "force command mode")
        s.o("no-defer-accept", True, "disable deferred ``accept()`` on sockets", help="by default (where available) uWSGI will defer the accept() of requests until some data is sent by the client (this is a security/performance measure). If you want to disable this feature for some reason, specify this option.")
        s.o("so-keepalive", True, "enable TCP KEEPALIVEs")
        s.o("never-swap", True, "lock all memory pages avoiding swapping")
        s.o("ksm", [int], "enable Linux KSM")
        s.o("touch-reload", [str], "reload uWSGI if the specified file or directory is modified/touched")
        s.o("touch-logrotate", [str], "trigger logrotation if the specified file is modified/touched")
        s.o("touch-logreopen", [str], "trigger log reopen if the specified file is modified/touched")
        s.o("propagate-touch", True, "over-engineering option for system with flaky signal mamagement")
        s.o("no-orphans", True, "automatically kill workers if master dies (can be dangerous for availability)")
        s.o("prio", int, "set processes/threads priority (``nice``) value.")
        s.o("cpu-affinity", "number of cores for each worker (Linux only)", "set CPU affinity", help="""
        Set the number of cores (CPUs) to allocate to each worker process.

        For example

        * With 4 workers, 4 CPUs and ``cpu-affinity`` is 1, each worker is allocated one CPU.
        * With 4 workers, 2 CPUs and ``cpu-affinity`` is 1, workers get one CPU each (0; 1; 0; 1).
        * With 4 workers, 4 CPUs and ``cpu-affinity`` is 2, workers get two CPUs each in a round-robin fashion (0, 1; 2, 3; 0, 1; 2; 3).
        * With 8 workers, 4 CPUs and ``cpu-affinity`` is 3, workers get three CPUs each in a round-robin fashion (0, 1, 2; 3, 0, 1; 2, 3, 0; 1, 2, 3; 0, 1, 2; 3, 0, 1; 2, 3, 0; 1, 2, 3).

        """)
        s.o("remap-modifier", str, "remap request modifier from one id to another (old-id:new-id)")
        s.o("env", str, "set environment variable (key=value)")
        s.o("unenv", str, "set environment variable (key)")
        s.o("close-on-exec", True, "set close-on-exec on sockets (could be required for spawning processes in requests)")
        s.o("mode", str, "set uWSGI custom mode", help="Generic `mode` option that is passed down to applications as ``uwsgi.mode`` (or similar for other languages)")
        s.o("vacuum", True, "try to remove all of the generated files/sockets (UNIX sockets and pidfiles) upon exit")
        s.o("cron", str, "Add a cron task")
        s.o("worker-exec", str, "Run the specified command as worker instead of uWSGI itself.", help="""
        This could be used to run a PHP FastCGI server pool::

            /usr/bin/uwsgi --workers 4 --worker-exec /usr/bin/php53-cgi

        """)
        s.o("attach-daemon", str, "Attach a command/daemon to the master process (the command has to remain in foreground)", help="""
        This will allow the uWSGI master to control/monitor/respawn this process.

        A typical usage is attaching a ``memcached`` instance::

            [uwsgi]
            master = true
            attach-daemon = memcached

        """)
        s.o("smart-attach-daemon", "pidfile", "Attach a command/daemon to the master process managed by a pidfile (the command must daemonize)")
        s.o("smart-attach-daemon2", "pidfile", "Attach a command/daemon to the master process managed by a pidfile (the command must NOT daemonize)")

    with config.section("Locks", docs=["Locks"]) as s:
        s.o("locks", int, "create the specified number of shared locks")
        s.o("lock-engine", str, "set the lock engine")
        s.o("ftok", str, "set the ipcsem key via ftok() for avoiding duplicates")
        s.o("flock", str, "lock the specified file before starting, exit if locked")
        s.o("flock-wait", str, "lock the specified file before starting, wait if locked")
        s.o("flock2", str, "lock the specified file after logging/daemon setup, exit if locked")
        s.o("flock-wait2", str, "lock the specified file after logging/daemon setup, wait if locked")

    with config.section("Cache", docs=["Caching"]) as s:
        s.o("cache", int, "create a shared cache containing given elements")
        s.o("cache-blocksize", int, "Set the cache block size in bytes. It's a good idea to use a multiple of 4096 (common memory page size).", default=65536)
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
        s.o("spooler-external", str, "map spooler requests to a spooler directory, but do not start a spooler (spooling managed by external instance)")
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
        s.o("lazy", True, "set lazy mode (load apps in workers instead of master)", help="This option may have memory usage implications as Copy-on-Write semantics can not be used.\nWhen ``lazy`` is enabled, only workers will be reloaded by uWSGI's reload signals; the master will remain alive. As such, uWSGI configuration changes are not picked up on reload by the master.")
        s.o("lazy-apps", True, "load apps in each worker instead of the master", help="This option may have memory usage implications as Copy-on-Write semantics can not be used.\nUnlike ``lazy``, this only affects the way applications are loaded, not master's behavior on reload.")
        s.o("cheap", True, "set cheap mode (spawn workers only after the first request)")
        s.o("cheaper", int, "set cheaper mode (adaptive process spawning)", help="""This an advanced `cheap` mode. This will only spawn <n> workers on startup and will use various (pluggable) algorithms to implement adaptive process spawning.""")
        s.o("cheaper-initial", int, "set the initial number of processes to spawn in cheaper mode")
        s.o("cheaper-algo", str, "choose to algorithm used for adaptive process spawning)")
        s.o("cheaper-step", int, "number of additional processes to spawn at each overload")
        s.o("cheaper-overload", int, "increase workers after specified overload")
        s.o(("cheaper-algo-list", "cheaper-algos-list", "cheaper-list"), True, "list enabled 'cheaper' algorithms")
        s.o("idle", int, "set idle mode (put uWSGI in cheap mode after inactivity)")
        s.o("die-on-idle", True, "shutdown uWSGI when idle")
        s.o("mount", "/mountpoint=/app/path", "load application under mountpoint", help="Example: ``mount /pinax=/var/www/pinax/deploy/pinax.wsgi``")
        s.o("worker-mount", [str], "load application under mountpoint in the specified worker or after workers spawn")
        s.o("grunt", True, "enable grunt mode (in-request fork)") # TODO: Undocumented.

    with config.section("Request handling") as s:
        s.o("limit-post", int, "limit request body (bytes) based on the ``CONTENT_LENGTH`` uwsgi var.")
        s.o("post-buffering", int, "enable post buffering past N bytes", help="""
        Enables HTTP body buffering. uWSGI will save to disk all HTTP bodies larger than the limit specified.
        This option is required and auto-enabled for Ruby Rack applications as they require a rewindable input stream.
        """)
        s.o("post-buffering-bufsize", int, "set buffer size for read() in post buffering mode", help="This is an advanced option you probably won't need to touch.")
        s.o("upload-progress", str, "enable creation of .json files in the specified directory during a file upload", help="""
        Enable the embedded upload progress system.

        Pass the name of a directory where uWSGI has write permissions into.

        For every upload with a ``X-Progress-ID`` query string ("GET") parameter, a JSON file will be written to this directory containing the status of the upload.
        AJAX calls can then be used to read these files.

        For instance, when ``upload-progress`` is set to ``/var/www/progress`` the user uploads a file to the URL::

          /upload?X-Progress-ID=550e8400-e29b-41d4-a716-446655440000

        uWSGI find ``X-Progress-ID`` in the query string and create a file called :file:`/var/www/progress/550e8400-e29b-41d4-a716-446655440000.js` containing something like::

          {"state": "uploading", "received": 170000, "size": 300000}

        If :file:`/var/www/progress` has been mapped to the ``/progress`` path in your web server, you can then request this file at ``/progress/550e8400-e29b-41d4-a716-446655440000.js``.

        It's likely that your web server supports similar functionality (Nginx does, at least), but the uWSGI implementation is ostensibly more controllable and hackable.
        """)
        s.o("no-default-app", True, "do not fallback to default app", help="""
        By default, when uWSGI does not find a corresponding app for the specified ``SCRIPT_NAME`` variable, it will use the default app
        (most of the time the app mounted under /). Enabling this option will return an error in case of unavailable app.
        """)
        s.o("manage-script-name", True, "automatically rewrite SCRIPT_NAME and PATH_INFO", help="If for some reason your webserver cannot manage ``SCRIPT_NAME`` on its own you can force uWSGI to rebuild the ``PATH_INFO`` variable automatically from it.")
        s.o("ignore-script-name", True, "ignore SCRIPT_NAME")
        s.o("catch-exceptions", True, "report exception as HTTP output", help="""
        .. warning::

           This option is heavily discouraged as it is a definite security risk.

        """)
        s.o("reload-on-exception", True, "reload a worker when an exception is raised")
        s.o("reload-on-exception-type", [str], "reload a worker when a specific exception type is raised")
        s.o("reload-on-exception-value", [str], "reload a worker when a specific exception value is raised")
        s.o("reload-on-exception-repr", [str], "reload a worker when a specific exception type+value (language-specific) is raised")
        s.o("add-header", [str], "automatically add HTTP headers to response")
        s.o("vhost", True, "enable virtualhosting mode (based on SERVER_NAME variable)", docs=["VirtualHosting"])
        s.o("vhost-host", True, "enable virtualhosting mode (based on HTTP_HOST variable)", docs=["VirtualHosting"], help="By default the virtualhosting mode use the SERVER_NAME variable as the hostname key. If you want to use the HTTP_HOST one (corresponding to the Host: header) add this option")

    with config.section("Clustering") as s:
        s.o("multicast", str, "subscribe to specified multicast group. internal option, usable by third party plugins.")
        s.o("multicast-ttl", int, "set multicast ttl")
        s.o("cluster", str, "join specified uWSGI cluster")
        s.o("cluster-nodes", "address:port", "get nodes list from the specified cluster without joining it.", help="This list is used internally by the uwsgi load balancing api.")
        s.o("cluster-reload", "address:port", "send a graceful reload message to the cluster")
        s.o("cluster-log", "address:port", "send a log line to the cluster", help="For instance, ``--cluster-log \"Hello, world!\"`` will print that to each cluster node's log file.")

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

    with config.section("Static files", refname="OptionsStatic") as s:
        s.o(("static-check", "check-static"), [str], "check for static files in the specified directory", help="""
        Specify a directory that uWSGI will check before passing control to a specific handler.

        uWSGI will check if the requested ``PATH_INFO`` has a file correspondence in this directory and serve it.

        For example, with ``check-static /var/www/example.com``, uWSGI will check if :file:`/var/www/example.com/foo.png` exists and directly serve it using `sendfile()` (or another configured method).
        """)
        s.o("check-static-docroot", True, "check for static files in the requested DOCUMENT_ROOT")
        s.o("static-map", [str], "map mountpoint to static directory (or file)", help="Whenever a PATH_INFO starts with one of the configured resources, uWSGI will serve the file as a static file.")
        s.o("static-map2", [str], "map mountpoint to static directory (or file), completely appending the requested resource to the docroot")
        s.o("static-skip-ext", [str], "skip specified extension from staticfile checks")
        s.o("static-index", [str], "search for specified file if a directory is requested", help="With ``static-index=index.html``, if the client asks for ``/doc/`` then uWSGI will check for ``/doc/index.html`` and if it exists it will be served to the client.")
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
        s.o("file-serve-mode", str, "set static file serving mode (x-sendfile, nginx, ...)", help="""
        Set the static serving mode:

        * ``x-sendfile`` will use the X-Sendfile header supported by Apache, Cherokee, lighttpd
        * ``x-accel-redirect`` will use the X-Accel-Redirect header supported by Nginx

        By default the `sendfile()` syscall is used.
        """)

        s.o("check-cache", True, "check for response data in the cache based on PATH_INFO")

    with config.section("Clocks") as s:
        s.o("clock", str, "set a clock source")
        s.o(("clock-list", "clocks-list"), True, "list enabled clocks")

    with config.section("Loop engines") as s:
        s.o("loop", str, "select the uWSGI loop engine (advanced)", docs=["LoopEngine"])
        s.o(("loop-list", "loops-list"), True, "list enabled loop engines")

    return config


def python_options():
    config = Config("Python")

    with config.section("Python", docs=["Python"]) as s:
        s.o(("wsgi-file", "file"), str, "load .wsgi file as the Python application")
        s.o("eval", str, "evaluate Python code as WSGI entry point")
        s.o(("module", "wsgi"), str, "load a WSGI module as the application. The module (sans ``.py``) must be importable, ie. be in ``PYTHONPATH``.", short_name="w")
        s.o("callable", str, "set default WSGI callable name", default="application")
        s.o("test", str, "test a module import", short_name="J")
        s.o(("home", "virtualenv", "venv", "pyhome"), str, "set PYTHONHOME/virtualenv", short_name="H", docs=["Virtualenv"])
        s.o(("py-programname", "py-program-name"), str, "set python program name")
        s.o(("pythonpath", "python-path", "pp"), ['directory/glob'], "add directory (or an .egg or a glob) to the Python search path. This can be specified up to 64 times.")
        s.o("pymodule-alias", [str], "add a python alias module", docs=["PyModuleAlias"])
        s.o("post-pymodule-alias", [str], "add a python module alias after uwsgi module initialization")
        s.o(("import", "pyimport", "py-import", "python-import"), [str], "import a python module")
        s.o(("shared-import", "shared-pyimport", "shared-py-import", "shared-python-import"), [str], "import a python module in all of the processes")
        s.o(("spooler-import", "spooler-pyimport", "spooler-py-import", "spooler-python-import"), [str], "import a python module in the spooler")
        s.o("pyargv", str, "manually set ``sys.argv`` for python apps.", help="``pyargv=\"one two three\"`` will set ``sys.argv`` to ``('one', 'two', 'three')``.")
        s.o("optimize", int, "set python optimization level (this may be dangerous for some apps)", short_name="O")
        s.o("paste", str, "load a paste.deploy config file", docs=["PythonPaste"])
        s.o("paste-logger", True, "enable paste fileConfig logger")
        s.o("web3", str, "load a web3 app")
        s.o("pump", str, "load a pump app")
        s.o("wsgi-lite", str, "load a wsgi-lite app")
        s.o("pecan", str, "Load a pecan config file.", docs=["PythonPecan"])
        s.o("ini-paste", 'paste .INI', "load a paste.deploy config file containing uwsgi section")
        s.o("ini-paste-logged", 'paste .INI', "load a paste.deploy config file containing uwsgi section (load loggers too)")
        s.o("reload-os-env", True, "Force reloading ``os.environ`` at each request")
        s.o("no-site", True, "Do not import the ``site`` module while initializing Python. This is usually only required for dynamic virtualenvs. If in doubt, do not enable.")
        s.o("pyshell", True, "Run an interactive Python shell in the uWSGI environment")
        s.o("pyshell-oneshot", True, "Run an interactive Python shell in the uWSGI environment (one-shot variant)")
        s.o(("python", "py", "pyrun"), '.py file', "Run a Python script in the uWSGI environment")
        s.o("py-tracebacker", str, "enable the uWSGI Python tracebacker")
        s.o(("py-auto-reload", "py-autoreload", "python-auto-reload", "python-autoreload"), int, "Monitor Python modules' modification times to trigger reload (use only in development)")
        s.o("py-auto-reload-ignore", [str], "ignore the specified module during auto-reload scan")
        s.o(("wsgi-env-behaviour", "wsgi-env-behavior"), str, "set the strategy for allocating/deallocating the WSGI env")
        s.o("start_response-nodelay", True, "send WSGI http headers as soon as possible (PEP violation)")
        s.o("python-version", True, "report python version")
    return config

def pypy_plugin_options():
    config = Config("PyPy")

    with config.section("PyPy", docs=[]) as s:
        s.o("pypy-lib", str, "set the path/name of the pypy library")
        s.o("pypy-setup", str, "set the path of the python setup script")
        s.o("pypy-home", str, "set the home of pypy library")
        s.o("pypy-wsgi", str, "load a WSGI module")
        s.o("pypy-wsgi-file", str, "load a WSGI/mod_wsgi file")
        s.o("pypy-eval", [str], "evaluate pypy code before fork()")
        s.o("pypy-eval-post-fork", [str], "evaluate pypy code soon after fork()")
        s.o("pypy-exec", [str], "execute pypy code from file before fork()")
        s.o("pypy-exec-post-fork", [str], "execute pypy code from file soon after fork()")
        s.o(("pypy-pp", "pypy-python-path", "pypy-pythonpath"), [str], "add an item to the pythonpath")

    return config

def carbon_options():
    config = Config("Carbon")
    with config.section("Carbon", docs=["Carbon"]) as s:
        s.o("carbon", ["host:port"], "push statistics to the specified carbon server/port")
        s.o("carbon-timeout", int, "set Carbon connection timeout in seconds", default=3)
        s.o("carbon-freq", int, "set Carbon push frequency in seconds", default=60)
        s.o("carbon-id", str, "set the identifier for Carbon metrics (by default the first uWSGI socket name)")
        s.o("carbon-no-workers", True, "disable generation of single worker metrics")
        s.o("carbon-max-retry", int, "set maximum number of retries in case of connection errors (default 1)")
        s.o("carbon-retry-delay", int, "set connection retry delay in seconds (default 7)")
        s.o("carbon-root", str, "set carbon metrics root node (default 'uwsgi')")
        s.o("carbon-hostname-dots", str, "set char to use as a replacement for dots in hostname (dots are not replaced by default)")
        s.o(("carbon-name-resolve", "carbon-resolve-names"), True, "allow using hostname as carbon server address (default disabled)")
        s.o("carbon-idle-avg", str, "average values source during idle period (no requests), can be 'last', 'zero', 'none' (default is last)")
        s.o("carbon-use-metrics", True, "don't compute all statistics, use metrics subsystem data instead (warning! key names will be different)")

    return config


def cgi_options():
    config = Config("CGI")
    with config.section("CGI", docs=["CGI"]) as s:
        s.o("cgi", '[mountpoint=]script', "Add a CGI directory/script with optional mountpoint (URI prefix)")
        s.o(("cgi-map-helper", "cgi-helper"), 'extension=helper-executable', "Add a cgi helper to map an extension into an executable.")
        s.o("cgi-from-docroot", True, "Blindly enable cgi in DOCUMENT_ROOT")
        s.o("cgi-buffer-size", int, "Set the CGI buffer size")
        s.o("cgi-timeout", int, "set CGI script timeout")
        s.o("cgi-index", [str], "add a CGI index file")
        s.o("cgi-allowed-ext", [str], "Allowed extensions for CGI")
        s.o("cgi-unset", [str], "unset specified environment variables before running CGI executable")
        s.o("cgi-loadlib", [str], "load a CGI shared library/optimizer")
        s.o(("cgi-optimize", "cgi-optimized"), True, "enable CGI realpath() optimizer")
        s.o("cgi-path-info", True, "Disable PATH_INFO management in CGI scripts")
    return config


def cheaper_options():
    config = Config("Cheaper")
    with config.section("Busyness Cheaper algorithm", docs=["Cheaper"]) as s:
        s.o("cheaper-busyness-max", long, "set the cheaper busyness high percent limit, above that value worker is considered loaded (default 50)")
        s.o("cheaper-busyness-min", long, "set the cheaper busyness low percent limit, belowe that value worker is considered idle (default 25)")
        s.o("cheaper-busyness-multiplier", long, "set initial cheaper multiplier, worker needs to be idle for cheaper-overload*multiplier seconds to be cheaped (default 10)")
        s.o("cheaper-busyness-penalty", long, "penalty for respawning workers to fast, it will be added to the current multiplier value if worker is cheaped and than respawned back too fast (default 2)")
        s.o("cheaper-busyness-verbose", True, "enable verbose log messages from busyness algorithm")
        s.o("cheaper-busyness-backlog-alert", int, "spawn emergency worker if anytime listen queue is higher than this value (default 33) (Linux only)")
        s.o("cheaper-busyness-backlog-multiplier", long, "set cheaper multiplier used for emergency workers (default 3) (Linux only)")
        s.o("cheaper-busyness-backlog-step", int, "number of emergency workers to spawn at a time (default 1) (Linux only)")
        s.o("cheaper-busyness-backlog-nonzero", long, "spawn emergency worker(s) if backlog is > 0 for more then N seconds (default 60)")
    return config

def curl_cron_config():
    config = Config("curl_cron")
    
    with config.section("curl_cron", docs = []) as s:
        s.o(("curl-cron", "cron-curl"), u'add cron curl', "add a cron task invoking the specified url via CURL")
        s.o(("legion-curl-cron", "legion-cron-curl", "curl-cron-legion", "cron-curl-legion"), u'add legion cron curl', "add a cron task invoking the specified url via CURL runnable only when the instance is a lord of the specified legion")
    
    return config

def dumb_config():
    config = Config("dumb")
    
    with config.section("dumb", docs = []) as s:
        s.o("dumbloop-modifier1", int, "set the modifier1 for the code_string")
        s.o("dumbloop-code", str, "set the script to load for the code_string")
        s.o("dumbloop-function", str, "set the function to run for the code_string")
    
    return config


def erlang_options():
    config = Config("Erlang")
    with config.section("Erlang", docs=["Erlang"]) as s:
        s.o("erlang", str, "spawn an Erlang c-node")
        s.o("erlang-cookie", str, "set Erlang cookie")
    return config


def fastrouter_options():
    config = Config("Fastrouter")
    with config.section("Fastrouter", docs=["Fastrouter"]) as s:
        s.o("fastrouter", 'address:port', "run the fastrouter (uwsgi protocol proxy/load balancer) on the specified address:port")
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
        s.o("fastrouter-events", int, "set the maximum number of concurrent events the fastrouter can return in one cycle")
        s.o("fastrouter-quiet", True, "do not report failed connections to instances")
        s.o("fastrouter-cheap", True, "run the fastrouter in cheap mode (do not respond to requests unless a node is available)")
        s.o("fastrouter-subscription-slot", u'deprecated', "*** deprecated ***")
        s.o("fastrouter-subscription-server", 'corerouter ss', "add a Subscription Server to the fastrouter to build the hostname:address map", docs=["SubscriptionServer"])
        s.o("fastrouter-timeout", int, "set the internal fastrouter timeout")
        s.o("fastrouter-post-buffering", long, "enable fastrouter post buffering")
        s.o("fastrouter-post-buffering-dir", str, "put fastrouter buffered files to the specified directory")
        s.o(("fastrouter-stats", "fastrouter-stats-server", "fastrouter-ss"), str, "run the fastrouter stats server")
        s.o("fastrouter-harakiri", int, "enable fastrouter harakiri")
    return config

def forkptyrouter_config():
    config = Config("Forkpty Router")
    
    with config.section("Forkpty Router", docs = []) as s:
        s.o(("forkptyrouter", "forkpty-router", "forkptyurouter", "forkpty-urouter"), u'undeferred corerouter', "run the forkptyrouter on the specified address")
        s.o(("forkptyrouter-command", "forkpty-router-command", "forkptyrouter-cmd", "forkpty-router-cmd"), str, "run the specified command on every connection (default: /bin/sh)")
        s.o("forkptyrouter-rows", u'set 16bit', "set forkptyrouter default pty window rows")
        s.o("forkptyrouter-cols", u'set 16bit', "set forkptyrouter default pty window cols")
        s.o(("forkptyrouter-processes", "forkptyrouter-workers"), int, "prefork the specified number of forkptyrouter processes")
        s.o("forkptyrouter-zerg", u'corerouter zerg', "attach the forkptyrouter to a zerg server")
        s.o("forkptyrouter-fallback", [str], "fallback to the specified node in case of error")
        s.o("forkptyrouter-events", int, "set the maximum number of concufptyent events")
        s.o("forkptyrouter-cheap", True, "run the forkptyrouter in cheap mode")
        s.o("forkptyrouter-timeout", int, "set forkptyrouter timeout")
        s.o(("forkptyrouter-stats", "forkptyrouter-stats-server", "forkptyrouter-ss"), str, "run the forkptyrouter stats server")
        s.o("forkptyrouter-harakiri", int, "enable forkptyrouter harakiri")
    
    return config


def http_options():
    config = Config("HTTP support")
    with config.section("HTTP", docs=["HTTP"]) as s:
        s.o("http", 'address', "enable the embedded HTTP router/server/gateway/loadbalancer/proxy on the specified address")
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
        s.o("http-subscription-server", 'corerouter ss', "enable the SubscriptionServer for clustering and massive hosting/load-balancing")
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
        s.o("http-modifier2", int, "set uwsgi protocol modifier2")
        s.o("http-auto-chunked", True, "automatically transform output to chunked encoding during HTTP 1.1 keepalive (if needed)")
        s.o("http-auto-gzip", True, "automatically gzip content if uWSGI-Encoding header is set to gzip, but content size (Content-Length/Transfer-Encoding) and Content-Encoding are not specified")
        s.o("http-websockets", True, "automatically detect websockets connections and put the session in raw mode")
        s.o("http-stud-prefix", 'add addr list', "expect a stud prefix (1byte family + 4/16 bytes address) on connections from the specified address")

    with config.section("HTTPS", docs=["HTTPS"]) as s:
        s.o("https", 'https config', "add an https router/server on the specified address with specified certificate and key")
        s.o("https-export-cert", True, "export uwsgi variable HTTPS_CC containing the raw client certificate")
        s.o("http-to-https", 'address', "add an HTTP router/server on the specified address and redirect all of the requests to HTTPS")
        s.o("https2", 'https2', "add an https/spdy router/server using keyval options")
        s.o("https-session-context", str, "set the session id context to the specified value")

    return config


def jvm_options():
    config = Config("JVM")
    with config.section("JVM", docs=["JVM"]) as s:
        s.o("jvm-main-class", str, "load the specified class and call its main() function")
        s.o("jvm-classpath", [str], "add the specified directory to the classpath")
        s.o("jvm-opt", [str], "add the specified jvm option")
        s.o("jvm-class", [str], "load the specified class")
        s.o("jwsgi", str, "load the specified JWSGI application (syntax class:method)")

    return config


def lua_options():
    config = Config("Lua")

    with config.section("Lua", docs=["Lua"]) as s:
        s.o("lua", str, "load lua wsapi app")
        s.o("lua-load", [str], "load a lua file")
        s.o(("lua-shell", "luashell"), True, "run the lua interactive shell (debug.debug())")

    return config


def nagios_options():
    config = Config("Nagios")

    with config.section("Nagios output", docs=["Nagios"]) as s:
        s.o("nagios", True, "Output Nagios-friendly status check information")

    return config


def pam_options():
    config = Config("PAM")

    with config.section("PAM", docs=["PAM"]) as s:
        s.o("pam", str, "set the pam service name to use")
        s.o("pam-user", str, "set a fake user for pam")

    return config


def php_options():
    config = Config("PHP")

    with config.section("PHP", docs=["PHP"]) as s:
        s.o(("php-ini", "php-config"), 'php ini', "Use this PHP.ini")
        s.o(("php-ini-append", "php-config-append"), [str], "Append this (these) php.inis to the first one")
        s.o("php-set", ["key=value"], "set a php config directive")
        s.o("php-index", [str], "set the file to open (like index.php) when a directory is requested")
        s.o("php-docroot", str, "force php DOCUMENT_ROOT")
        s.o("php-allowed-docroot", [str], "Add an allowed document root. Only scripts under these directories will be executed.")
        s.o("php-allowed-ext", [str], "Add an allowed php file extension. Only scripts ending with these extensions will run.")
        s.o("php-server-software", str, "force the SERVER_SOFTWARE value reported to PHP")
        s.o("php-app", str, "run _only_ this file whenever a request to the PHP plugin is made")
        s.o("php-dump-config", True, "dump php config (even if modified via --php-set or append options)")
        s.o("php-allowed-script", [str], "list the allowed php scripts (require absolute path)")
        s.o("php-app-qs", str, "when in app mode force QUERY_STRING to the specified value + REQUEST_URI")
        s.o("php-fallback", str, "run the specified php script when the request one does not exist")
        s.o("php-app-bypass", 'add regexp list', "if the regexp matches the uri the --php-app is bypassed")
        s.o("php-var", [str], "add/overwrite a CGI variable at each request")

    return config


def ping_options():
    config = Config("Ping")

    with config.section("Ping", docs=["Ping"]) as s:
        s.o("ping", str, "ping specified uwsgi host", help="If the ping is successful the process exits with a 0 code, otherwise with a value > 0.")
        s.o("ping-timeout", int, "set ping timeout", default=3, help="The maximum number of seconds to wait before considering a uWSGI instance dead")

    return config


def perl_options():
    config = Config("Perl (PSGI plugin)", "Perl")

    with config.section("Perl", docs=["Perl"]) as s:
        s.o("psgi", str, "load a psgi app")
        s.o("perl-no-die-catch", True, "do not catch $SIG{__DIE__}")
        s.o("perl-local-lib", str, "set perl locallib path")
        s.o("perl-version", True, "print perl version")
        s.o("perl-args", str, "add items (space separated) to @ARGV")
        s.o("perl-arg", [str], "add an item to @ARGV")
        s.o("perl-exec", [str], "exec the specified perl file before fork()")
        s.o("perl-exec-post-fork", [str], "exec the specified perl file after fork()")
        s.o("perl-auto-reload", int, "enable perl auto-reloader with the specified frequency")
        s.o("perl-auto-reload-ignore", [str], "ignore the specified files when auto-reload is enabled")

    return config

def pty_config():
    config = Config("pty")
    
    with config.section("pty", docs = ["Pty"]) as s:
        s.o("pty-socket", str, "bind the pty server on the specified address")
        s.o("pty-log", True, "send stdout/stderr to the log engine too")
        s.o("pty-input", True, "read from original stdin in addition to pty")
        s.o("pty-connect", str, "connect the current terminal to a pty server")
        s.o("pty-uconnect", str, "connect the current terminal to a pty server (using uwsgi protocol)")
        s.o("pty-no-isig", True, "disable ISIG terminal attribute in client mode")
        s.o("pty-exec", str, "run the specified command soon after the pty thread is spawned")
    
    return config



def ruby_options():
    config = Config("Ruby")

    with config.section("Ruby", docs=["Ruby"]) as s:
        s.o("rails", str, "load a Ruby on Rails <= 2.x app")
        s.o("rack", str, "load a Rack app")
        s.o(("ruby-gc-freq", "rb-gc-freq"), int, "set Ruby GC frequency")
        s.o(("rb-require", "ruby-require", "rbrequire", "rubyrequire", "require"), [str], "import/require a Ruby module/script")
        s.o(("shared-rb-require", "shared-ruby-require", "shared-rbrequire", "shared-rubyrequire", "shared-require"), [str], "import/require a Ruby module/script (shared)")
        s.o(("gemset", "rvm"), str, "load the specified gemset (rvm)")
        s.o("rvm-path", [str], "search for rvm in the specified directory")
        s.o("rbshell", optional(True), "run a Ruby/irb shell")
        s.o(("rb-threads", "rbthreads", "ruby-threads"), int, "set the number of Ruby threads to run (Ruby 1.9+)")
        s.o(("rb-lib", "ruby-lib"), [str], "add a directory to the ruby libdir search path")
        s.o("rbshell-oneshot", True, "set ruby/irb shell (one shot)")

    return config


def rados_config():
    config = Config("RADOS")
    
    with config.section("RADOS", docs = ["RADOS"]) as s:
        s.o("rados-mount", [str], "virtual mount the specified rados volume in a uri")
        s.o("rados-timeout", int, "timeout for async operations")
    
    return config


def rawrouter_options():
    config = Config("Rawrouter")

    with config.section("Rawrouter", docs=["Rawrouter"]) as s:
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
        s.o("rawrouter-subscription-slot", u'deprecated', "*** deprecated ***")
        s.o("rawrouter-timeout", int, "set rawrouter timeout")
        s.o(("rawrouter-stats", "rawrouter-stats-server", "rawrouter-ss"), str, "run the rawrouter stats server")
        s.o("rawrouter-harakiri", int, "enable rawrouter harakiri")
        s.o("rawrouter-max-retries", int, "set the maximum number of retries/fallbacks to other nodes")

    return config

def rrdtool_options():
    config = Config("RRDtool")

    with config.section("RRDtool", docs=["RRDtool"]) as s:
        s.o("rrdtool", [str], "collect request data in the specified rrd file")
        s.o("rrdtool-freq", int, "set collect frequency")
        s.o("rrdtool-max-ds", int, "set maximum number of data sources")
        s.o("rrdtool-lib", str, "set the name of rrd library (default: librrd.so)")

    return config


def async_options():
    config = Config("Async engines")

    with config.section("Greenlet", docs=["Greenlet"]) as s:
        s.o("greenlet", True, "enable greenlet as suspend engine")

    with config.section("Gevent", docs=["Gevent"]) as s:
        s.o("gevent", int, "a shortcut enabling gevent loop engine with the specified number of async cores and optimal parameters")
        s.o("gevent-monkey-patch", True, "call gevent.monkey.patch_all() automatically on startup")
        s.o("gevent-wait-for-hub", True, "wait for gevent hub's death instead of the control greenlet")

    with config.section("Stackless", docs=["Stackless"]) as s:
        s.o("stackless", True, "use stackless as suspend engine")

    with config.section("uGreen", docs=["uGreen"]) as s:
        s.o("ugreen", True, "Enable uGreen as suspend/resume engine")
        s.o("ugreen-stacksize", int, "set ugreen stack size in pages")

    with config.section("Fiber") as s:
        s.o("fiber", True, "Enable Ruby fiber as suspend engine")

    with config.section("CoroAE", docs=[]) as s:
        s.o("coroae", u'setup coroae', "a shortcut enabling Coro::AnyEvent loop engine with the specified number of async cores and optimal parameters")

    with config.section("tornado", docs = []) as s:
        s.o("tornado", u'setup tornado', "a shortcut enabling tornado loop engine with the specified number of async cores and optimal parameters")
    
    return config

def go_options():
    config = Config("Go")

    with config.section("Gccgo", docs=["Go"]) as s:
        s.o(("go-load", "gccgo-load"), [str], "load a go shared library in the process address space, eventually patching main.main and __go_init_main")
        s.o(("go-args", "gccgo-args"), str, "set go commandline arguments")

    with config.section("Go_plugin", docs=["Go"]) as s:
        s.o("goroutines", 'setup goroutines', "a shortcut setting optimal options for goroutine-based apps, takes the number of goroutines to spawn as argument")

    return config



def geoip_options():
    config = Config("GeoIP")

    with config.section("GeoIP", docs=[]) as s:
        s.o("geoip-country", str, "load the specified geoip country database")
        s.o("geoip-city", str, "load the specified geoip city database")

    return config

def mono_options():
    config = Config("Mono")

    with config.section("Mono", docs=["Mono"]) as s:
        s.o("mono-app", [str], "load a Mono asp.net app from the specified directory")
        s.o("mono-gc-freq", long, "run the Mono GC every <n> requests (default: run after every request)")
        s.o("mono-key", [str], "select the ApplicationHost based on the specified CGI var")
        s.o("mono-version", str, "set the Mono jit version")
        s.o("mono-config", str, "set the Mono config file")
        s.o("mono-assembly", str, "load the specified main assembly (default: uwsgi.dll)")
        s.o("mono-exec", [str], "exec the specified assembly just before app loading")
        s.o("mono-index", [str], "add an asp.net index file")

    return config

def rsyslog_options():
    config = Config("Rsyslog")

    with config.section("Rsyslog", docs=[]) as s:
        s.o("rsyslog-packet-size", int, "set maximum packet size for syslog messages (default 1024) WARNING! using packets > 1024 breaks RFC 3164 (#4.1)")
        s.o("rsyslog-split-messages", True, "split big messages into multiple chunks if they are bigger than allowed packet size (default is false)")

    return config

def webdav_options():
    config = Config("WebDAV")

    with config.section("WebDAV", docs=[]) as s:
        s.o("webdav-mount", [str], "map a filesystem directory as a webdav store")
        s.o("webdav-css", [str], "add a css url for automatic webdav directory listing")
        s.o(("webdav-javascript", "webdav-js"), [str], "add a javascript url for automatic webdav directory listing")
        s.o("webdav-class-directory", str, "set the css directory class for automatic webdav directory listing")
        s.o("webdav-div", str, "set the div id for automatic webdav directory listing")
        s.o("webdav-lock-cache", str, "set the cache to use for webdav locking")
        s.o("webdav-principal-base", str, "enable WebDAV Current Principal Extension using the specified base")
        s.o("webdav-add-option", [str], "add a WebDAV standard to the OPTIONS response")
        s.o("webdav-add-prop", [str], "add a WebDAV property to all resources")
        s.o("webdav-add-collection-prop", [str], "add a WebDAV property to all collections")
        s.o("webdav-add-object-prop", [str], "add a WebDAV property to all objects")
        s.o("webdav-add-prop-href", [str], "add a WebDAV property to all resources (href value)")
        s.o("webdav-add-collection-prop-href", [str], "add a WebDAV property to all collections (href value)")
        s.o("webdav-add-object-prop-href", [str], "add a WebDAV property to all objects (href value)")
        s.o("webdav-add-prop-comp", [str], "add a WebDAV property to all resources (xml value)")
        s.o("webdav-add-collection-prop-comp", [str], "add a WebDAV property to all collections (xml value)")
        s.o("webdav-add-object-prop-comp", [str], "add a WebDAV property to all objects (xml value)")
        s.o("webdav-add-rtype-prop", [str], "add a WebDAV resourcetype property to all resources")
        s.o("webdav-add-rtype-collection-prop", [str], "add a WebDAV resourcetype property to all collections")
        s.o("webdav-add-rtype-object-prop", [str], "add a WebDAV resourcetype property to all objects")
        s.o("webdav-skip-prop", [str], "do not add the specified prop if available in resource xattr")

    return config


def xslt_options():
    config = Config("XSLT")

    with config.section("XSLT", docs=[]) as s:
        s.o("xslt-docroot", [str], "add a document_root for xslt processing")
        s.o("xslt-ext", [str], "search for xslt stylesheets with the specified extension")
        s.o("xslt-var", [str], "get the xslt stylesheet path from the specified request var")
        s.o("xslt-stylesheet", [str], "if no xslt stylesheet file can be found, use the specified one")
        s.o("xslt-content-type", str, "set the content-type for the xslt rsult (default: text/html)")

    return config


def ring_options():
    config = Config("Ring")

    with config.section("Ring", docs=[]) as s:
        s.o(("ring-load", "clojure-load"), [str], "load the specified clojure script")
        s.o("ring-app", str, "map the specified ring application (syntax namespace:function)")

    return config

def glusterfs_options():
    config = Config("GlusterFS")

    with config.section("GlusterFS", docs=[]) as s:
        s.o("glusterfs-mount", [str], "virtual mount the specified glusterfs volume in a uri")
        s.o("glusterfs-timeout", int, "timeout for glusterfs async mode")

    return config




def sslrouter_options():
    config = Config("SSL Router")

    with config.section("SSL Router", docs=[]) as s:
        s.o("sslrouter", u'sslrouter', "run the sslrouter on the specified port")
        s.o("sslrouter2", u'sslrouter2', "run the sslrouter on the specified port (key-value based)")
        s.o("sslrouter-session-context", str, "set the session id context to the specified value")
        s.o(("sslrouter-processes", "sslrouter-workers"), int, "prefork the specified number of sslrouter processes")
        s.o("sslrouter-zerg", u'corerouter zerg', "attach the sslrouter to a zerg server")
        s.o("sslrouter-use-cache", optional(str), "use uWSGI cache as hostname->server mapper for the sslrouter")
        s.o("sslrouter-use-pattern", u'corerouter use pattern', "use a pattern for sslrouter hostname->server mapping")
        s.o("sslrouter-use-base", u'corerouter use base', "use a base dir for sslrouter hostname->server mapping")
        s.o("sslrouter-fallback", [str], "fallback to the specified node in case of error")
        s.o("sslrouter-use-code-string", u'corerouter cs', "use code string as hostname->server mapper for the sslrouter")
        s.o("sslrouter-use-socket", optional(u'corerouter use socket'), "forward request to the specified uwsgi socket")
        s.o("sslrouter-to", [str], "forward requests to the specified uwsgi server (you can specify it multiple times for load balancing)")
        s.o("sslrouter-gracetime", int, "retry connections to dead static nodes after the specified amount of seconds")
        s.o("sslrouter-events", int, "set the maximum number of concusrent events")
        s.o("sslrouter-max-retries", int, "set the maximum number of retries/fallbacks to other nodes")
        s.o("sslrouter-quiet", True, "do not report failed connections to instances")
        s.o("sslrouter-cheap", True, "run the sslrouter in cheap mode")
        s.o("sslrouter-subscription-server", u'corerouter ss', "run the sslrouter subscription server on the spcified address")
        s.o("sslrouter-timeout", int, "set sslrouter timeout")
        s.o(("sslrouter-stats", "sslrouter-stats-server", "sslrouter-ss"), str, "run the sslrouter stats server")
        s.o("sslrouter-harakiri", int, "enable sslrouter harakiri")
        s.o("sslrouter-sni", True, "use SNI to route requests")

    return config


def symcall_options():
    config = Config("Symcall")

    with config.section("Symcall", docs=[]) as s:
        s.o("symcall", str, "load the specified C symbol as the symcall request handler")
        s.o("symcall-register-rpc", [str], "load the specified C symbol as an RPC function (syntax: name function)")
        s.o("symcall-post-fork", [str], "call the specified C symbol after each fork()")

    return config


def tuntap_config():
    config = Config("TUN/TAP")
    
    with config.section("TUN/TAP", docs = []) as s:
        s.o("tuntap-router", [str], "run the tuntap router (syntax: <device> <socket> [stats])")
        s.o("tuntap-device", [str], "add a tuntap device to the instance (syntax: <device>[ <socket>])")
        s.o(("tuntap-router-firewall-in", "tuntap-router-firewall-out"), u'uwsgi tuntap opt firewall', "add a firewall rule to the tuntap router (syntax: <action> <src/mask> <dst/mask>)")
    
    return config
