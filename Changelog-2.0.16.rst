uWSGI 2.0.16
============

[20180210]

Maintenance release

Security
------

- [CVE-2018-6758] Stack-based buffer overflow in core/utils.c:uwsgi_expand_path()

Changes
-------

- Backported early_post_jail plugin hook (Bjørnar Ness)
- Fixed ipv6 suupport for http-socket (James Brown)
- Enable execinfo on DragonFly BSD (Aaron LI)
- Fix inet_ntop buffer size (Orivej Desh)
- Add worker running time metrics (Serge/yasek)
- Backported safe-pidfile, safe-pidfile2 (Nate Coraor)
- Stop using libxml2 by default on osx
- Fixed uwsgi_kvlist_parse signature
- Backport http range fixes from master (Curtis Maloney, Sokolov Yura)
- relicensed mod_proxy_uwsgi to Apache 2.0
- logging: Add ${millis} support to json encode
- plugins/router_xmldir: fixup invalid locale check (Riccardo Magliocchetti)
- Add ssl-verify-depth flag to set the max Client CA chain length (Paul Tagliamonte)
- Allow to override build date (Bernhard M. Wiedemann)
- Python 3 plugin: set thread name as unicode (Jyrki Muukkonen)

Availability
------------

You can download uWSGI 2.0.16 from https://projects.unbit.it/downloads/uwsgi-2.0.16.tar.gz
