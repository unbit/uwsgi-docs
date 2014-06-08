$OPTIONS = {
	'emperor' => {'ref' => 'Emperor', 'doc' => "The Emperor is a special uWSGI instance aimed at governing other uWSGI instances (named: vassals). By default it is configured to monitor a directory containing valid uWSGI config files, whenever a fiel is created a new instance is spawned, when the file is touched the instance is reloaded, when the file is removed the instance is destroyed. It can be extended to support more paradigms"},
	'thunder-lock' => {'ref' => 'articles/SerializingAccept'},
	'declare-option' => {'ref' => 'CustomOptions'},
	'fastrouter' => {'ref' => 'Fastrouter'},
};
