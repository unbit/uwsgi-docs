FreeBSD Jails
=============

uWSGI 1.9.16 introduced native FreeBSD jails support.

FreeBSD jails can be seen as new-generation chroot() with fine-grained tuning of what this "jail" can see.

They are very similar to Linux namespaces even if a bit higher-level (from the API point of view).

Jails are available since FreeBSD 4


Why managing jails with uWSGI ?
*******************************

Generally jails are managed using the system tool "jail" and its utilities.

Til now running uWSGI in FreeBSD jails was pretty common, but for really massive setups (read: hosting business)
where an Emperor (for example) manages hundreds of unrelated uWSGI instances, the setup could be really overkill.

Managing jails directly in uWSGI config files highly reduce sysadmin costs and helps having a better organization of the whole infrastructure.

Old-style jails
***************

FreeBSD exposes two main api for managing jails. The old (and easier) one is based on the jail() function.

It is available since FreeBSD 4 and allows you to set the rootfs, the hostname and one ore more ipv4/ipv6 addresses

Two options are needed for running a uWSGI instance in a jail: --jail and --jail-ip4/--jail-ip6 (effectively they are 3 if you use IPv6)

``--jail <rootfs> [hostname] [jailname]``

``--jail-ip4 <address>`` (can be specified multiple times)

``--jail-ip6 <address>`` (can be specified multiple times)

Showing how to create the rootfs for your jail is not the objective of this document, but personally i hate rebuilding from sources, so generally
i simply explode the base.tgz file from an official repository and chroot() to it to make the fine tuning.

An important thing you have to remember is that the ip addresses you attach to a jail must be available in the system (as aliases)
