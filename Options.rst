uWSGI Options
^^^^^^^^^^^^^

This is an automatically generated reference list of the uWSGI options.

It is the same output you can get via the ``--help`` option.

This page is probably the worst way to understand uWSGI for newbies. If you are still learning how the project
works, you should read the various quickstarts and tutorials.

uWSGI core
==========
----socket
******
``argument``: required_argument

``shortcut``: -s

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using default protocol

----uwsgi-socket
************
``argument``: required_argument

``shortcut``: -s

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using uwsgi protocol

----suwsgi-socket
*************
``argument``: required_argument

``shortcut``: -s

``parser``: uwsgi_opt_add_ssl_socket



bind to the specified UNIX/TCP socket using uwsgi protocol over SSL

----ssl-socket
**********
``argument``: required_argument

``shortcut``: -s

``parser``: uwsgi_opt_add_ssl_socket



bind to the specified UNIX/TCP socket using uwsgi protocol over SSL

----http-socket
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using HTTP protocol

----http-socket-modifier1
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier1 when using HTTP protocol

----http-socket-modifier2
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier2 when using HTTP protocol

----https-socket
************
``argument``: required_argument

``parser``: uwsgi_opt_add_ssl_socket



bind to the specified UNIX/TCP socket using HTTPS protocol

----https-socket-modifier1
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier1 when using HTTPS protocol

----https-socket-modifier2
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier2 when using HTTPS protocol

----fastcgi-socket
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using FastCGI protocol

----fastcgi-nph-socket
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using FastCGI protocol (nph mode)

----fastcgi-modifier1
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier1 when using FastCGI protocol

----fastcgi-modifier2
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier2 when using FastCGI protocol

----scgi-socket
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using SCGI protocol

----scgi-nph-socket
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using SCGI protocol (nph mode)

----scgi-modifier1
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier1 when using SCGI protocol

----scgi-modifier2
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier2 when using SCGI protocol

----raw-socket
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_socket_no_defer



bind to the specified UNIX/TCP socket using RAW protocol

----raw-modifier1
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier1 when using RAW protocol

----raw-modifier2
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



force the specified modifier2 when using RAW protocol

----puwsgi-socket
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_socket



bind to the specified UNIX/TCP socket using persistent uwsgi protocol (puwsgi)

----protocol
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force the specified protocol for default sockets

----socket-protocol
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force the specified protocol for default sockets

----shared-socket
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_shared_socket



create a shared sacket for advanced jailing or ipc

----undeferred-shared-socket
************************
``argument``: required_argument

``parser``: uwsgi_opt_add_shared_socket



create a shared sacket for advanced jailing or ipc (undeferred mode)

----processes
*********
``argument``: required_argument

``shortcut``: -p

``parser``: uwsgi_opt_set_int



spawn the specified number of workers/processes

----workers
*******
``argument``: required_argument

``shortcut``: -p

``parser``: uwsgi_opt_set_int



spawn the specified number of workers/processes

----thunder-lock
************
``argument``: no_argument

``parser``: uwsgi_opt_true



serialize accept() usage (if possible)

----harakiri
********
``argument``: required_argument

``shortcut``: -t

``parser``: uwsgi_opt_set_int



set harakiri timeout

----harakiri-verbose
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable verbose mode for harakiri

----harakiri-no-arh
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not enable harakiri during after-request-hook

----no-harakiri-arh
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not enable harakiri during after-request-hook

----no-harakiri-after-req-hook
**************************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not enable harakiri during after-request-hook

----backtrace-depth
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set backtrace depth

----mule-harakiri
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set harakiri timeout for mule tasks

----xmlconfig
*********
``argument``: required_argument

``shortcut``: -x

``parser``: uwsgi_opt_load_xml

``flags``: UWSGI_OPT_IMMEDIATE



load config from xml file

----xml
***
``argument``: required_argument

``shortcut``: -x

``parser``: uwsgi_opt_load_xml

``flags``: UWSGI_OPT_IMMEDIATE



load config from xml file

----config
******
``argument``: required_argument

``parser``: uwsgi_opt_load_config

``flags``: UWSGI_OPT_IMMEDIATE



load configuration using the pluggable system

----fallback-config
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_IMMEDIATE



re-exec uwsgi with the specified config when exit code is 1

----strict
******
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_IMMEDIATE



enable strict mode (placeholder cannot be used)

----skip-zero
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



skip check of file descriptor 0

----skip-atexit
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



skip atexit hooks (ignored by the master)

----set
***
``argument``: required_argument

``shortcut``: -S

``parser``: uwsgi_opt_set_placeholder

``flags``: UWSGI_OPT_IMMEDIATE



set a placeholder or an option

----set-placeholder
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_placeholder

``flags``: UWSGI_OPT_IMMEDIATE



set a placeholder

----set-ph
******
``argument``: required_argument

``parser``: uwsgi_opt_set_placeholder

``flags``: UWSGI_OPT_IMMEDIATE



set a placeholder

----get
***
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_NO_INITIAL



print the specified option value and exit

----declare-option
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_custom_option

``flags``: UWSGI_OPT_IMMEDIATE



declare a new uWSGI custom option

----declare-option2
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_custom_option



declare a new uWSGI custom option (non-immediate)

----resolve
*******
``argument``: required_argument

``parser``: uwsgi_opt_resolve

``flags``: UWSGI_OPT_IMMEDIATE



place the result of a dns query in the specified placeholder, sytax: placeholder=name (immediate option)

----for
***
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) for cycle

----for-glob
********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) for cycle (expand glob)

----for-times
*********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) for cycle (expand the specified num to a list starting from 1)

----for-readline
************
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) for cycle (expand the specified file to a list of lines)

----endfor
******
``argument``: optional_argument

``parser``: uwsgi_opt_noop

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) end for cycle

----end-for
*******
``argument``: optional_argument

``parser``: uwsgi_opt_noop

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) end for cycle

----if-opt
******
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for option

----if-not-opt
**********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for option

----if-env
******
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for environment variable

----if-not-env
**********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for environment variable

----ifenv
*****
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for environment variable

----if-reload
*********
``argument``: no_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for reload

----if-not-reload
*************
``argument``: no_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for reload

----if-exists
*********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for file/directory existance

----if-not-exists
*************
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for file/directory existance

----ifexists
********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for file/directory existance

----if-plugin
*********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for plugin

----if-not-plugin
*************
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for plugin

----ifplugin
********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for plugin

----if-file
*******
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for file existance

----if-not-file
***********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for file existance

----if-dir
******
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for directory existance

----if-not-dir
**********
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for directory existance

----ifdir
*****
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for directory existance

----if-directory
************
``argument``: required_argument

``parser``: uwsgi_opt_logic

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) check for directory existance

----endif
*****
``argument``: optional_argument

``parser``: uwsgi_opt_noop

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) end if

----end-if
******
``argument``: optional_argument

``parser``: uwsgi_opt_noop

``flags``: UWSGI_OPT_IMMEDIATE



(opt logic) end if

----blacklist
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_IMMEDIATE



set options blacklist context

----end-blacklist
*************
``argument``: no_argument

``parser``: uwsgi_opt_set_null

``flags``: UWSGI_OPT_IMMEDIATE



clear options blacklist context

----whitelist
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_IMMEDIATE



set options whitelist context

----end-whitelist
*************
``argument``: no_argument

``parser``: uwsgi_opt_set_null

``flags``: UWSGI_OPT_IMMEDIATE



clear options whitelist context

----ignore-sigpipe
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not report (annoying) SIGPIPE

----ignore-write-errors
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not report (annoying) write()/writev() errors

----write-errors-tolerance
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the maximum number of allowed write errors (default: no tolerance)

----write-errors-exception-only
***************************
``argument``: no_argument

``parser``: uwsgi_opt_true



only raise an exception on write errors giving control to the app itself

----disable-write-exception
***********************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable exception generation on write()/writev()

----inherit
*******
``argument``: required_argument

``parser``: uwsgi_opt_load



use the specified file as config template

----include
*******
``argument``: required_argument

``parser``: uwsgi_opt_load

``flags``: UWSGI_OPT_IMMEDIATE



include the specified file as immediate configuration

----inject-before
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_IMMEDIATE



inject a text file before the config file (advanced templating)

----inject-after
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_IMMEDIATE



inject a text file after the config file (advanced templating)

----daemonize
*********
``argument``: required_argument

``shortcut``: -d

``parser``: uwsgi_opt_set_str



daemonize uWSGI

----daemonize2
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



daemonize uWSGI after app loading

----stop
****
``argument``: required_argument

``parser``: uwsgi_opt_pidfile_signal

``flags``: UWSGI_OPT_IMMEDIATE



stop an instance

----reload
******
``argument``: required_argument

``parser``: uwsgi_opt_pidfile_signal

``flags``: UWSGI_OPT_IMMEDIATE



reload an instance

----pause
*****
``argument``: required_argument

``parser``: uwsgi_opt_pidfile_signal

``flags``: UWSGI_OPT_IMMEDIATE



pause an instance

----suspend
*******
``argument``: required_argument

``parser``: uwsgi_opt_pidfile_signal

``flags``: UWSGI_OPT_IMMEDIATE



suspend an instance

----resume
******
``argument``: required_argument

``parser``: uwsgi_opt_pidfile_signal

``flags``: UWSGI_OPT_IMMEDIATE



resume an instance

----connect-and-read
****************
``argument``: required_argument

``parser``: uwsgi_opt_connect_and_read

``flags``: UWSGI_OPT_IMMEDIATE



connect to a socket and wait for data from it

----extract
*******
``argument``: required_argument

``parser``: uwsgi_opt_extract

``flags``: UWSGI_OPT_IMMEDIATE



fetch/dump any supported address to stdout

----listen
******
``argument``: required_argument

``shortcut``: -l

``parser``: uwsgi_opt_set_int



set the socket listen queue size

----max-vars
********
``argument``: required_argument

``shortcut``: -v

``parser``: uwsgi_opt_max_vars



set the amount of internal iovec/vars structures

----max-apps
********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of per-worker applications

----buffer-size
***********
``argument``: required_argument

``shortcut``: -b

``parser``: uwsgi_opt_set_16bit



set internal buffer size

----memory-report
*************
``argument``: no_argument

``shortcut``: -m

``parser``: uwsgi_opt_true



enable memory report

----profiler
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



enable the specified profiler

----cgi-mode
********
``argument``: no_argument

``shortcut``: -c

``parser``: uwsgi_opt_true



force CGI-mode for plugins supporting it

----abstract-socket
***************
``argument``: no_argument

``shortcut``: -a

``parser``: uwsgi_opt_true



force UNIX socket in abstract mode (Linux only)

----chmod-socket
************
``argument``: optional_argument

``shortcut``: -C

``parser``: uwsgi_opt_chmod_socket



chmod-socket

----chmod
*****
``argument``: optional_argument

``shortcut``: -C

``parser``: uwsgi_opt_chmod_socket



chmod-socket

----chown-socket
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



chown unix sockets

----umask
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_umask

``flags``: UWSGI_OPT_IMMEDIATE



set umask

----freebind
********
``argument``: no_argument

``parser``: uwsgi_opt_true



put socket in freebind mode

----map-socket
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



map sockets to specific workers

----enable-threads
**************
``argument``: no_argument

``shortcut``: -T

``parser``: uwsgi_opt_true



enable threads

----no-threads-wait
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not wait for threads cancellation on quit/reload

----auto-procname
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



automatically set processes name to something meaningful

----procname-prefix
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_PROCNAME



add a prefix to the process names

----procname-prefix-spaced
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str_spaced

``flags``: UWSGI_OPT_PROCNAME



add a spaced prefix to the process names

----procname-append
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_PROCNAME



append a string to process names

----procname
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_PROCNAME



set process names

----procname-master
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_PROCNAME



set master process name

----single-interpreter
******************
``argument``: no_argument

``shortcut``: -i

``parser``: uwsgi_opt_true



do not use multiple interpreters (where available)

----need-app
********
``argument``: no_argument

``parser``: uwsgi_opt_true



exit if no app can be loaded

----master
******
``argument``: no_argument

``shortcut``: -M

``parser``: uwsgi_opt_true



enable master process

----honour-stdin
************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not remap stdin to /dev/null

----emperor
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the Emperor

----emperor-proxy-socket
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force the vassal to became an Emperor proxy

----emperor-wrapper
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set a binary wrapper for vassals

----emperor-nofollow
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not follow symlinks when checking for mtime

----emperor-procname
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the Emperor process name

----emperor-freq
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the Emperor scan frequency (default 3 seconds)

----emperor-required-heartbeat
**************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the Emperor tolerance about heartbeats

----emperor-curse-tolerance
***********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the Emperor tolerance about cursed vassals

----emperor-pidfile
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



write the Emperor pid in the specified file

----emperor-tyrant
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



put the Emperor in Tyrant mode

----emperor-tyrant-nofollow
***********************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not follow symlinks when checking for uid/gid in Tyrant mode

----emperor-stats
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the Emperor stats server

----emperor-stats-server
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the Emperor stats server

----early-emperor
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



spawn the emperor as soon as possibile

----emperor-broodlord
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



run the emperor in BroodLord mode

----emperor-throttle
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set throttling level (in milliseconds) for bad behaving vassals (default 1000)

