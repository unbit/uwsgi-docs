Hooks
=====

(updated to uWSGI 1.9.16)


uWSGI main directive is being "modular". The vast majority of its features are exposed as plugins, both to allow users to optimize
their build and to encourage developers to extend it.

Writing plugins can be an annoying task, expecially if you only need to change/implement a single function.

For simple tasks, uWSGI exposes an hook api you can abuse to modify uWSGI internal behaviours.

The uWSGI "hookable" phases
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Before being ready to manage requests, uWSGI go through various "phases". You can attach one or more "hooks" to that phases.

Each phase can be "fatal", if so, a failing hook will mean failing of the whole uWSGI instance (generally calling exit(1) )

Currently (September 2013) the following phases are available:

``pre-jail`` run before any attempt to drop privileges or put the process in some form of jail. it is fatal.

``post-jail`` run soon after any jailing, but before privileges drop. If jailing requires fork(), the parent process run this phase. it is fatal.

``in-jail`` run soon after jayling, but after post-jail. If jailing requires fork(), the chidlren run this phase. it is fatal.

``as-root`` run soon before privileges drop (last chance to run something as root). it is fatal.

``as-user`` run soon after privileges drop. it is fatal.

``as-user-atexit`` run before shutdown of the instance. it is non-fatal.

``as-emperor`` run soon after the spawn of a vassal in the Emperor process. it is non-fatal.

``as-vassal`` run in the vassal before executing the uwsgi binary. it is fatal.

The "hardcoded" hooks
^^^^^^^^^^^^^^^^^^^^^

As sais before the purpose of the hook subsystem is allowing to attach "hooks" to the various uWSGI phases.

There are two kind of hooks, the simple ones are the so-called "hardcoded". They exposes common patterns at the cost of versatility.

Currently (Semptember 2013) the following "hardcoded" hooks are available:

``exec`` run shell commands

``call`` call functions in the current process address space

``mount`` mount filesystems

``umount`` un-mount filesystems
