uWSGI 2.0.8
===========

Bugfixes
--------

* fixed php SCRIPT_NAME usage when --php-app is in place
* allow "appendn" hook without second argument
* fix heap corruption in carbon plugin
* fix getifaddrs() memory management
* fixed tcsetattr() usage
* fixed kevent usage of return value
* ensure PSGI response headers are in the right format
* fixed attached daemons reload