----emperor-max-throttle
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set max throttling level (in milliseconds) for bad behaving vassals (default 3 minutes)

----emperor-magic-exec
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



prefix vassals config files with exec:// if they have the executable bit

----emperor-on-demand-extension
***************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



search for text file (vassal name + extension) containing the on demand socket name

----emperor-on-demand-ext
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



search for text file (vassal name + extension) containing the on demand socket name

----emperor-on-demand-directory
***************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



enable on demand mode binding to the unix socket in the specified directory named like the vassal + .socket

----emperor-on-demand-dir
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



enable on demand mode binding to the unix socket in the specified directory named like the vassal + .socket

----emperor-on-demand-exec
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



use the output of the specified command as on demand socket name (the vassal name is passed as the only argument)

----emperor-extra-extension
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



allows the specified extension in the Emperor (vassal will be called with --config)

----emperor-extra-ext
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



allows the specified extension in the Emperor (vassal will be called with --config)

----emperor-no-blacklist
********************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable Emperor blacklisting subsystem

----emperor-use-clone
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_unshare



use clone() instead of fork() passing the specified unshare() flags

----emperor-cap
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_emperor_cap



set vassals capability

----vassals-cap
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_emperor_cap



set vassals capability

----vassal-cap
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_emperor_cap



set vassals capability

----imperial-monitor-list
*********************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled imperial monitors

----imperial-monitors-list
**********************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled imperial monitors

----vassals-inherit
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add config templates to vassals config (uses --inherit)

----vassals-include
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



include config templates to vassals config (uses --include instead of --inherit)

----vassals-inherit-before
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add config templates to vassals config (uses --inherit, parses before the vassal file)

----vassals-include-before
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



include config templates to vassals config (uses --include instead of --inherit, parses before the vassal file)

----vassals-start-hook
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command before each vassal starts

----vassals-stop-hook
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command after vassal's death

----vassal-sos-backlog
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



ask emperor for sos if backlog queue has more items than the value specified

----vassals-set
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



automatically set the specified option (via --set) for every vassal

----vassal-set
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



automatically set the specified option (via --set) for every vassal

----heartbeat
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



announce healthiness to the emperor

----reload-mercy
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum time (in seconds) we wait for workers and other processes to die during reload/shutdown

----worker-reload-mercy
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum time (in seconds) a worker can take to reload/shutdown (default is 60)

----mule-reload-mercy
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum time (in seconds) a mule can take to reload/shutdown (default is 60)

----exit-on-reload
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



force exit even if a reload is requested

----die-on-term
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



exit instead of brutal reload on SIGTERM

----force-gateway
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



force the spawn of the first registered gateway without a master

----help
****
``argument``: no_argument

``shortcut``: -h

``parser``: uwsgi_help

``flags``: UWSGI_OPT_IMMEDIATE



show this help

----usage
*****
``argument``: no_argument

``shortcut``: -h

``parser``: uwsgi_help

``flags``: UWSGI_OPT_IMMEDIATE



show this help

----print-sym
*********
``argument``: required_argument

``parser``: uwsgi_print_sym

``flags``: UWSGI_OPT_IMMEDIATE



print content of the specified binary symbol

----print-symbol
************
``argument``: required_argument

``parser``: uwsgi_print_sym

``flags``: UWSGI_OPT_IMMEDIATE



print content of the specified binary symbol

----reaper
******
``argument``: no_argument

``shortcut``: -r

``parser``: uwsgi_opt_true



call waitpid(-1,...) after each request to get rid of zombies

----max-requests
************
``argument``: required_argument

``shortcut``: -R

``parser``: uwsgi_opt_set_64bit



reload workers after the specified amount of managed requests

----min-worker-lifetime
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



number of seconds worker must run before being reloaded (default is 60)

----max-worker-lifetime
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



reload workers after the specified amount of seconds (default is disabled)

----socket-timeout
**************
``argument``: required_argument

``shortcut``: -z

``parser``: uwsgi_opt_set_int



set internal sockets timeout

----no-fd-passing
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable file descriptor passing

----locks
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_int



create the specified number of shared locks

----lock-engine
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the lock engine

----ftok
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the ipcsem key via ftok() for avoiding duplicates

----persistent-ipcsem
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not remove ipcsem's on shutdown

----sharedarea
**********
``argument``: required_argument

``shortcut``: -A

``parser``: uwsgi_opt_add_string_list



create a raw shared memory area of specified pages (note: it supports keyval too)

----safe-fd
*******
``argument``: required_argument

``parser``: uwsgi_opt_safe_fd



do not close the specified file descriptor

----fd-safe
*******
``argument``: required_argument

``parser``: uwsgi_opt_safe_fd



do not close the specified file descriptor

----cache
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



create a shared cache containing given elements

----cache-blocksize
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set cache blocksize

----cache-store
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



enable persistent cache to disk

----cache-store-sync
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set frequency of sync for persistent cache

----cache-no-expire
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable auto sweep of expired items

----cache-expire-freq
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the frequency of cache sweeper scans (default 3 seconds)

----cache-report-freed-items
************************
``argument``: no_argument

``parser``: uwsgi_opt_true



constantly report the cache item freed by the sweeper (use only for debug)

----cache-udp-server
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



bind the cache udp server (used only for set/update/delete) to the specified socket

----cache-udp-node
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



send cache update/deletion to the specified cache udp server

----cache-sync
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



copy the whole content of another uWSGI cache server on server startup

----cache-use-last-modified
***********************
``argument``: no_argument

``parser``: uwsgi_opt_true



update last_modified_at timestamp on every cache item modification (default is disabled)

----add-cache-item
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an item in the cache

----load-file-in-cache
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a static file in the cache

----load-file-in-cache-gzip
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a static file in the cache with gzip compression

----cache2
******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



create a new generation shared cache (keyval syntax)

----queue
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable shared queue

----queue-blocksize
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set queue blocksize

----queue-store
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



enable persistent queue to disk

----queue-store-sync
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set frequency of sync for persistent queue

----spooler
*******
``argument``: required_argument

``shortcut``: -Q

``parser``: uwsgi_opt_add_spooler

``flags``: UWSGI_OPT_MASTER



run a spooler on the specified directory

----spooler-external
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_spooler

``flags``: UWSGI_OPT_MASTER



map spoolers requests to a spooler directory managed by an external instance

----spooler-ordered
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



try to order the execution of spooler tasks

----spooler-chdir
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



chdir() to specified directory before each spooler task

----spooler-processes
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_IMMEDIATE



set the number of processes for spoolers

----spooler-quiet
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not be verbose with spooler tasks

----spooler-max-tasks
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of tasks to run before recycling a spooler

----spooler-harakiri
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set harakiri timeout for spooler tasks

----spooler-frequency
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set spooler frequency

----spooler-freq
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set spooler frequency

----mule
****
``argument``: optional_argument

``parser``: uwsgi_opt_add_mule

``flags``: UWSGI_OPT_MASTER



add a mule

----mules
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_mules

``flags``: UWSGI_OPT_MASTER



add the specified number of mules

----farm
****
``argument``: required_argument

``parser``: uwsgi_opt_add_farm

``flags``: UWSGI_OPT_MASTER



add a mule farm

----mule-msg-size
*************
``argument``: optional_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set mule message buffer size

----signal
******
``argument``: required_argument

``parser``: uwsgi_opt_signal

``flags``: UWSGI_OPT_IMMEDIATE



send a uwsgi signal to a server

----signal-bufsize
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set buffer size for signal queue

----signals-bufsize
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set buffer size for signal queue

----signal-timer
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



add a timer (syntax: <signal> <seconds>)

----timer
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



add a timer (syntax: <signal> <seconds>)

----signal-rbtimer
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



add a redblack timer (syntax: <signal> <seconds>)

----rbtimer
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



add a redblack timer (syntax: <signal> <seconds>)

----rpc-max
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



maximum number of rpc slots (default: 64)

----disable-logging
***************
``argument``: no_argument

``shortcut``: -L

``parser``: uwsgi_opt_false



disable request logging

----flock
*****
``argument``: required_argument

``parser``: uwsgi_opt_flock

``flags``: UWSGI_OPT_IMMEDIATE



lock the specified file before starting, exit if locked

----flock-wait
**********
``argument``: required_argument

``parser``: uwsgi_opt_flock_wait

``flags``: UWSGI_OPT_IMMEDIATE



lock the specified file before starting, wait if locked

----flock2
******
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_IMMEDIATE



lock the specified file after logging/daemon setup, exit if locked

----flock-wait2
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_IMMEDIATE



lock the specified file after logging/daemon setup, wait if locked

----pidfile
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



create pidfile (before privileges drop)

----pidfile2
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



create pidfile (after privileges drop)

----chroot
******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



chroot() to the specified directory

----pivot-root
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



pivot_root() to the specified directories (new_root and put_old must be separated with a space)

----pivot_root
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



pivot_root() to the specified directories (new_root and put_old must be separated with a space)

----uid
***
``argument``: required_argument

``parser``: uwsgi_opt_set_uid



setuid to the specified user/uid

----gid
***
``argument``: required_argument

``parser``: uwsgi_opt_set_gid



setgid to the specified group/gid

----add-gid
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add the specified group id to the process credentials

----immediate-uid
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_immediate_uid

``flags``: UWSGI_OPT_IMMEDIATE



setuid to the specified user/uid IMMEDIATELY

----immediate-gid
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_immediate_gid

``flags``: UWSGI_OPT_IMMEDIATE



setgid to the specified group/gid IMMEDIATELY

----no-initgroups
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable additional groups set via initgroups()

----cap
***
``argument``: required_argument

``parser``: uwsgi_opt_set_cap



set process capability

----unshare
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_unshare



unshare() part of the processes and put it in a new namespace

----unshare2
********
``argument``: required_argument

``parser``: uwsgi_opt_set_unshare



unshare() part of the processes and put it in a new namespace after rootfs change

----setns-socket
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



expose a unix socket returning namespace fds from /proc/self/ns

----setns-socket-skip
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



skip the specified entry when sending setns file descriptors

----setns-skip
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



skip the specified entry when sending setns file descriptors

----setns
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



join a namespace created by an external uWSGI instance

----setns-preopen
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



open /proc/self/ns as soon as possible and cache fds

----jailed
******
``argument``: no_argument

``parser``: uwsgi_opt_true



mark the instance as jailed (force the execution of post_jail hooks)

----jail
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



put the instance in a FreeBSD jail

----jail-ip4
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an ipv4 address to the FreeBSD jail

----jail-ip6
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an ipv6 address to the FreeBSD jail

----jidfile
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



save the jid of a FreeBSD jail in the specified file

----jid-file
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



save the jid of a FreeBSD jail in the specified file

----jail2
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an option to the FreeBSD jail

----libjail
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an option to the FreeBSD jail

----jail-attach
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



attach to the FreeBSD jail

----refork
******
``argument``: no_argument

``parser``: uwsgi_opt_true



fork() again after privileges drop. Useful for jailing systems

----re-fork
*******
``argument``: no_argument

``parser``: uwsgi_opt_true



fork() again after privileges drop. Useful for jailing systems

----refork-as-root
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



fork() again before privileges drop. Useful for jailing systems

----re-fork-as-root
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



fork() again before privileges drop. Useful for jailing systems

----refork-post-jail
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



fork() again after jailing. Useful for jailing systems

----re-fork-post-jail
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



fork() again after jailing. Useful for jailing systems

----hook-asap
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook as soon as possible

----hook-pre-jail
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook before jailing

----hook-post-jail
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook after jailing

----hook-in-jail
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook in jail after initialization

----hook-as-root
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook before privileges drop

----hook-as-user
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook after privileges drop

----hook-as-user-atexit
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook before app exit and reload

----hook-pre-app
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook before app loading

----hook-post-app
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook after app loading

----hook-accepting
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook after each worker enter the accepting phase

----hook-accepting1
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook after the first worker enters the accepting phase

----hook-accepting-once
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook after each worker enter the accepting phase (once per-instance)

----hook-accepting1-once
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook after the first worker enters the accepting phase (once per instance)

----hook-master-start
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook when the Master starts

----hook-touch
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook when the specified file is touched (syntax: <file> <action>)

----hook-emperor-start
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook when the Emperor starts

----hook-emperor-stop
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook when the Emperor send a stop message

----hook-emperor-reload
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook when the Emperor send a reload message

----hook-emperor-lost
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook when the Emperor connection is lost

----hook-as-vassal
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook before exec()ing the vassal

----hook-as-emperor
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook in the emperor after the vassal has been started

----hook-as-mule
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook in each mule

----hook-as-gateway
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified hook in each gateway

----after-request-hook
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified function/symbol after each request

----after-request-call
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified function/symbol after each request

----exec-asap
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command as soon as possible

----exec-pre-jail
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command before jailing

----exec-post-jail
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command after jailing

----exec-in-jail
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command in jail after initialization

----exec-as-root
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command before privileges drop

----exec-as-user
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command after privileges drop

----exec-as-user-atexit
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command before app exit and reload

----exec-pre-app
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command before app loading

----exec-post-app
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command after app loading

----exec-as-vassal
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command before exec()ing the vassal

----exec-as-emperor
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the specified command in the emperor after the vassal has been started

----mount-asap
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



mount filesystem as soon as possible

----mount-pre-jail
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



