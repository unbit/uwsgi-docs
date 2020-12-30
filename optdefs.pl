$OPTIONS = {
	'emperor' => {'ref' => 'Emperor', 'doc' => "The Emperor is a special uWSGI instance aimed at governing other uWSGI instances (named: vassals). By default it is configured to monitor a directory containing valid uWSGI config files, whenever a file is created a new instance is spawned, when the file is touched the instance is reloaded, when the file is removed the instance is destroyed. It can be extended to support more paradigms"},
	'thunder-lock' => {'ref' => 'articles/SerializingAccept'},
	'declare-option' => {'ref' => 'CustomOptions'},
	'fastrouter' => {'ref' => 'Fastrouter'},
	'freebind' => {'doc' => "set the IP_FREEBIND flag to every socket created by uWSGI. This kind of socket can bind to non-existent ip addresses. Its main purpose is for high availability (this is Linux only)"},
	'sharedarea' => {'ref' => 'SharedArea' },
	'metrics-no-cores' => {'ref' => 'Metrics', 'doc' => "Do not expose metrics of async cores."},
	'stats-no-cores' => {'ref' => 'Metrics', 'doc' => "Do not expose the information about cores in the stats server."},
	'stats-no-metrics' => {'ref' => 'Metrics', 'doc' => "Do not expose the metrics at all in the stats server."},
	'buffer-size' => {'doc' => "Set the max size of a request (request-body excluded), this generally maps to the size of request headers. By default it is 4k. If you receive a bigger request (for example with big cookies or query string) you may need to increase it. It is a security measure too, so adapt to your app needs instead of maxing it out."},
};
