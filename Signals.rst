Signals
=======

The uWSGI server responds to the following signals:

==========  ========================================================================
`SIGHUP`    gracefully reload all the workers and the master process (see :doc:`Reload`)
`SIGTERM`   brutally reload all the workers and the master process (see :doc:`Reload`)
`SIGINT`    immediately kill the entire uWSGI stack
`SIGQUIT`   immediately kill the entire uWSGI stack
`SIGUSR1`   print statistics
`SIGUSR2`   print worker status or wakeup the spooler
`SIGURG`    restore a snapshot
`SIGTSTP`   pause/suspend/resume an instance
`SIGWINCH`  wakeup a worker blocked in a syscall (internal use)
==========  ========================================================================