mount filesystem before jailing

----mount-post-jail
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



mount filesystem after jailing

----mount-in-jail
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



mount filesystem in jail after initialization

----mount-as-root
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



mount filesystem before privileges drop

----mount-as-vassal
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



mount filesystem before exec()ing the vassal

----mount-as-emperor
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



mount filesystem in the emperor after the vassal has been started

----umount-asap
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unmount filesystem as soon as possible

----umount-pre-jail
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unmount filesystem before jailing

----umount-post-jail
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unmount filesystem after jailing

----umount-in-jail
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unmount filesystem in jail after initialization

----umount-as-root
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unmount filesystem before privileges drop

----umount-as-vassal
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unmount filesystem before exec()ing the vassal

----umount-as-emperor
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unmount filesystem in the emperor after the vassal has been started

----wait-for-interface
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



wait for the specified network interface to come up before running root hooks

----wait-for-interface-timeout
**************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the timeout for wait-for-interface

----wait-interface
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



wait for the specified network interface to come up before running root hooks

----wait-interface-timeout
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the timeout for wait-for-interface

----wait-for-iface
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



wait for the specified network interface to come up before running root hooks

----wait-for-iface-timeout
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the timeout for wait-for-interface

----wait-iface
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



wait for the specified network interface to come up before running root hooks

----wait-iface-timeout
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the timeout for wait-for-interface

----call-asap
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function as soon as possible

----call-pre-jail
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function before jailing

----call-post-jail
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function after jailing

----call-in-jail
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function in jail after initialization

----call-as-root
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function before privileges drop

----call-as-user
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function after privileges drop

----call-as-user-atexit
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function before app exit and reload

----call-pre-app
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function before app loading

----call-post-app
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function after app loading

----call-as-vassal
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function() before exec()ing the vassal

----call-as-vassal1
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function before exec()ing the vassal

----call-as-vassal3
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function(char *, uid_t, gid_t) before exec()ing the vassal

----call-as-emperor
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function() in the emperor after the vassal has been started

----call-as-emperor1
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function in the emperor after the vassal has been started

----call-as-emperor2
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function(char *, pid_t) in the emperor after the vassal has been started

----call-as-emperor4
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified function(char *, pid_t, uid_t, gid_t) in the emperor after the vassal has been started

----ini
***
``argument``: required_argument

``parser``: uwsgi_opt_load_ini

``flags``: UWSGI_OPT_IMMEDIATE



load config from ini file

----yaml
****
``argument``: required_argument

``shortcut``: -y

``parser``: uwsgi_opt_load_yml

``flags``: UWSGI_OPT_IMMEDIATE



load config from yaml file

----yml
***
``argument``: required_argument

``shortcut``: -y

``parser``: uwsgi_opt_load_yml

``flags``: UWSGI_OPT_IMMEDIATE



load config from yaml file

----json
****
``argument``: required_argument

``shortcut``: -j

``parser``: uwsgi_opt_load_json

``flags``: UWSGI_OPT_IMMEDIATE



load config from json file

----js
**
``argument``: required_argument

``shortcut``: -j

``parser``: uwsgi_opt_load_json

``flags``: UWSGI_OPT_IMMEDIATE



load config from json file

----weight
******
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



weight of the instance (used by clustering/lb/subscriptions)

----auto-weight
***********
``argument``: required_argument

``parser``: uwsgi_opt_true



set weight of the instance (used by clustering/lb/subscriptions) automatically

----no-server
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



force no-server mode

----command-mode
************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_IMMEDIATE



force command mode

----no-defer-accept
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable deferred-accept on sockets

----tcp-nodelay
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



enable TCP NODELAY on each request

----so-keepalive
************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable TCP KEEPALIVEs

----so-send-timeout
***************
``argument``: no_argument

``parser``: uwsgi_opt_set_int



set SO_SNDTIMEO

----socket-send-timeout
*******************
``argument``: no_argument

``parser``: uwsgi_opt_set_int



set SO_SNDTIMEO

----so-write-timeout
****************
``argument``: no_argument

``parser``: uwsgi_opt_set_int



set SO_SNDTIMEO

----socket-write-timeout
********************
``argument``: no_argument

``parser``: uwsgi_opt_set_int



set SO_SNDTIMEO

----socket-sndbuf
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set SO_SNDBUF

----socket-rcvbuf
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set SO_RCVBUF

----limit-as
********
``argument``: required_argument

``parser``: uwsgi_opt_set_megabytes



limit processes address space/vsz

----limit-nproc
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



limit the number of spawnable processes

----reload-on-as
************
``argument``: required_argument

``parser``: uwsgi_opt_set_megabytes

``flags``: UWSGI_OPT_MEMORY



reload if address space is higher than specified megabytes

----reload-on-rss
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_megabytes

``flags``: UWSGI_OPT_MEMORY



reload if rss memory is higher than specified megabytes

----evil-reload-on-as
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_megabytes

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_MEMORY



force the master to reload a worker if its address space is higher than specified megabytes

----evil-reload-on-rss
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_megabytes

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_MEMORY



force the master to reload a worker if its rss memory is higher than specified megabytes

----reload-on-fd
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



reload if the specified file descriptor is ready

----brutal-reload-on-fd
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



brutal reload if the specified file descriptor is ready

----ksm
***
``argument``: optional_argument

``parser``: uwsgi_opt_set_int



enable Linux KSM

----pcre-jit
********
``argument``: no_argument

``parser``: uwsgi_opt_pcre_jit

``flags``: UWSGI_OPT_IMMEDIATE



enable pcre jit (if available)

----never-swap
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



lock all memory pages avoiding swapping

----touch-reload
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



reload uWSGI if the specified file is modified/touched

----touch-workers-reload
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



trigger reload of (only) workers if the specified file is modified/touched

----touch-chain-reload
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



trigger chain reload if the specified file is modified/touched

----touch-logrotate
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



trigger logrotation if the specified file is modified/touched

----touch-logreopen
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



trigger log reopen if the specified file is modified/touched

----touch-exec
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



run command when the specified file is modified/touched (syntax: file command)

----touch-signal
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



signal when the specified file is modified/touched (syntax: file signal)

----fs-reload
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



graceful reload when the specified filesystem object is modified

----fs-brutal-reload
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



brutal reload when the specified filesystem object is modified

----fs-signal
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise a uwsgi signal when the specified filesystem object is modified (syntax: file signal)

----check-mountpoint
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



destroy the instance if a filesystem is no more reachable (useful for reliable Fuse management)

----mountpoint-check
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



destroy the instance if a filesystem is no more reachable (useful for reliable Fuse management)

----check-mount
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



destroy the instance if a filesystem is no more reachable (useful for reliable Fuse management)

----mount-check
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



destroy the instance if a filesystem is no more reachable (useful for reliable Fuse management)

----propagate-touch
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



over-engineering option for system with flaky signal management

----limit-post
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



limit request body

----no-orphans
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



automatically kill workers if master dies (can be dangerous for availability)

----prio
****
``argument``: required_argument

``parser``: uwsgi_opt_set_rawint



set processes/threads priority

----cpu-affinity
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set cpu affinity

----post-buffering
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



enable post buffering

----post-buffering-bufsize
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set buffer size for read() in post buffering mode

----body-read-warning
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the amount of allowed memory allocation (in megabytes) for request body before starting printing a warning

----upload-progress
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



enable creation of .json files in the specified directory during a file upload

----no-default-app
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not fallback to default app

----manage-script-name
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



automatically rewrite SCRIPT_NAME and PATH_INFO

----ignore-script-name
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



ignore SCRIPT_NAME

----catch-exceptions
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



report exception as http output (discouraged, use only for testing)

----reload-on-exception
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



reload a worker when an exception is raised

----reload-on-exception-type
************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



reload a worker when a specific exception type is raised

----reload-on-exception-value
*************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



reload a worker when a specific exception value is raised

----reload-on-exception-repr
************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



reload a worker when a specific exception type+value (language-specific) is raised

----exception-handler
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



add an exception handler

----enable-metrics
**************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



enable metrics subsystem

----metric
******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



add a custom metric

----metric-threshold
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



add a metric threshold/alarm

----metric-alarm
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



add a metric threshold/alarm

----alarm-metric
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



add a metric threshold/alarm

----metrics-dir
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



export metrics as text files to the specified directory

----metrics-dir-restore
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



restore last value taken from the metrics dir

----metric-dir
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



export metrics as text files to the specified directory

----metric-dir-restore
******************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



restore last value taken from the metrics dir

----metrics-no-cores
****************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_METRICS|UWSGI_OPT_MASTER



disable generation of cores-related metrics

----udp
***
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



run the udp server on the specified address

----stats
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



enable the stats server on the specified address

----stats-server
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



enable the stats server on the specified address

----stats-http
**********
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



prefix stats server json output with http headers

----stats-minified
**************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



minify statistics json output

----stats-min
*********
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



minify statistics json output

----stats-push
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER|UWSGI_OPT_METRICS



push the stats json to the specified destination

----stats-pusher-default-freq
*************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set the default frequency of stats pushers

----stats-pushers-default-freq
**************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set the default frequency of stats pushers

----stats-no-cores
**************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



disable generation of cores-related stats

----stats-no-metrics
****************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



do not include metrics in stats output

----multicast
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



subscribe to specified multicast group

----multicast-ttl
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set multicast ttl

----multicast-loop
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set multicast loop (default 1)

----master-fifo
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



enable the master fifo

----notify-socket
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



enable the notification socket

----subscription-notify-socket
**************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



set the notification socket for subscriptions

----legion
******
``argument``: required_argument

``parser``: uwsgi_opt_legion

``flags``: UWSGI_OPT_MASTER



became a member of a legion

----legion-mcast
************
``argument``: required_argument

``parser``: uwsgi_opt_legion_mcast

``flags``: UWSGI_OPT_MASTER



became a member of a legion (shortcut for multicast)

----legion-node
***********
``argument``: required_argument

``parser``: uwsgi_opt_legion_node

``flags``: UWSGI_OPT_MASTER



add a node to a legion

----legion-freq
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set the frequency of legion packets

----legion-tolerance
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set the tolerance of legion subsystem

----legion-death-on-lord-error
**************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



declare itself as a dead node for the specified amount of seconds if one of the lord hooks fails

----legion-skew-tolerance
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set the clock skew tolerance of legion subsystem (default 30 seconds)

----legion-lord
***********
``argument``: required_argument

``parser``: uwsgi_opt_legion_hook

``flags``: UWSGI_OPT_MASTER



action to call on Lord election

----legion-unlord
*************
``argument``: required_argument

``parser``: uwsgi_opt_legion_hook

``flags``: UWSGI_OPT_MASTER



action to call on Lord dismiss

----legion-setup
************
``argument``: required_argument

``parser``: uwsgi_opt_legion_hook

``flags``: UWSGI_OPT_MASTER



action to call on legion setup

----legion-death
************
``argument``: required_argument

``parser``: uwsgi_opt_legion_hook

``flags``: UWSGI_OPT_MASTER



action to call on legion death (shutdown of the instance)

----legion-join
***********
``argument``: required_argument

``parser``: uwsgi_opt_legion_hook

``flags``: UWSGI_OPT_MASTER



action to call on legion join (first time quorum is reached)

----legion-node-joined
******************
``argument``: required_argument

``parser``: uwsgi_opt_legion_hook

``flags``: UWSGI_OPT_MASTER



action to call on new node joining legion

----legion-node-left
****************
``argument``: required_argument

``parser``: uwsgi_opt_legion_hook

``flags``: UWSGI_OPT_MASTER



action to call node leaving legion

----legion-quorum
*************
``argument``: required_argument

``parser``: uwsgi_opt_legion_quorum

``flags``: UWSGI_OPT_MASTER



set the quorum of a legion

----legion-scroll
*************
``argument``: required_argument

``parser``: uwsgi_opt_legion_scroll

``flags``: UWSGI_OPT_MASTER



set the scroll of a legion

----legion-scroll-max-size
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_16bit



set max size of legion scroll buffer

----legion-scroll-list-max-size
***************************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set max size of legion scroll list buffer

----subscriptions-sign-check
************************
``argument``: required_argument

``parser``: uwsgi_opt_scd

``flags``: UWSGI_OPT_MASTER



set digest algorithm and certificate directory for secured subscription system

----subscriptions-sign-check-tolerance
**********************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set the maximum tolerance (in seconds) of clock skew for secured subscription system

----subscriptions-sign-skip-uid
***************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



skip signature check for the specified uid when using unix sockets credentials

----subscriptions-credentials-check
*******************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



add a directory to search for subscriptions key credentials

----subscriptions-use-credentials
*****************************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable management of SCM_CREDENTIALS in subscriptions UNIX sockets

----subscription-algo
*****************
``argument``: required_argument

``parser``: uwsgi_opt_ssa



set load balancing algorithm for the subscription system

----subscription-dotsplit
*********************
``argument``: no_argument

``parser``: uwsgi_opt_true



try to fallback to the next part (dot based) in subscription key

----subscribe-to
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



subscribe to the specified subscription server

----st
**
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



subscribe to the specified subscription server

----subscribe
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



subscribe to the specified subscription server

----subscribe2
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



subscribe to the specified subscription server using advanced keyval syntax

----subscribe-freq
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



send subscription announce at the specified interval

----subscription-tolerance
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set tolerance for subscription servers

