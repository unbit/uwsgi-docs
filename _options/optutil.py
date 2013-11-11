from collections import defaultdict
import re
import textwrap

un_whitespace_re = re.compile(r"[\s_]+")
first_word_re = re.compile("^(\w+)", re.I)

class _Optional:
    def __init__(self, inner):
        self.inner = inner

def transmogrify_name(name):
    if isinstance(name, basestring):
        return [unicode(name)]
    else:
        return [unicode(name) for name in name]    

class Option:
    def __init__(self, name, type, desc, short_name, optional, multiple, docs=(), default=None, help=None, since=None):
        self.names = transmogrify_name(name)
        self.type = type
        self.desc = desc
        self.short_name = short_name
        self.optional = optional
        self.multiple = multiple
        self.docs = sorted(docs)
        self.cc_name = self.names[0].replace("-", " ").title().replace(" ", "")
        self.help = textwrap.dedent((help or "").strip("\r\n"))
        self.default = default
        self.since = since

    def get_argument(self):
        if self.type is int or self.type is long:
            argument_desc = "number"
        elif self.type is str:
            argument_desc = "string"
        elif self.type is True:
            argument_desc = "no argument"
        else:
            argument_desc = "*%s*" % self.type

        if self.optional:
            argument_desc = "optional %s" % argument_desc

        return argument_desc

    def get_description(self):
        desc = self.desc.strip()

        # Fixup!
        if desc[0] == desc[0].lower():
            desc = desc[0].upper() + desc[1:]
        if not desc.endswith("."):
            desc += "."
        
        if self.short_name:
            desc += u"\n\nThis option may be set with ``-%s`` from the command line." % self.short_name

        if self.multiple:
            desc += "\n\n*This option may be declared multiple times.*"

        if self.since:
            desc += "\n\nThis option is available since version %s." % self.since

        return desc

class Section:
    def __init__(self, name, docs = [], refname=None):
        self.name = name
        self.options = []
        self.refname = refname
        self.docs = sorted(docs)

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        pass

    def define_option(self, name, type, desc, short_name=None, docs=(), default=None, help=None, since=None):
        if isinstance(type, _Optional):
            optional = True
            type = type.inner
        else:
            optional = False
        
        if isinstance(type, list):
            multiple = True
            type = type[0]
        else:
            multiple = False

        assert (not short_name or len(short_name) == 1)
        args = locals()
        args.pop("self")

        for option in self.options:
            if option.desc == desc:
                print "Found redeclared config entry %s, augmenting old one (%s)" % (name, option.names)
                option.names.extend(transmogrify_name(name))
                return

        self.options.append(Option(**args))

    o = define_option


class Config(object):
    def __init__(self, title, filename_part=None):
        self.title = title
        if filename_part:
            self.filename_part = filename_part
        else:
            filename_part = first_word_re.search(self.title).group(1)
            if filename_part.upper() != filename_part:
                filename_part = (un_whitespace_re.sub("", filename_part).title())
        self.filename_part = filename_part
        self.sections = []

    def section(self, name, **kwargs):
        section = Section(name, **kwargs)
        self.sections.append(section)
        return section