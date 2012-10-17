from collections import defaultdict

class _Optional:
    def __init__(self, inner):
        self.inner = inner

def transmogrify_name(name):
    if isinstance(name, basestring):
        return [unicode(name)]
    else:
        return [unicode(name) for name in name]    

class Option:
    def __init__(self, name, type, desc, short_name, optional, multiple, docs = ()):
        self.names = transmogrify_name(name)
        self.type = type
        self.desc = desc
        self.short_name = short_name
        self.optional = optional
        self.multiple = multiple
        self.docs = sorted(docs)

    def get_argument(self):
        if self.type is int:
            argument_desc = "number"
        elif self.type is long:
            argument_desc = "number"
        elif self.type is str:
            argument_desc = "string"
        elif self.type is True:
            argument_desc = "\\"
        else:
            argument_desc = "*%s*" % self.type

        if self.optional:
            argument_desc = "[%s]" % argument_desc

        return argument_desc

    def get_description(self):
        desc = self.desc.strip()

        # Fixup!
        if desc[0] == desc[0].lower():
            desc = desc[0].upper() + desc[1:]
        if not desc.endswith("."):
            desc += "."
        
        if self.short_name:
            desc += u" This option may be set with ``-%s`` from the command line." % self.short_name

        if self.multiple:
            desc += " *This option may be declared multiple times.*"


        return desc

class Section:
    def __init__(self, name, docs = []):
        self.name = name
        self.options = []
        self.docs = sorted(docs)

    def __enter__(self):
        return self

    def __exit__(self, et, ev, tb):
        pass

    def define_option(self, name, type, desc, short_name=None, docs = []):
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
    def __init__(self, title):
        self.title = title
        self.sections = []

    def section(self, name, docs=()):
        section = Section(name, docs)
        self.sections.append(section)
        return section