----unsubscribe-on-graceful-reload
******************************
``argument``: no_argument

``parser``: uwsgi_opt_true



force unsubscribe request even during graceful reload

----start-unsubscribed
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



configure subscriptions but do not send them (useful with master fifo)

----snmp
****
``argument``: optional_argument

``parser``: uwsgi_opt_snmp



enable the embedded snmp server

----snmp-community
**************
``argument``: required_argument

``parser``: uwsgi_opt_snmp_community



set the snmp community string

----ssl-verbose
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



be verbose about SSL errors

----ssl-sessions-use-cache
**********************
``argument``: optional_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



use uWSGI cache for ssl sessions storage

----ssl-session-use-cache
*********************
``argument``: optional_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



use uWSGI cache for ssl sessions storage

----ssl-sessions-timeout
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set SSL sessions timeout (default: 300 seconds)

----ssl-session-timeout
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set SSL sessions timeout (default: 300 seconds)

----sni
***
``argument``: required_argument

``parser``: uwsgi_opt_sni



add an SNI-governed SSL context

----sni-dir
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



check for cert/key/client_ca file in the specified directory and create a sni/ssl context on demand

----sni-dir-ciphers
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set ssl ciphers for sni-dir option

----sni-regexp
**********
``argument``: required_argument

``parser``: uwsgi_opt_sni



add an SNI-governed SSL context (the key is a regexp)

----ssl-tmp-dir
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



store ssl-related temp files in the specified directory

----check-interval
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set the interval (in seconds) of master checks

----forkbomb-delay
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



sleep for the specified number of seconds when a forkbomb is detected

----binary-path
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force binary path

----privileged-binary-patch
***********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



patch the uwsgi binary with a new command (before privileges drop)

----unprivileged-binary-patch
*************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



patch the uwsgi binary with a new command (after privileges drop)

----privileged-binary-patch-arg
***************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



patch the uwsgi binary with a new command and arguments (before privileges drop)

----unprivileged-binary-patch-arg
*****************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



patch the uwsgi binary with a new command and arguments (after privileges drop)

----async
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable async mode with specified cores

----max-fd
******
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set maximum number of file descriptors (requires root privileges)

----logto
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set logfile/udp address

----logto2
******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



log to specified file or udp address after privileges drop

----log-format
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set advanced format for request logging

----logformat
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set advanced format for request logging

----logformat-strftime
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



apply strftime to logformat output

----log-format-strftime
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



apply strftime to logformat output

----logfile-chown
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



chown logfiles

----logfile-chmod
*************
``argument``: required_argument

``parser``: uwsgi_opt_logfile_chmod



chmod logfiles

----log-syslog
**********
``argument``: optional_argument

``parser``: uwsgi_opt_set_logger

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



log to syslog

----log-socket
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_logger

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



send logs to the specified socket

----req-logger
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_req_logger

``flags``: UWSGI_OPT_REQ_LOG_MASTER



set/append a request logger

----logger-req
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_req_logger

``flags``: UWSGI_OPT_REQ_LOG_MASTER



set/append a request logger

----logger
******
``argument``: required_argument

``parser``: uwsgi_opt_set_logger

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



set/append a logger

----logger-list
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled loggers

----loggers-list
************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled loggers

----threaded-logger
***************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



offload log writing to a thread

----log-encoder
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



add an item in the log encoder chain

----log-req-encoder
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



add an item in the log req encoder chain

----log-drain
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



drain (do not show) log lines matching the specified regexp

----log-filter
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



show only log lines matching the specified regexp

----log-route
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_custom_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



log to the specified named logger if regexp applied on logline matches

----log-req-route
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_custom_list

``flags``: UWSGI_OPT_REQ_LOG_MASTER



log requests to the specified named logger if regexp applied on logline matches

----use-abort
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



call abort() on segfault/fpe, could be useful for generating a core dump

----alarm
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



create a new alarm, syntax: <alarm> <plugin:args>

----alarm-cheap
***********
``argument``: required_argument

``parser``: uwsgi_opt_true



use main alarm thread rather than create dedicated threads for curl-based alarms

----alarm-freq
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



tune the anti-loop alam system (default 3 seconds)

----alarm-fd
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when an fd is read for read (by default it reads 1 byte, set 8 for eventfd)

----alarm-segfault
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the segmentation fault handler is executed

----segfault-alarm
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the segmentation fault handler is executed

----alarm-backlog
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the socket backlog queue is full

----backlog-alarm
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the socket backlog queue is full

----lq-alarm
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the socket backlog queue is full

----alarm-lq
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the socket backlog queue is full

----alarm-listen-queue
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the socket backlog queue is full

----listen-queue-alarm
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



raise the specified alarm when the socket backlog queue is full

----log-alarm
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



raise the specified alarm when a log line matches the specified regexp, syntax: <alarm>[,alarm...] <regexp>

----alarm-log
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



raise the specified alarm when a log line matches the specified regexp, syntax: <alarm>[,alarm...] <regexp>

----not-log-alarm
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list_custom

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



skip the specified alarm when a log line matches the specified regexp, syntax: <alarm>[,alarm...] <regexp>

----not-alarm-log
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list_custom

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



skip the specified alarm when a log line matches the specified regexp, syntax: <alarm>[,alarm...] <regexp>

----alarm-list
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled alarms

----alarms-list
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled alarms

----alarm-msg-size
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the max size of an alarm message (default 8192)

----log-master
**********
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



delegate logging to master process

----log-master-bufsize
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the buffer size for the master logger. bigger log messages will be truncated

----log-master-stream
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



create the master logpipe as SOCK_STREAM

----log-master-req-stream
*********************
``argument``: no_argument

``parser``: uwsgi_opt_true



create the master requests logpipe as SOCK_STREAM

----log-reopen
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



reopen log after reload

----log-truncate
************
``argument``: no_argument

``parser``: uwsgi_opt_true



truncate log on startup

----log-maxsize
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit

``flags``: UWSGI_OPT_LOG_MASTER



set maximum logfile size

----log-backupname
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set logfile name after rotation

----logdate
*******
``argument``: optional_argument

``parser``: uwsgi_opt_log_date



prefix logs with date or a strftime string

----log-date
********
``argument``: optional_argument

``parser``: uwsgi_opt_log_date



prefix logs with date or a strftime string

----log-prefix
**********
``argument``: optional_argument

``parser``: uwsgi_opt_log_date



prefix logs with a string

----log-zero
********
``argument``: no_argument

``parser``: uwsgi_opt_true



log responses without body

----log-slow
********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



log requests slower than the specified number of milliseconds

----log-4xx
*******
``argument``: no_argument

``parser``: uwsgi_opt_true



log requests with a 4xx response

----log-5xx
*******
``argument``: no_argument

``parser``: uwsgi_opt_true



log requests with a 5xx response

----log-big
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



log requestes bigger than the specified size

----log-sendfile
************
``argument``: required_argument

``parser``: uwsgi_opt_true



log sendfile requests

----log-ioerror
***********
``argument``: required_argument

``parser``: uwsgi_opt_true



log requests with io errors

----log-micros
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



report response time in microseconds instead of milliseconds

----log-x-forwarded-for
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



use the ip from X-Forwarded-For header instead of REMOTE_ADDR

----master-as-root
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



leave master process running as root

----drop-after-init
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



run privileges drop after plugin initialization

----drop-after-apps
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



run privileges drop after apps loading

----force-cwd
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force the initial working directory to the specified value

----binsh
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



override /bin/sh (used by exec hooks, it always fallback to /bin/sh)

----chdir
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



chdir to specified directory before apps loading

----chdir2
******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



chdir to specified directory after apps loading

----lazy
****
``argument``: no_argument

``parser``: uwsgi_opt_true



set lazy mode (load apps in workers instead of master)

----lazy-apps
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



load apps in each worker instead of the master

----cheap
*****
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



set cheap mode (spawn workers only after the first request)

----cheaper
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_CHEAPER



set cheaper mode (adaptive process spawning)

----cheaper-initial
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_CHEAPER



set the initial number of processes to spawn in cheaper mode

----cheaper-algo
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



choose to algorithm used for adaptive process spawning

----cheaper-step
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_CHEAPER



number of additional processes to spawn at each overload

----cheaper-overload
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_CHEAPER



increase workers after specified overload

----cheaper-algo-list
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled cheapers algorithms

----cheaper-algos-list
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled cheapers algorithms

----cheaper-list
************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled cheapers algorithms

----cheaper-rss-limit-soft
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_CHEAPER



don't spawn new workers if total resident memory usage of all workers is higher than this limit

----cheaper-rss-limit-hard
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_CHEAPER



if total workers resident memory usage is higher try to stop workers

----idle
****
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



set idle mode (put uWSGI in cheap mode after inactivity)

----die-on-idle
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



shutdown uWSGI when idle

----mount
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load application under mountpoint

----worker-mount
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load application under mountpoint in the specified worker or after workers spawn

----threads
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS



run each worker in prethreaded mode with the specified number of threads

----thread-stacksize
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS



set threads stacksize

----threads-stacksize
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS



set threads stacksize

----thread-stack-size
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS



set threads stacksize

----threads-stack-size
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS



set threads stacksize

----vhost
*****
``argument``: no_argument

``parser``: uwsgi_opt_true



enable virtualhosting mode (based on SERVER_NAME variable)

----vhost-host
**********
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_VHOST



enable virtualhosting mode (based on HTTP_HOST variable)

----route
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route

----route-host
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on Host header

----route-uri
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on REQUEST_URI

----route-qs
********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on QUERY_STRING

----route-remote-addr
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on REMOTE_ADDR

----route-user-agent
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on HTTP_USER_AGENT

----route-remote-user
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on REMOTE_USER

----route-referer
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on HTTP_REFERER

----route-label
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a routing label (for use with goto)

----route-if
********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on condition

----route-if-not
************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a route based on condition (negate version)

----route-run
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



always run the specified route action

----final-route
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route

----final-route-status
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route for the specified status

----final-route-host
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on Host header

----final-route-uri
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on REQUEST_URI

----final-route-qs
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on QUERY_STRING

----final-route-remote-addr
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on REMOTE_ADDR

----final-route-user-agent
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on HTTP_USER_AGENT

----final-route-remote-user
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on REMOTE_USER

----final-route-referer
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on HTTP_REFERER

----final-route-label
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final routing label (for use with goto)

----final-route-if
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on condition

----final-route-if-not
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a final route based on condition (negate version)

----final-route-run
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



always run the specified final route action

----error-route
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route

----error-route-status
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route for the specified status

----error-route-host
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on Host header

----error-route-uri
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on REQUEST_URI

----error-route-qs
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on QUERY_STRING

----error-route-remote-addr
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on REMOTE_ADDR

----error-route-user-agent
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on HTTP_USER_AGENT

----error-route-remote-user
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on REMOTE_USER

----error-route-referer
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on HTTP_REFERER

----error-route-label
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error routing label (for use with goto)

----error-route-if
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on condition

----error-route-if-not
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add an error route based on condition (negate version)

----error-route-run
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



always run the specified error route action

----response-route
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route

----response-route-status
*********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route for the specified status

----response-route-host
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on Host header

----response-route-uri
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on REQUEST_URI

----response-route-qs
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on QUERY_STRING

----response-route-remote-addr
**************************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on REMOTE_ADDR

----response-route-user-agent
*************************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on HTTP_USER_AGENT

----response-route-remote-user
**************************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on REMOTE_USER

----response-route-referer
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on HTTP_REFERER

----response-route-label
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response routing label (for use with goto)

----response-route-if
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on condition

----response-route-if-not
*********************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



add a response route based on condition (negate version)

----response-route-run
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_route



always run the specified response route action

----router-list
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled routers

----routers-list
************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled routers

----error-page-403
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an error page (html) for managed 403 response

----error-page-404
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an error page (html) for managed 404 response

----error-page-500
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an error page (html) for managed 500 response

----websockets-ping-freq
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the frequency (in seconds) of websockets automatic ping packets

----websocket-ping-freq
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the frequency (in seconds) of websockets automatic ping packets

----websockets-pong-tolerance
*************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the tolerance (in seconds) of websockets ping/pong subsystem

----websocket-pong-tolerance
************************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the tolerance (in seconds) of websockets ping/pong subsystem

----websockets-max-size
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the max allowed size of websocket messages (in Kbytes, default 1024)

----websocket-max-size
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the max allowed size of websocket messages (in Kbytes, default 1024)

----chunked-input-limit
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the max size of a chunked input part (default 1MB, in bytes)

----chunked-input-timeout
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set default timeout for chunked input

----clock
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set a clock source

----clock-list
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled clocks

----clocks-list
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled clocks

----add-header
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



automatically add HTTP headers to response

----rem-header
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



automatically remove specified HTTP header from the response

----del-header
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



automatically remove specified HTTP header from the response

----collect-header
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



store the specified response header in a request var (syntax: header var)

----response-header-collect
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



store the specified response header in a request var (syntax: header var)

----check-static
************
``argument``: required_argument

``parser``: uwsgi_opt_check_static

``flags``: UWSGI_OPT_MIME



check for static files in the specified directory

----check-static-docroot
********************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MIME



check for static files in the requested DOCUMENT_ROOT

----static-check
************
``argument``: required_argument

``parser``: uwsgi_opt_check_static

``flags``: UWSGI_OPT_MIME



