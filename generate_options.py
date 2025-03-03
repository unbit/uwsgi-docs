#!/usr/bin/env python3
import os
import re
import sys

# Any information per option that's not defined in the source code definition of the option goes here.
# The key is the option name and the value is a dictionary with the following keys:
# - ref: The reference documentation page for the option
# - doc: Additional information about the option
OPTIONS = {
    'emperor': {
        'ref': 'Emperor', 
        'doc': "The Emperor is a special uWSGI instance aimed at governing other uWSGI instances (named: vassals). By default it is configured to monitor a directory containing valid uWSGI config files, whenever a file is created a new instance is spawned, when the file is touched the instance is reloaded, when the file is removed the instance is destroyed. It can be extended to support more paradigms"
    },
    'thunder-lock': {'ref': 'articles/SerializingAccept'},
    'declare-option': {'ref': 'CustomOptions'},
    'fastrouter': {'ref': 'Fastrouter'},
    'freebind': {
        'doc': "set the IP_FREEBIND flag to every socket created by uWSGI. This kind of socket can bind to non-existent ip addresses. Its main purpose is for high availability (this is Linux only)"
    },
    'sharedarea': {'ref': 'SharedArea'},
    'metrics-no-cores': {
        'ref': 'Metrics', 
        'doc': "Do not expose metrics of async cores."
    },
    'stats-no-cores': {
        'ref': 'Metrics', 
        'doc': "Do not expose the information about cores in the stats server."
    },
    'stats-no-metrics': {
        'ref': 'Metrics', 
        'doc': "Do not expose the metrics at all in the stats server."
    },
    'buffer-size': {
        'doc': "Set the max size of a request (request-body excluded), this generally maps to the size of request headers. By default it is 4k. If you receive a bigger request (for example with big cookies or query string) you may need to increase it. It is a security measure too, so adapt to your app needs instead of maxing it out."
    },
    'wsgi-env-behaviour': {
        'doc': 'set the strategy for allocating/deallocating the WSGI env',
        'ref': 'articles/WSGIEnvBehaviour',
    },
    'wsgi-env-behavior': {
        'ref': 'articles/WSGIEnvBehaviour',
    }
}

def print_header():
    """Print the document header"""
    print('''uWSGI Options
^^^^^^^^^^^^^

This is an automatically generated reference list of the uWSGI options.

It is the same output you can get via the ``--help`` option.

This page is probably the worst way to understand uWSGI for newbies. If you are still learning how the project
works, you should read the various quickstarts and tutorials.

Each option has the following attributes:

* argument: it is the struct option (used by getopt()/getopt_long()) has_arg element. Can be 'required', 'no_argument' or 'optional_argument'
* shortcut: some option can be specified with the short form (a dash followed by a single letter)
* parser: this is how uWSGI parses the parameter. There are dozens of way, the most common are 'uwsgi_opt_set_str' when it takes a simple string, 'uwsgi_opt_set_int' when it takes a 32bit number, 'uwsgi_opt_add_string_list' when the parameter can be specified multiple times to build a list.
* help: the help message, the same you get from ``uwsgi --help``
* reference: a link to a documentation page that gives better understanding and context of an option

You can add more detailed infos to this page, editing https://github.com/unbit/uwsgi-docs/blob/master/generate_options.py (please, double check it before sending a pull request)
''')

line_re = re.compile(
    r'''
        ^\s*  # Whitespace on start of line
        \{   # Opening brace
        \s*
        (?:\(char\s*\*\)\s*)?  # Optional cast to char*
        "(?P<name>[^"]+)"  # Option name
        \s*,\s*  # comma and Whitespace
        (?P<type>\w+)  # Argument type
        \s*,\s*  # comma and Whitespace
        (?:0|'(?P<shortname>\w)')
        \s*,\s*  # comma and Whitespace
        (?:\(char\s*\*\)\s*)?  # Optional cast to char*
        "(?P<help>.+)"  # Help text
        \s*,\s*  # comma and Whitespace
        (?P<func>[^,]+)  # Function name
        \s*,\s*  # comma and Whitespace
        (?P<arg1>[^,]+)  # Arg1
        \s*,\s*  # comma and Whitespace
        (?P<flags>[^,]+)  # Arg2
        \s*}\s*,?
        $  # End of line

    ''',
    re.VERBOSE | re.IGNORECASE | re.MULTILINE
)

def parse_options(file):
    """Parse options from a C file"""
    with open(file, 'r', encoding='utf-8') as file:
        contents = file.read()
    options = line_re.findall(contents)
    return list(options)

def generate_doc(options):
    """Parse a C file and generate documentation for options"""
    for name, type_, shortcut, help_text, func, _data, flags in options:

        # Print option documentation
        print(f"{name}")
        print('*' * len(name))
        print(f"``argument``: {type_}\n")
            
        if shortcut:
            print(f"``shortcut``: -{shortcut}\n")
            
        if func:
            print(f"``parser``: {func}\n")
            
        if flags and flags.strip() != '0':
            print(f"``flags``: {flags}\n")
            
        print(f"``help``: {help_text}\n")
            
        if name in OPTIONS and 'ref' in OPTIONS[name]:
            print(f"``reference``: :doc:`{OPTIONS[name]['ref']}`")

        print ("\n")
            
        if name in OPTIONS and 'doc' in OPTIONS[name]:
            print(f"{OPTIONS[name]['doc']}\n")

def scan_dir(path):
    """Recursively scan directories for C files"""
    if os.path.isfile(path):
        if path.endswith(('.c', '.cc', '.m')):
            yield path
    elif os.path.isdir(path):
        for entry in os.listdir(path):
            if entry.startswith('.'):
                continue
            yield from scan_dir(os.path.join(path, entry))

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_options.py <uwsgi_source_dir>", file=sys.stderr)
        sys.exit(1)
    
    root_dir = sys.argv[1]
    os.chdir(root_dir)
    
    print_header()
    
    # Process core options
    title = "uWSGI core"
    print(f"\n{title}")
    print('=' * len(title))
    core_options = parse_options('core/uwsgi.c')
    generate_doc(core_options)
    
    # Process plugins
    plugins_dir = 'plugins'
    if os.path.isdir(plugins_dir):
        for plugin in os.listdir(plugins_dir):
            if plugin.startswith('.') or not os.path.isdir(os.path.join(plugins_dir, plugin)):
                continue
            
            options = []
            for filename in scan_dir(os.path.join(plugins_dir, plugin)):
                options.extend(parse_options(filename))

            title = f"plugin: {plugin}"
            print(f"\n{title}")
            print('=' * len(title))
            generate_doc(options)

if __name__ == "__main__":
    main()
