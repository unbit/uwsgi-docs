# Parse "struct uwsgi_option ..._options[] = { }" lists into Python files for inclusion into optdefs.
# Good luck!

from pycparser import CParser
from pycparser.c_ast import NodeVisitor, Constant
import re
import sys

DIRECTIVE_RE = re.compile("^#(.+)$", re.MULTILINE)

class DictWrapper(object):
	def __init__(self, dict):
		self.dict = dict
	def __getattr__(self, key):
		return self.dict[key]

class OptionParser(NodeVisitor):
	def __init__(self):
		self.commands = []

	def visit_ExprList(self, node):
		bits = [n[1] for n in node.children()]
		if isinstance(bits[0], Constant) and bits[0].type == "string":
			self.add_option(node, bits)
		
		self.generic_visit(node)

	def parse_file(self, filename):
		parser = CParser()
		buf = file(filename).read()
		buf = DIRECTIVE_RE.sub("", buf)#r"/* directive \1 elided */", buf)
		t = parser.parse(buf, filename)
		self.visit(t)

	def add_option(self, node, bits):
		cmd = {
			"names":		[bits[0].value.replace('"', '')],
			"argument":		bits[1].name.replace("_argument", ""),
			"short_name":	None,
			"help":			bits[3].value.replace('"', ''),
			"type":			None
		}
		if bits[2].type == "char":
			cmd["short_name"] = bits[2].value.replace("'", "")

		setter = bits[4].name

		if setter == "uwsgi_opt_true" or cmd["argument"] == "no":
			cmd["type"] = "True"
		elif setter == "uwsgi_opt_set_str":
			cmd["type"] = "str"
		elif setter == "uwsgi_opt_set_int":
			cmd["type"] = "int"
		elif setter == "uwsgi_opt_set_64bit":
			cmd["type"] = "long"
		elif setter == "uwsgi_opt_add_string_list":
			cmd["type"] = "[str]"
		else:
			print >>sys.stderr, "Setter? %s, %r" % (setter, cmd)
			cmd["type"] = repr(setter.replace("uwsgi_opt_", "").replace("_", " "))

		for tcmd in self.commands:
			if cmd["help"] == tcmd.help:
				tcmd.names.append(cmd["names"][0])
				return False
		self.commands.append(DictWrapper(cmd))

	def write_py(self, stream):
		W = stream.write
		W("\n")
		W("\n")
		W("def XXX_config():\n")
		W('\tconfig = Config("XXX")\n')
		W('\t\n')
		W('\twith config.section("XXX", docs = []) as s:\n')
		for cmd in self.commands:

			tp = cmd.type
			if cmd.argument == "optional":
				tp = "optional(%s)" % tp

			if len(cmd.names) == 1:
				names = '"%s"' % cmd.names[0]
			else:
				names = "(%s)" % (", ".join('"%s"' % n for n in cmd.names))

			W('\t\ts.o(%s, %s, "%s"' % (names, tp, cmd.help))
			if cmd.short_name:
				W(', short_name="%s"' % cmd.short_name)
			W(")\n")
		W("\t\n")
		W("\treturn config\n")





def main(filename):
	op = OptionParser()
	op.parse_file(filename)
	op.write_py(sys.stdout)

if __name__ == '__main__':
	main(sys.argv[1])