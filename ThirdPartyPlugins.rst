uWSGI third party plugins
=========================

The following plugins (unless otherwise specified) are not commercially supported.

Feel free to add your plugin to the list by sending a pull request to the ``uwsgi-docs`` project.

uwsgi-capture
*************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-capture

Allows gathering video4linux frames in a sharedarea.


uwsgi-wstcp
***********

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-wstcp

Maps websockets to TCP connections (useful for proxying via javascript).

uwsgi-pgnotify
**************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-pgnotify

Integrates the PostgreSQL notification system with the uWSGI signal framework.

uwsgi-quota
***********

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-quota

Allows to set and monitor filesystem quotas.

uwsgi-eventfd
*************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-eventfd

Allows to monitor eventfd() objects (like events sent by the cgroup system).

uwsgi-console-broadcast
***********************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-console-broadcast

Exposes hooks for sending broadcast messages to user terminals.

uwsgi-strophe
*************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-strophe

Integration with the libstrophe library (xmpp).

uwsgi-alarm-chain
*****************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-alarm-chain

Virtual alarm handler combining multiple alarms into a single one.

uwsgi-netlink
*************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-netlink

Integration with the Linux netlink subsystem.

uwsgi-pushover
**************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-pushover

Integration with Pushover.net services.

uwsgi-consul
************

* License: MIT
* Author: unbit, ultrabug
* Website: https://github.com/unbit/uwsgi-consul


Integration with consul agents (consul.io)

uwsgi-influxdb
**************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-influxdb

Allows sending metrics to influxdb

uwsgi-opentsdb
**************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-opentsdb

Allows sending metrics to opentsdb

uwsgi-cares
***********

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-cares

exposes non-blocking dns query via the cares library

uwsgi-ganglia
**************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-ganglia

Allows sending metrics to ganglia

uwsgi-bonjour
*************

* License: MIT
* Author: unbit, 20tab
* Website: https://github.com/unbit/uwsgi-bonjour

Automatically register domain names in OSX bonjour subsystem

uwsgi-avahi
***********

* License: MIT
* Author: 20tab
* Website: https://github.com/20tab/uwsgi-avahi

Automatically register domain names in avahi subsystem

uwsgi-datadog
*************

* License: MIT
* Author: unbit
* Website: https://github.com/unbit/uwsgi-datadog

Automatically send metrics to datadog (https://www.datadoghq.com/)