check for static files in the specified directory

----static-map
**********
``argument``: required_argument

``parser``: uwsgi_opt_static_map

``flags``: UWSGI_OPT_MIME



map mountpoint to static directory (or file)

----static-map2
***********
``argument``: required_argument

``parser``: uwsgi_opt_static_map

``flags``: UWSGI_OPT_MIME



like static-map but completely appending the requested resource to the docroot

----static-skip-ext
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



skip specified extension from staticfile checks

----static-index
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



search for specified file if a directory is requested

----static-safe
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



skip security checks if the file is under the specified path

----static-cache-paths
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MIME|UWSGI_OPT_MASTER



put resolved paths in the uWSGI cache for the specified amount of seconds

----static-cache-paths-name
***********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MIME|UWSGI_OPT_MASTER



use the specified cache for static paths

----mimefile
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



set mime types file path (default /etc/apache2/mime.types)

----mime-file
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



set mime types file path (default /etc/apache2/mime.types)

----mimefile
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



set mime types file path (default /etc/mime.types)

----mime-file
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



set mime types file path (default /etc/mime.types)

----static-expires-type
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on content type

----static-expires-type-mtime
*************************
``argument``: required_argument

``parser``: uwsgi_opt_add_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on content type and file mtime

----static-expires
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on filename regexp

----static-expires-mtime
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on filename regexp and file mtime

----static-expires-uri
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on REQUEST_URI regexp

----static-expires-uri-mtime
************************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on REQUEST_URI regexp and file mtime

----static-expires-path-info
************************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on PATH_INFO regexp

----static-expires-path-info-mtime
******************************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_dyn_dict

``flags``: UWSGI_OPT_MIME



set the Expires header based on PATH_INFO regexp and file mtime

----static-gzip
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_list

``flags``: UWSGI_OPT_MIME



if the supplied regexp matches the static file translation it will search for a gzip version

----static-gzip-all
***************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MIME



check for a gzip version of all requested static files

----static-gzip-dir
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



check for a gzip version of all requested static files in the specified dir/prefix

----static-gzip-prefix
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



check for a gzip version of all requested static files in the specified dir/prefix

----static-gzip-ext
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



check for a gzip version of all requested static files with the specified ext/suffix

----static-gzip-suffix
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



check for a gzip version of all requested static files with the specified ext/suffix

----honour-range
************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable support for the HTTP Range header

----offload-threads
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the number of offload threads to spawn (per-worker, default 0)

----offload-thread
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the number of offload threads to spawn (per-worker, default 0)

----file-serve-mode
***************
``argument``: required_argument

``parser``: uwsgi_opt_fileserve_mode

``flags``: UWSGI_OPT_MIME



set static file serving mode

----fileserve-mode
**************
``argument``: required_argument

``parser``: uwsgi_opt_fileserve_mode

``flags``: UWSGI_OPT_MIME



set static file serving mode

----disable-sendfile
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable sendfile() and rely on boring read()/write()

----check-cache
***********
``argument``: optional_argument

``parser``: uwsgi_opt_set_str



check for response data in the specified cache (empty for default cache)

----close-on-exec
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



set close-on-exec on connection sockets (could be required for spawning processes in requests)

----close-on-exec2
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



set close-on-exec on server sockets (could be required for spawning processes in requests)

----mode
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set uWSGI custom mode

----env
***
``argument``: required_argument

``parser``: uwsgi_opt_set_env



set environment variable

----envdir
******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a daemontools compatible envdir

----early-envdir
************
``argument``: required_argument

``parser``: uwsgi_opt_envdir

``flags``: UWSGI_OPT_IMMEDIATE



load a daemontools compatible envdir ASAP

----unenv
*****
``argument``: required_argument

``parser``: uwsgi_opt_unset_env



unset environment variable

----vacuum
******
``argument``: no_argument

``parser``: uwsgi_opt_true



try to remove all of the generated file/sockets

----file-write
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



write the specified content to the specified file (syntax: file=value) before privileges drop

----cgroup
******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



put the processes in the specified cgroup

----cgroup-opt
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



set value in specified cgroup option

----cgroup-dir-mode
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set permission for cgroup directory (default is 700)

----namespace
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run in a new namespace under the specified rootfs

----namespace-keep-mount
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



keep the specified mountpoint in your namespace

----ns
**
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run in a new namespace under the specified rootfs

----namespace-net
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



add network namespace

----ns-net
******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



add network namespace

----enable-proxy-protocol
*********************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable PROXY1 protocol support (only for http parsers)

----reuse-port
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



enable REUSE_PORT flag on socket (BSD only)

----tcp-fast-open
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable TCP_FASTOPEN flag on TCP sockets with the specified qlen value

----tcp-fastopen
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable TCP_FASTOPEN flag on TCP sockets with the specified qlen value

----tcp-fast-open-client
********************
``argument``: no_argument

``parser``: uwsgi_opt_true



use sendto(..., MSG_FASTOPEN, ...) instead of connect() if supported

----tcp-fastopen-client
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



use sendto(..., MSG_FASTOPEN, ...) instead of connect() if supported

----zerg
****
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



attach to a zerg server

----zerg-fallback
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



fallback to normal sockets if the zerg server is not available

----zerg-server
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MASTER



enable the zerg server on the specified UNIX socket

----cron
****
``argument``: required_argument

``parser``: uwsgi_opt_add_cron

``flags``: UWSGI_OPT_MASTER



add a cron task

----cron2
*****
``argument``: required_argument

``parser``: uwsgi_opt_add_cron2

``flags``: UWSGI_OPT_MASTER



add a cron task (key=val syntax)

----unique-cron
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_unique_cron

``flags``: UWSGI_OPT_MASTER



add a unique cron task

----cron-harakiri
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum time (in seconds) we wait for cron command to complete

----legion-cron
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_legion_cron

``flags``: UWSGI_OPT_MASTER



add a cron task runnable only when the instance is a lord of the specified legion

----cron-legion
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_legion_cron

``flags``: UWSGI_OPT_MASTER



add a cron task runnable only when the instance is a lord of the specified legion

----unique-legion-cron
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_unique_legion_cron

``flags``: UWSGI_OPT_MASTER



add a unique cron task runnable only when the instance is a lord of the specified legion

----unique-cron-legion
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_unique_legion_cron

``flags``: UWSGI_OPT_MASTER



add a unique cron task runnable only when the instance is a lord of the specified legion

----loop
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



select the uWSGI loop engine

----loop-list
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled loop engines

----loops-list
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled loop engines

----worker-exec
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command as worker

----worker-exec2
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command as worker (after post_fork hook)

----attach-daemon
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon

``flags``: UWSGI_OPT_MASTER



attach a command/daemon to the master process (the command has to not go in background)

----attach-control-daemon
*********************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon

``flags``: UWSGI_OPT_MASTER



attach a command/daemon to the master process (the command has to not go in background), when the daemon dies, the master dies too

----smart-attach-daemon
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon

``flags``: UWSGI_OPT_MASTER



attach a command/daemon to the master process managed by a pidfile (the command has to daemonize)

----smart-attach-daemon2
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon

``flags``: UWSGI_OPT_MASTER



attach a command/daemon to the master process managed by a pidfile (the command has to NOT daemonize)

----legion-attach-daemon
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon

``flags``: UWSGI_OPT_MASTER



same as --attach-daemon but daemon runs only on legion lord node

----legion-smart-attach-daemon
**************************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon

``flags``: UWSGI_OPT_MASTER



same as --smart-attach-daemon but daemon runs only on legion lord node

----legion-smart-attach-daemon2
***************************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon

``flags``: UWSGI_OPT_MASTER



same as --smart-attach-daemon2 but daemon runs only on legion lord node

----daemons-honour-stdin
********************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MASTER



do not change the stdin of external daemons to /dev/null

----attach-daemon2
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_daemon2

``flags``: UWSGI_OPT_MASTER



attach-daemon keyval variant (supports smart modes too)

----plugins
*******
``argument``: required_argument

``parser``: uwsgi_opt_load_plugin

``flags``: UWSGI_OPT_IMMEDIATE



load uWSGI plugins

----plugin
******
``argument``: required_argument

``parser``: uwsgi_opt_load_plugin

``flags``: UWSGI_OPT_IMMEDIATE



load uWSGI plugins

----need-plugins
************
``argument``: required_argument

``parser``: uwsgi_opt_load_plugin

``flags``: UWSGI_OPT_IMMEDIATE



load uWSGI plugins (exit on error)

----need-plugin
***********
``argument``: required_argument

``parser``: uwsgi_opt_load_plugin

``flags``: UWSGI_OPT_IMMEDIATE



load uWSGI plugins (exit on error)

----plugins-dir
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_IMMEDIATE



add a directory to uWSGI plugin search path

----plugin-dir
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_IMMEDIATE



add a directory to uWSGI plugin search path

----plugins-list
************
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled plugins

----plugin-list
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



list enabled plugins

----autoload
********
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_IMMEDIATE



try to automatically load plugins when unknown options are found

----dlopen
******
``argument``: required_argument

``parser``: uwsgi_opt_load_dl

``flags``: UWSGI_OPT_IMMEDIATE



blindly load a shared library

----allowed-modifiers
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



comma separated list of allowed modifiers

----remap-modifier
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



remap request modifier from one id to another

----dump-options
************
``argument``: no_argument

``parser``: uwsgi_opt_true



dump the full list of available options

----show-config
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



show the current config reformatted as ini

----binary-append-data
******************
``argument``: required_argument

``parser``: uwsgi_opt_binary_append_data

``flags``: UWSGI_OPT_IMMEDIATE



return the content of a resource to stdout for appending to a uwsgi binary (for data:// usage)

----print
*****
``argument``: required_argument

``parser``: uwsgi_opt_print



simple print

----iprint
******
``argument``: required_argument

``parser``: uwsgi_opt_print

``flags``: UWSGI_OPT_IMMEDIATE



simple print (immediate version)

----exit
****
``argument``: optional_argument

``parser``: uwsgi_opt_exit

``flags``: UWSGI_OPT_IMMEDIATE



force exit() of the instance

----cflags
******
``argument``: no_argument

``parser``: uwsgi_opt_cflags

``flags``: UWSGI_OPT_IMMEDIATE



report uWSGI CFLAGS (useful for building external plugins)

----dot-h
*****
``argument``: no_argument

``parser``: uwsgi_opt_dot_h

``flags``: UWSGI_OPT_IMMEDIATE



dump the uwsgi.h used for building the core  (useful for building external plugins)

----config-py
*********
``argument``: no_argument

``parser``: uwsgi_opt_config_py

``flags``: UWSGI_OPT_IMMEDIATE



dump the uwsgiconfig.py used for building the core  (useful for building external plugins)

----build-plugin
************
``argument``: required_argument

``parser``: uwsgi_opt_build_plugin

``flags``: UWSGI_OPT_IMMEDIATE



build a uWSGI plugin for the current binary

----version
*******
``argument``: no_argument

``parser``: uwsgi_opt_print



print uWSGI version


plugin: airbrake
================

plugin: alarm_curl
==================

plugin: alarm_speech
====================

plugin: alarm_xmpp
==================

plugin: asyncio
===============
----asyncio
*******
``argument``: required_argument

``parser``: uwsgi_opt_setup_asyncio

``flags``: UWSGI_OPT_THREADS



a shortcut enabling asyncio loop engine with the specified number of async cores and optimal parameters


plugin: cache
=============

plugin: carbon
==============
----carbon
******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



push statistics to the specified carbon server

----carbon-timeout
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set carbon connection timeout in seconds (default 3)

----carbon-freq
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set carbon push frequency in seconds (default 60)

----carbon-id
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set carbon id

----carbon-no-workers
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable generation of single worker metrics

----carbon-max-retry
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set maximum number of retries in case of connection errors (default 1)

----carbon-retry-delay
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set connection retry delay in seconds (default 7)

----carbon-root
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set carbon metrics root node (default 'uwsgi')

----carbon-hostname-dots
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set char to use as a replacement for dots in hostname (dots are not replaced by default)

----carbon-name-resolve
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



allow using hostname as carbon server address (default disabled)

----carbon-resolve-names
********************
``argument``: no_argument

``parser``: uwsgi_opt_true



allow using hostname as carbon server address (default disabled)

----carbon-idle-avg
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



average values source during idle period (no requests), can be "last", "zero", "none" (default is last)

----carbon-use-metrics
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



don't compute all statistics, use metrics subsystem data instead (warning! key names will be different)


plugin: cgi
===========
----cgi
***
``argument``: required_argument

``parser``: uwsgi_opt_add_cgi



add a cgi mountpoint/directory/script

----cgi-map-helper
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_cgi_maphelper



add a cgi map-helper

----cgi-helper
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_cgi_maphelper



add a cgi map-helper

----cgi-from-docroot
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



blindly enable cgi in DOCUMENT_ROOT

----cgi-buffer-size
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set cgi buffer size

----cgi-timeout
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set cgi script timeout

----cgi-index
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a cgi index file

----cgi-allowed-ext
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



cgi allowed extension

----cgi-unset
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



unset specified environment variables

----cgi-loadlib
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a cgi shared library/optimizer

----cgi-optimize
************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable cgi realpath() optimizer

----cgi-optimized
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable cgi realpath() optimizer

----cgi-path-info
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



disable PATH_INFO management in cgi scripts

----cgi-do-not-kill-on-error
************************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not send SIGKILL to cgi script on errors

----cgi-async-max-attempts
**********************
``argument``: no_argument

``parser``: uwsgi_opt_set_int



max waitpid() attempts in cgi async mode (default 10)


plugin: cheaper_backlog2
========================

plugin: cheaper_busyness
========================

plugin: clock_monotonic
=======================

plugin: clock_realtime
======================

plugin: corerouter
==================

plugin: coroae
==============
----coroae
******
``argument``: required_argument

``parser``: uwsgi_opt_setup_coroae



a shortcut enabling Coro::AnyEvent loop engine with the specified number of async cores and optimal parameters


plugin: cplusplus
=================

plugin: curl_cron
=================
----curl-cron
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_cron_curl

``flags``: UWSGI_OPT_MASTER



add a cron task invoking the specified url via CURL

----cron-curl
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_cron_curl

``flags``: UWSGI_OPT_MASTER



add a cron task invoking the specified url via CURL

----legion-curl-cron
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_legion_cron_curl

``flags``: UWSGI_OPT_MASTER



add a cron task invoking the specified url via CURL runnable only when the instance is a lord of the specified legion

----legion-cron-curl
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_legion_cron_curl

``flags``: UWSGI_OPT_MASTER



add a cron task invoking the specified url via CURL runnable only when the instance is a lord of the specified legion

----curl-cron-legion
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_legion_cron_curl

``flags``: UWSGI_OPT_MASTER



add a cron task invoking the specified url via CURL runnable only when the instance is a lord of the specified legion

----cron-curl-legion
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_legion_cron_curl

``flags``: UWSGI_OPT_MASTER



add a cron task invoking the specified url via CURL runnable only when the instance is a lord of the specified legion


plugin: dumbloop
================
----dumbloop-modifier1
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the modifier1 for the code_string

----dumbloop-code
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the script to load for the code_string

----dumbloop-function
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the function to run for the code_string


plugin: dummy
=============

plugin: echo
============

plugin: emperor_amqp
====================

plugin: emperor_mongodb
=======================

plugin: emperor_pg
==================

plugin: emperor_zeromq
======================

plugin: example
===============

plugin: exception_log
=====================

plugin: fastrouter
==================
----fastrouter
**********
``argument``: required_argument

``parser``: uwsgi_opt_corerouter



run the fastrouter on the specified port

----fastrouter-processes
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of fastrouter processes

----fastrouter-workers
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of fastrouter processes

----fastrouter-zerg
***************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_zerg



attach the fastrouter to a zerg server

----fastrouter-use-cache
********************
``argument``: optional_argument

``parser``: uwsgi_opt_set_str



use uWSGI cache as hostname->server mapper for the fastrouter

----fastrouter-use-pattern
**********************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_pattern



use a pattern for fastrouter hostname->server mapping

----fastrouter-use-base
*******************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_base



use a base dir for fastrouter hostname->server mapping

----fastrouter-fallback
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



fallback to the specified node in case of error

----fastrouter-use-code-string
**************************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_cs



use code string as hostname->server mapper for the fastrouter

----fastrouter-use-socket
*********************
``argument``: optional_argument

``parser``: uwsgi_opt_corerouter_use_socket



forward request to the specified uwsgi socket

----fastrouter-to
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



forward requests to the specified uwsgi server (you can specify it multiple times for load balancing)

----fastrouter-gracetime
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



retry connections to dead static nodes after the specified amount of seconds

----fastrouter-events
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of concurrent events

----fastrouter-quiet
****************
``argument``: required_argument

``parser``: uwsgi_opt_true



do not report failed connections to instances

----fastrouter-cheap
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



run the fastrouter in cheap mode

----fastrouter-subscription-server
******************************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_ss



run the fastrouter subscription server on the specified address

----fastrouter-subscription-slot
****************************
``argument``: required_argument

``parser``: uwsgi_opt_deprecated



*** deprecated ***

----fastrouter-timeout
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set fastrouter timeout

----fastrouter-post-buffering
*************************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



enable fastrouter post buffering

----fastrouter-post-buffering-dir
*****************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



put fastrouter buffered files to the specified directory

----fastrouter-stats
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the fastrouter stats server

----fastrouter-stats-server
***********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the fastrouter stats server

----fastrouter-ss
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the fastrouter stats server

----fastrouter-harakiri
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable fastrouter harakiri

----fastrouter-uid
**************
``argument``: required_argument

``parser``: uwsgi_opt_uid



drop fastrouter privileges to the specified uid

----fastrouter-gid
**************
``argument``: required_argument

``parser``: uwsgi_opt_gid



drop fastrouter privileges to the specified gid

----fastrouter-resubscribe
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



forward subscriptions to the specified subscription server

----fastrouter-resubscribe-bind
***************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



bind to the specified address when re-subscribing

----fastrouter-buffer-size
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set internal buffer size (default: page size)


plugin: fiber
=============
----fiber
*****
``argument``: no_argument

``parser``: uwsgi_opt_true



enable ruby fiber as suspend engine


plugin: forkptyrouter
=====================
----forkptyrouter
*************
``argument``: required_argument

``parser``: uwsgi_opt_undeferred_corerouter



run the forkptyrouter on the specified address

----forkpty-router
**************
``argument``: required_argument

``parser``: uwsgi_opt_undeferred_corerouter



run the forkptyrouter on the specified address

----forkptyurouter
**************
``argument``: required_argument

``parser``: uwsgi_opt_forkpty_urouter



run the forkptyrouter on the specified address

----forkpty-urouter
***************
``argument``: required_argument

``parser``: uwsgi_opt_forkpty_urouter



run the forkptyrouter on the specified address

----forkptyrouter-command
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command on every connection (default: /bin/sh)

----forkpty-router-command
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command on every connection (default: /bin/sh)

----forkptyrouter-cmd
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command on every connection (default: /bin/sh)

----forkpty-router-cmd
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command on every connection (default: /bin/sh)

----forkptyrouter-rows
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_16bit



set forkptyrouter default pty window rows

----forkptyrouter-cols
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_16bit



set forkptyrouter default pty window cols

----forkptyrouter-processes
***********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of forkptyrouter processes

----forkptyrouter-workers
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of forkptyrouter processes

----forkptyrouter-zerg
******************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_zerg



attach the forkptyrouter to a zerg server

----forkptyrouter-fallback
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



fallback to the specified node in case of error

----forkptyrouter-events
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of concufptyent events

----forkptyrouter-cheap
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



run the forkptyrouter in cheap mode

----forkptyrouter-timeout
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set forkptyrouter timeout

----forkptyrouter-stats
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the forkptyrouter stats server

----forkptyrouter-stats-server
**************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the forkptyrouter stats server

----forkptyrouter-ss
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the forkptyrouter stats server

----forkptyrouter-harakiri
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable forkptyrouter harakiri


plugin: gccgo
=============
----go-load
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a go shared library in the process address space, eventually patching main.main and __go_init_main

----gccgo-load
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a go shared library in the process address space, eventually patching main.main and __go_init_main

----go-args
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set go commandline arguments

----gccgo-args
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set go commandline arguments

----goroutines
**********
``argument``: required_argument

``parser``: uwsgi_opt_setup_goroutines

``flags``: UWSGI_OPT_THREADS



a shortcut setting optimal options for goroutine-based apps, takes the number of max goroutines to spawn as argument


plugin: geoip
=============
----geoip-country
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load the specified geoip country database

----geoip-city
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load the specified geoip city database

----geoip-use-disk
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not cache geoip databases in memory


plugin: gevent
==============
----gevent
******
``argument``: required_argument

``parser``: uwsgi_opt_setup_gevent

``flags``: UWSGI_OPT_THREADS



a shortcut enabling gevent loop engine with the specified number of async cores and optimal parameters

----gevent-monkey-patch
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



call gevent.monkey.patch_all() automatically on startup

----gevent-wait-for-hub
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



wait for gevent hub's death instead of the control greenlet


plugin: glusterfs
=================
----glusterfs-mount
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



virtual mount the specified glusterfs volume in a uri

----glusterfs-timeout
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



timeout for glusterfs async mode


plugin: graylog2
================

plugin: greenlet
================
----greenlet
********
``argument``: no_argument

``parser``: uwsgi_opt_true



enable greenlet as suspend engine


plugin: gridfs
==============
----gridfs-mount
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



mount a gridfs db on the specified mountpoint

----gridfs-debug
************
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_MIME



report gridfs mountpoint and itemname for each request (debug)


plugin: http
============
----http
****
``argument``: required_argument

``parser``: uwsgi_opt_corerouter



add an http router/server on the specified address

----httprouter
**********
``argument``: required_argument

``parser``: uwsgi_opt_corerouter



add an http router/server on the specified address

----https
*****
``argument``: required_argument

``parser``: uwsgi_opt_https



add an https router/server on the specified address with specified certificate and key

----https2
******
``argument``: required_argument

``parser``: uwsgi_opt_https2



add an https/spdy router/server using keyval options

----https-export-cert
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



export uwsgi variable HTTPS_CC containing the raw client certificate

----https-session-context
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the session id context to the specified value

----http-to-https
*************
``argument``: required_argument

``parser``: uwsgi_opt_http_to_https



add an http router/server on the specified address and redirect all of the requests to https

----http-processes
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the number of http processes to spawn

----http-workers
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the number of http processes to spawn

----http-var
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a key=value item to the generated uwsgi packet

----http-to
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



forward requests to the specified node (you can specify it multiple time for lb)

----http-zerg
*********
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_zerg



attach the http router to a zerg server

----http-fallback
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



fallback to the specified node in case of error

----http-modifier1
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set uwsgi protocol modifier1

----http-modifier2
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set uwsgi protocol modifier2

----http-use-cache
**************
``argument``: optional_argument

``parser``: uwsgi_opt_set_str



use uWSGI cache as key->value virtualhost mapper

----http-use-pattern
****************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_pattern



use the specified pattern for mapping requests to unix sockets

----http-use-base
*************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_base



use the specified base for mapping requests to unix sockets

----http-events
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the number of concurrent http async events

----http-subscription-server
************************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_ss



enable the subscription server

----http-timeout
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set internal http socket timeout

----http-manage-expect
******************
``argument``: optional_argument

``parser``: uwsgi_opt_set_64bit



manage the Expect HTTP request header (optionally checking for Content-Length)

----http-keepalive
**************
``argument``: optional_argument

``parser``: uwsgi_opt_set_int



HTTP 1.1 keepalive support (non-pipelined) requests

----http-auto-chunked
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



automatically transform output to chunked encoding during HTTP 1.1 keepalive (if needed)

----http-auto-gzip
**************
``argument``: no_argument

``parser``: uwsgi_opt_true



automatically gzip content if uWSGI-Encoding header is set to gzip, but content size (Content-Length/Transfer-Encoding) and Content-Encoding are not specified

----http-raw-body
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



blindly send HTTP body to backends (required for WebSockets and Icecast support in backends)

----http-websockets
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



automatically detect websockets connections and put the session in raw mode

----http-use-code-string
********************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_cs



use code string as hostname->server mapper for the http router

----http-use-socket
***************
``argument``: optional_argument

``parser``: uwsgi_opt_corerouter_use_socket



forward request to the specified uwsgi socket

----http-gracetime
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



retry connections to dead static nodes after the specified amount of seconds

----http-quiet
**********
``argument``: required_argument

``parser``: uwsgi_opt_true



do not report failed connections to instances

----http-cheap
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



run the http router in cheap mode

----http-stats
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the http router stats server

----http-stats-server
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the http router stats server

----http-ss
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the http router stats server

----http-harakiri
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable http router harakiri

----http-stud-prefix
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_addr_list



expect a stud prefix (1byte family + 4/16 bytes address) on connections from the specified address

----http-uid
********
``argument``: required_argument

``parser``: uwsgi_opt_uid



drop http router privileges to the specified uid

----http-gid
********
``argument``: required_argument

``parser``: uwsgi_opt_gid



drop http router privileges to the specified gid

----http-resubscribe
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



forward subscriptions to the specified subscription server

----http-buffer-size
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set internal buffer size (default: page size)

----http-server-name-as-http-host
*****************************
``argument``: required_argument

``parser``: uwsgi_opt_true



force SERVER_NAME to HTTP_HOST

----http-headers-timeout
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set internal http socket timeout for headers

----http-connect-timeout
********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set internal http socket timeout for backend connections

----http-manage-source
******************
``argument``: optional_argument

``parser``: uwsgi_opt_true



manage the SOURCE HTTP method placing the session in raw mode

----http-enable-proxy-protocol
**************************
``argument``: optional_argument

``parser``: uwsgi_opt_true



manage PROXY protocol requests

----0x1f
****
``argument``: 0x8b

``shortcut``: -Z_DEFLATED



0


plugin: jvm
===========
----jvm-main-class
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load the specified class and call its main() function

----jvm-opt
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add the specified jvm option

----jvm-class
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load the specified class

----jvm-classpath
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add the specified directory to the classpath


plugin: jwsgi
=============
----jwsgi
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load the specified JWSGI application (syntax class:method)


plugin: ldap
============
----ldap
****
``argument``: required_argument

``parser``: uwsgi_opt_load_ldap

``flags``: UWSGI_OPT_IMMEDIATE



load configuration from ldap server

----ldap-schema
***********
``argument``: no_argument

``parser``: uwsgi_opt_ldap_dump

``flags``: UWSGI_OPT_IMMEDIATE



dump uWSGI ldap schema

----ldap-schema-ldif
****************
``argument``: no_argument

``parser``: uwsgi_opt_ldap_dump_ldif

``flags``: UWSGI_OPT_IMMEDIATE



dump uWSGI ldap schema in ldif format


plugin: legion_cache_fetch
==========================

plugin: libffi
==============

plugin: libtcc
==============

plugin: logcrypto
=================

plugin: logfile
===============

plugin: logpipe
===============

plugin: logsocket
=================

plugin: logzmq
==============
----log-zeromq
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_logger

``flags``: UWSGI_OPT_MASTER | UWSGI_OPT_LOG_MASTER



send logs to a zeromq server


plugin: lua
===========
----lua
***
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load lua wsapi app

----lua-load
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a lua file

----lua-shell
*********
``argument``: no_argument

``parser``: uwsgi_opt_luashell



run the lua interactive shell (debug.debug())

----luashell
********
``argument``: no_argument

``parser``: uwsgi_opt_luashell



run the lua interactive shell (debug.debug())

----lua-gc-freq
***********
``argument``: no_argument

``parser``: uwsgi_opt_set_int



set the lua gc frequency (default: 0, runs after every request)


plugin: matheval
================

plugin: mongodb
===============

plugin: mongodblog
==================

plugin: mongrel2
================
----zeromq
******
``argument``: required_argument

``parser``: uwsgi_opt_add_lazy_socket



create a mongrel2/zeromq pub/sub pair

----zmq
***
``argument``: required_argument

``parser``: uwsgi_opt_add_lazy_socket



create a mongrel2/zeromq pub/sub pair

----zeromq-socket
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_lazy_socket



create a mongrel2/zeromq pub/sub pair

----zmq-socket
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_lazy_socket



create a mongrel2/zeromq pub/sub pair

----mongrel2
********
``argument``: required_argument

``parser``: uwsgi_opt_add_lazy_socket



create a mongrel2/zeromq pub/sub pair


plugin: mono
============
----mono-app
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a Mono asp.net app from the specified directory

----mono-gc-freq
************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



run the Mono GC every <n> requests (default: run after every request)

----mono-key
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



select the ApplicationHost based on the specified CGI var

----mono-version
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the Mono jit version

----mono-config
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the Mono config file

----mono-assembly
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load the specified main assembly (default: uwsgi.dll)

----mono-exec
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



exec the specified assembly just before app loading

----mono-index
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an asp.net index file


plugin: msgpack
===============

plugin: nagios
==============
----nagios
******
``argument``: no_argument

``parser``: uwsgi_opt_true

``flags``: UWSGI_OPT_NO_INITIAL



nagios check


plugin: notfound
================
----notfound-log
************
``argument``: no_argument

``parser``: uwsgi_opt_true



log requests to the notfound plugin


plugin: objc_gc
===============

plugin: pam
===========
----pam
***
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the pam service name to use

----pam-user
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set a fake user for pam


plugin: php
===========
----php-ini
*******
``argument``: required_argument

``parser``: uwsgi_opt_php_ini



set php.ini path

----php-config
**********
``argument``: required_argument

``parser``: uwsgi_opt_php_ini



set php.ini path

----php-ini-append
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



set php.ini path (append mode)

----php-config-append
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



set php.ini path (append mode)

----php-set
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



set a php config directive

----php-index
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



list the php index files

----php-docroot
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force php DOCUMENT_ROOT

----php-allowed-docroot
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



list the allowed document roots

----php-allowed-ext
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



list the allowed php file extensions

----php-allowed-script
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



list the allowed php scripts (require absolute path)

----php-server-software
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force php SERVER_SOFTWARE

----php-app
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



force the php file to run at each request

----php-app-qs
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



when in app mode force QUERY_STRING to the specified value + REQUEST_URI

----php-fallback
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified php script when the request one does not exist

----php-app-bypass
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_regexp_list



if the regexp matches the uri the --php-app is bypassed

----php-var
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add/overwrite a CGI variable at each request

----php-dump-config
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



dump php config (if modified via --php-set or append options)

----php-exec-before
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run specified php code before the requested script

----php-exec-begin
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run specified php code before the requested script

----php-exec-after
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run specified php code after the requested script

----php-exec-end
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run specified php code after the requested script


plugin: ping
============
----ping
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_NO_INITIAL | UWSGI_OPT_NO_SERVER



ping specified uwsgi host

----ping-timeout
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set ping timeout


plugin: psgi
============
----psgi
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a psgi app

----psgi-enable-psgix-io
********************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable psgix.io support

----perl-no-die-catch
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



do not catch $SIG{__DIE__}

----perl-local-lib
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set perl locallib path

----perl-version
************
``argument``: no_argument

``parser``: uwsgi_opt_print

``flags``: UWSGI_OPT_IMMEDIATE



print perl version

----perl-args
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



add items (space separated) to @ARGV

----perl-arg
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an item to @ARGV

----perl-exec
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



exec the specified perl file before fork()

----perl-exec-post-fork
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



exec the specified perl file after fork()

----perl-auto-reload
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_MASTER



enable perl auto-reloader with the specified frequency

----perl-auto-reload-ignore
***********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER



ignore the specified files when auto-reload is enabled

----plshell
*******
``argument``: optional_argument

``parser``: uwsgi_opt_plshell



run a perl interactive shell

----plshell-oneshot
***************
``argument``: no_argument

``parser``: uwsgi_opt_plshell



run a perl interactive shell (one shot)

----perl-no-plack
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



force the use of do instead of Plack::Util::load_psgi


plugin: pty
===========
----pty-socket
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



bind the pty server on the specified address

----pty-log
*******
``argument``: no_argument

``parser``: uwsgi_opt_true



send stdout/stderr to the log engine too

----pty-input
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



read from original stdin in addition to pty

----pty-connect
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_NO_INITIAL



connect the current terminal to a pty server

----pty-uconnect
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_NO_INITIAL



connect the current terminal to a pty server (using uwsgi protocol)

----pty-no-isig
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



disable ISIG terminal attribute in client mode

----pty-exec
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the specified command soon after the pty thread is spawned


plugin: pypy
============
----pypy-lib
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the path/name of the pypy library

----pypy-setup
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the path of the python setup script

----pypy-home
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the home of pypy library

----pypy-wsgi
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a WSGI module

----pypy-wsgi-file
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a WSGI/mod_wsgi file

----pypy-ini-paste
**************
``argument``: required_argument

``parser``: uwsgi_opt_pypy_ini_paste

``flags``: UWSGI_OPT_IMMEDIATE



load a paste.deploy config file containing uwsgi section

----pypy-paste
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a paste.deploy config file

----pypy-eval
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



evaluate pypy code before fork()

----pypy-eval-post-fork
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



evaluate pypy code soon after fork()

----pypy-exec
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



execute pypy code from file before fork()

----pypy-exec-post-fork
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



execute pypy code from file soon after fork()

----pypy-pp
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an item to the pythonpath

----pypy-python-path
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an item to the pythonpath

----pypy-pythonpath
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add an item to the pythonpath


plugin: python
==============
----wsgi-file
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load .wsgi file

----file
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load .wsgi file

----eval
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



eval python code

----module
******
``argument``: required_argument

``shortcut``: -w

``parser``: uwsgi_opt_set_str



load a WSGI module

----wsgi
****
``argument``: required_argument

``shortcut``: -w

``parser``: uwsgi_opt_set_str



load a WSGI module

----callable
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set default WSGI callable name

----test
****
``argument``: required_argument

``shortcut``: -J

``parser``: uwsgi_opt_set_str



test a mdule import

----home
****
``argument``: required_argument

``shortcut``: -H

``parser``: uwsgi_opt_set_str



set PYTHONHOME/virtualenv

----virtualenv
**********
``argument``: required_argument

``shortcut``: -H

``parser``: uwsgi_opt_set_str



set PYTHONHOME/virtualenv

----venv
****
``argument``: required_argument

``shortcut``: -H

``parser``: uwsgi_opt_set_str



set PYTHONHOME/virtualenv

----pyhome
******
``argument``: required_argument

``shortcut``: -H

``parser``: uwsgi_opt_set_str



set PYTHONHOME/virtualenv

----py-programname
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set python program name

----py-program-name
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set python program name

----pythonpath
**********
``argument``: required_argument

``parser``: uwsgi_opt_pythonpath



add directory (or glob) to pythonpath

----python-path
***********
``argument``: required_argument

``parser``: uwsgi_opt_pythonpath



add directory (or glob) to pythonpath

----pp
**
``argument``: required_argument

``parser``: uwsgi_opt_pythonpath



add directory (or glob) to pythonpath

----pymodule-alias
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a python alias module

----post-pymodule-alias
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a python module alias after uwsgi module initialization

----import
******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module

----pyimport
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module

----py-import
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module

----python-import
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module

----shared-import
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module in all of the processes

----shared-pyimport
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module in all of the processes

----shared-py-import
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module in all of the processes

----shared-python-import
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import a python module in all of the processes

----pyargv
******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



manually set sys.argv

----optimize
********
``argument``: required_argument

``shortcut``: -O

``parser``: uwsgi_opt_set_int



set python optimization level

----pecan
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a pecan config file

----paste
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a paste.deploy config file

----paste-logger
************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable paste fileConfig logger

----web3
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a web3 app

----pump
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a pump app

----wsgi-lite
*********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a wsgi-lite app

----ini-paste
*********
``argument``: required_argument

``parser``: uwsgi_opt_ini_paste

``flags``: UWSGI_OPT_IMMEDIATE



load a paste.deploy config file containing uwsgi section

----ini-paste-logged
****************
``argument``: required_argument

``parser``: uwsgi_opt_ini_paste

``flags``: UWSGI_OPT_IMMEDIATE



load a paste.deploy config file containing uwsgi section (load loggers too)

----reload-os-env
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



force reload of os.environ at each request

----no-site
*******
``argument``: no_argument

``parser``: uwsgi_opt_true



do not import site module

----pyshell
*******
``argument``: optional_argument

``parser``: uwsgi_opt_pyshell



run an interactive python shell in the uWSGI environment

----pyshell-oneshot
***************
``argument``: optional_argument

``parser``: uwsgi_opt_pyshell



run an interactive python shell in the uWSGI environment (one-shot variant)

----python
******
``argument``: required_argument

``parser``: uwsgi_opt_pyrun



run a python script in the uWSGI environment

----py
**
``argument``: required_argument

``parser``: uwsgi_opt_pyrun



run a python script in the uWSGI environment

----pyrun
*****
``argument``: required_argument

``parser``: uwsgi_opt_pyrun



run a python script in the uWSGI environment

----py-tracebacker
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER



enable the uWSGI python tracebacker

----py-auto-reload
**************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER



monitor python modules mtime to trigger reload (use only in development)

----py-autoreload
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER



monitor python modules mtime to trigger reload (use only in development)

----python-auto-reload
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER



monitor python modules mtime to trigger reload (use only in development)

----python-autoreload
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int

``flags``: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER



monitor python modules mtime to trigger reload (use only in development)

----py-auto-reload-ignore
*********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_THREADS|UWSGI_OPT_MASTER



ignore the specified module during auto-reload scan (can be specified multiple times)

----wsgi-env-behaviour
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the strategy for allocating/deallocating the WSGI env

----wsgi-env-behavior
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the strategy for allocating/deallocating the WSGI env

----start_response-nodelay
**********************
``argument``: no_argument

``parser``: uwsgi_opt_true



send WSGI http headers as soon as possible (PEP violation)

----wsgi-strict
***********
``argument``: no_argument

``parser``: uwsgi_opt_true



try to be fully PEP compliant disabling optimizations

----wsgi-accept-buffer
******************
``argument``: no_argument

``parser``: uwsgi_opt_true



accept CPython buffer-compliant objects as WSGI response in addition to string/bytes

----wsgi-accept-buffers
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



accept CPython buffer-compliant objects as WSGI response in addition to string/bytes

----python-version
**************
``argument``: no_argument

``parser``: uwsgi_opt_pyver

``flags``: UWSGI_OPT_IMMEDIATE



report python version

----python-raw
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load a python file for managing raw requests

----py-sharedarea
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



create a sharedarea from a python bytearray object of the specified size

----py-call-osafterfork
*******************
``argument``: no_argument

``parser``: uwsgi_opt_true



enable child processes running cpython to trap OS signals


plugin: pyuwsgi
===============

plugin: rack
============
----rails
*****
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_POST_BUFFERING



load a rails <= 2.x app

----rack
****
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_POST_BUFFERING



load a rack app

----ruby-gc-freq
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set ruby GC frequency

----rb-gc-freq
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set ruby GC frequency

----rb-lib
******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a directory to the ruby libdir search path

----ruby-lib
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a directory to the ruby libdir search path

----rb-require
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script

----ruby-require
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script

----rbrequire
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script

----rubyrequire
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script

----require
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script

----shared-rb-require
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script (shared)

----shared-ruby-require
*******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script (shared)

----shared-rbrequire
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script (shared)

----shared-rubyrequire
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script (shared)

----shared-require
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



import/require a ruby module/script (shared)

----gemset
******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load the specified gemset (rvm)

----rvm
***
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load the specified gemset (rvm)

----rvm-path
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



search for rvm in the specified directory

----rbshell
*******
``argument``: optional_argument

``parser``: uwsgi_opt_rbshell



run  a ruby/irb shell

----rbshell-oneshot
***************
``argument``: no_argument

``parser``: uwsgi_opt_rbshell



set ruby/irb shell (one shot)


plugin: rados
=============
----rados-mount
***********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



virtual mount the specified rados volume in a uri

----rados-timeout
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



timeout for async operations


plugin: rawrouter
=================
----rawrouter
*********
``argument``: required_argument

``parser``: uwsgi_opt_undeferred_corerouter



run the rawrouter on the specified port

----rawrouter-processes
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of rawrouter processes

----rawrouter-workers
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of rawrouter processes

----rawrouter-zerg
**************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_zerg



attach the rawrouter to a zerg server

----rawrouter-use-cache
*******************
``argument``: optional_argument

``parser``: uwsgi_opt_set_str



use uWSGI cache as hostname->server mapper for the rawrouter

----rawrouter-use-pattern
*********************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_pattern



use a pattern for rawrouter hostname->server mapping

----rawrouter-use-base
******************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_base



use a base dir for rawrouter hostname->server mapping

----rawrouter-fallback
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



fallback to the specified node in case of error

----rawrouter-use-code-string
*************************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_cs



use code string as hostname->server mapper for the rawrouter

----rawrouter-use-socket
********************
``argument``: optional_argument

``parser``: uwsgi_opt_corerouter_use_socket



forward request to the specified uwsgi socket

----rawrouter-to
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



forward requests to the specified uwsgi server (you can specify it multiple times for load balancing)

----rawrouter-gracetime
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



retry connections to dead static nodes after the specified amount of seconds

----rawrouter-events
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of concurrent events

----rawrouter-max-retries
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of retries/fallbacks to other nodes

----rawrouter-quiet
***************
``argument``: required_argument

``parser``: uwsgi_opt_true



do not report failed connections to instances

----rawrouter-cheap
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



run the rawrouter in cheap mode

----rawrouter-subscription-server
*****************************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_ss



run the rawrouter subscription server on the spcified address

----rawrouter-subscription-slot
***************************
``argument``: required_argument

``parser``: uwsgi_opt_deprecated



*** deprecated ***

----rawrouter-timeout
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set rawrouter timeout

----rawrouter-stats
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the rawrouter stats server

----rawrouter-stats-server
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the rawrouter stats server

----rawrouter-ss
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the rawrouter stats server

----rawrouter-harakiri
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable rawrouter harakiri

----rawrouter-xclient
*****************
``argument``: no_argument

``parser``: uwsgi_opt_true



use the xclient protocol to pass the client addres

----rawrouter-buffer-size
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set internal buffer size (default: page size)


plugin: rbthreads
=================
----rbthreads
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



enable ruby native threads

----rb-threads
**********
``argument``: no_argument

``parser``: uwsgi_opt_true



enable ruby native threads

----rbthread
********
``argument``: no_argument

``parser``: uwsgi_opt_true



enable ruby native threads

----rb-thread
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



enable ruby native threads


plugin: redislog
================

plugin: ring
============
----ring-load
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load the specified clojure script

----clojure-load
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load the specified clojure script

----ring-app
********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



map the specified ring application (syntax namespace:function)


plugin: router_access
=====================

plugin: router_basicauth
========================

plugin: router_cache
====================

plugin: router_expires
======================

plugin: router_hash
===================

plugin: router_http
===================

plugin: router_memcached
========================

plugin: router_metrics
======================

plugin: router_radius
=====================

plugin: router_redirect
=======================

plugin: router_redis
====================

plugin: router_rewrite
======================

plugin: router_spnego
=====================

plugin: router_static
=====================

plugin: router_uwsgi
====================

plugin: router_xmldir
=====================

plugin: rpc
===========

plugin: rrdtool
===============
----rrdtool
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MASTER|UWSGI_OPT_METRICS



store rrd files in the specified directory

----rrdtool-freq
************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set collect frequency

----rrdtool-lib
***********
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the name of rrd library (default: librrd.so)


plugin: rsyslog
===============
----rsyslog-packet-size
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set maximum packet size for syslog messages (default 1024) WARNING! using packets > 1024 breaks RFC 3164 (#4.1)

----rsyslog-split-messages
**********************
``argument``: no_argument

``parser``: uwsgi_opt_true



split big messages into multiple chunks if they are bigger than allowed packet size (default is false)


plugin: ruby19
==============

plugin: servlet
===============

plugin: signal
==============

plugin: spooler
===============

plugin: sqlite3
===============
----sqlite3
*******
``argument``: required_argument

``parser``: uwsgi_opt_load_sqlite3

``flags``: UWSGI_OPT_IMMEDIATE



load config from sqlite3 db

----sqlite
******
``argument``: required_argument

``parser``: uwsgi_opt_load_sqlite3

``flags``: UWSGI_OPT_IMMEDIATE



load config from sqlite3 db


plugin: ssi
===========

plugin: sslrouter
=================
----sslrouter
*********
``argument``: required_argument

``parser``: uwsgi_opt_sslrouter



run the sslrouter on the specified port

----sslrouter2
**********
``argument``: required_argument

``parser``: uwsgi_opt_sslrouter2



run the sslrouter on the specified port (key-value based)

----sslrouter-session-context
*************************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the session id context to the specified value

----sslrouter-processes
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of sslrouter processes

----sslrouter-workers
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



prefork the specified number of sslrouter processes

----sslrouter-zerg
**************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_zerg



attach the sslrouter to a zerg server

----sslrouter-use-cache
*******************
``argument``: optional_argument

``parser``: uwsgi_opt_set_str



use uWSGI cache as hostname->server mapper for the sslrouter

----sslrouter-use-pattern
*********************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_pattern



use a pattern for sslrouter hostname->server mapping

----sslrouter-use-base
******************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_use_base



use a base dir for sslrouter hostname->server mapping

----sslrouter-fallback
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



fallback to the specified node in case of error

----sslrouter-use-code-string
*************************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_cs



use code string as hostname->server mapper for the sslrouter

----sslrouter-use-socket
********************
``argument``: optional_argument

``parser``: uwsgi_opt_corerouter_use_socket



forward request to the specified uwsgi socket

----sslrouter-to
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



forward requests to the specified uwsgi server (you can specify it multiple times for load balancing)

----sslrouter-gracetime
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



retry connections to dead static nodes after the specified amount of seconds

----sslrouter-events
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of concurrent events

----sslrouter-max-retries
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set the maximum number of retries/fallbacks to other nodes

----sslrouter-quiet
***************
``argument``: required_argument

``parser``: uwsgi_opt_true



do not report failed connections to instances

----sslrouter-cheap
***************
``argument``: no_argument

``parser``: uwsgi_opt_true



run the sslrouter in cheap mode

----sslrouter-subscription-server
*****************************
``argument``: required_argument

``parser``: uwsgi_opt_corerouter_ss



run the sslrouter subscription server on the spcified address

----sslrouter-timeout
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set sslrouter timeout

----sslrouter-stats
***************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the sslrouter stats server

----sslrouter-stats-server
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the sslrouter stats server

----sslrouter-ss
************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the sslrouter stats server

----sslrouter-harakiri
******************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



enable sslrouter harakiri

----sslrouter-sni
*************
``argument``: no_argument

``parser``: uwsgi_opt_true



use SNI to route requests

----sslrouter-buffer-size
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set internal buffer size (default: page size)


plugin: stackless
=================
----stackless
*********
``argument``: no_argument

``parser``: uwsgi_opt_true



use stackless as suspend engine


plugin: stats_pusher_file
=========================

plugin: stats_pusher_mongodb
============================

plugin: stats_pusher_socket
===========================

plugin: stats_pusher_statsd
===========================

plugin: symcall
===============
----symcall
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load the specified C symbol as the symcall request handler (supports <mountpoint=func> too)

----symcall-use-next
****************
``argument``: no_argument

``parser``: uwsgi_opt_true



use RTLD_NEXT when searching for symbols

----symcall-register-rpc
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load the specified C symbol as an RPC function (syntax: name function)

----symcall-post-fork
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



call the specified C symbol after each fork()


plugin: syslog
==============

plugin: systemd_logger
======================

plugin: tornado
===============
----tornado
*******
``argument``: required_argument

``parser``: uwsgi_opt_setup_tornado

``flags``: UWSGI_OPT_THREADS



a shortcut enabling tornado loop engine with the specified number of async cores and optimal parameters


plugin: transformation_chunked
==============================

plugin: transformation_gzip
===========================

plugin: transformation_offload
==============================

plugin: transformation_template
===============================

plugin: transformation_tofile
=============================

plugin: transformation_toupper
==============================

plugin: tuntap
==============
----tuntap-router
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



run the tuntap router (syntax: <device> <socket> [stats] [gateway])

----tuntap-device
*************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a tuntap device to the instance (syntax: <device>[ <socket>])

----tuntap-use-credentials
**********************
``argument``: optional_argument

``parser``: uwsgi_opt_set_str



enable check of SCM_CREDENTIALS for tuntap client/server

----tuntap-router-firewall-in
*************************
``argument``: required_argument

``parser``: uwsgi_tuntap_opt_firewall



add a firewall rule to the tuntap router (syntax: <action> <src/mask> <dst/mask>)

----tuntap-router-firewall-out
**************************
``argument``: required_argument

``parser``: uwsgi_tuntap_opt_firewall



add a firewall rule to the tuntap router (syntax: <action> <src/mask> <dst/mask>)

----tuntap-router-route
*******************
``argument``: required_argument

``parser``: uwsgi_tuntap_opt_route



add a routing rule to the tuntap router (syntax: <src/mask> <dst/mask> <gateway>)

----tuntap-router-stats
*******************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



run the tuntap router stats server

----tuntap-device-rule
******************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a tuntap device rule (syntax: <direction> <src/mask> <dst/mask> <action> [target])


plugin: ugreen
==============
----ugreen
******
``argument``: no_argument

``parser``: uwsgi_opt_true



enable ugreen coroutine subsystem

----ugreen-stacksize
****************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



set ugreen stack size in pages


plugin: v8
==========
----v8-load
*******
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



load a javascript file

----v8-preemptive
*************
``argument``: required_argument

``parser``: uwsgi_opt_set_int



put v8 in preemptive move (single isolate) with the specified frequency

----v8-gc-freq
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_64bit



set the v8 garbage collection frequency

----v8-module-path
**************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



set the v8 modules search path

----v8-jsgi
*******
``argument``: required_argument

``parser``: uwsgi_opt_set_str



load the specified JSGI 3.0 application


plugin: webdav
==============
----webdav-mount
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



map a filesystem directory as a webdav store

----webdav-css
**********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a css url for automatic webdav directory listing

----webdav-javascript
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a javascript url for automatic webdav directory listing

----webdav-js
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a javascript url for automatic webdav directory listing

----webdav-class-directory
**********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MIME



set the css directory class for automatic webdav directory listing

----webdav-div
**********
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MIME



set the div id for automatic webdav directory listing

----webdav-lock-cache
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MIME



set the cache to use for webdav locking

----webdav-principal-base
*********************
``argument``: required_argument

``parser``: uwsgi_opt_set_str

``flags``: UWSGI_OPT_MIME



enable WebDAV Current Principal Extension using the specified base

----webdav-add-option
*****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV standard to the OPTIONS response

----webdav-add-prop
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all resources

----webdav-add-collection-prop
**************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all collections

----webdav-add-object-prop
**********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all objects

----webdav-add-prop-href
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all resources (href value)

----webdav-add-collection-prop-href
*******************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all collections (href value)

----webdav-add-object-prop-href
***************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all objects (href value)

----webdav-add-prop-comp
********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all resources (xml value)

----webdav-add-collection-prop-comp
*******************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all collections (xml value)

----webdav-add-object-prop-comp
***************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV property to all objects (xml value)

----webdav-add-rtype-prop
*********************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV resourcetype property to all resources

----webdav-add-rtype-collection-prop
********************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV resourcetype property to all collections

----webdav-add-rtype-object-prop
****************************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



add a WebDAV resourcetype property to all objects

----webdav-skip-prop
****************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list

``flags``: UWSGI_OPT_MIME



do not add the specified prop if available in resource xattr


plugin: xattr
=============

plugin: xslt
============
----xslt-docroot
************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



add a document_root for xslt processing

----xslt-ext
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



search for xslt stylesheets with the specified extension

----xslt-var
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



get the xslt stylesheet path from the specified request var

----xslt-stylesheet
***************
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



if no xslt stylesheet file can be found, use the specified one

----xslt-content-type
*****************
``argument``: required_argument

``parser``: uwsgi_opt_set_str



set the content-type for the xslt rsult (default: text/html)


plugin: zabbix
==============
----zabbix-template
***************
``argument``: optional_argument

``parser``: uwsgi_opt_zabbix_template

``flags``: UWSGI_OPT_METRICS



print (or store to a file) the zabbix template for the current metrics setup


plugin: zergpool
================
----zergpool
********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



start a zergpool on specified address for specified address

----zerg-pool
*********
``argument``: required_argument

``parser``: uwsgi_opt_add_string_list



start a zergpool on specified address for specified address

