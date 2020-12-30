# Parse "struct uwsgi_option ..._options[] = { }" lists into Python files for inclusion into optdefs.
# Good luck!

from pycparser import CParser, parse_file, preprocess_file
from pycparser.c_ast import NodeVisitor, Constant
import os
import re
import sys
import json
import traceback
import time
import ast

def comment_remover(text):
	def replacer(match):
		s = match.group(0)
		if s.startswith('/'):
			return ""
		else:
			return s
	pattern = re.compile(
		r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
		re.DOTALL | re.MULTILINE
	)
	return re.sub(pattern, replacer, text)

DIRECTIVE_RE = re.compile("^#(.+)$", re.MULTILINE)

class DictWrapper(object):
	def __init__(self, dict):
		self.dict = dict
	def __getattr__(self, key):
		return self.dict[key]

def A(type):
	return lambda scanner, token: (type, token)

scanner = re.Scanner([
	(r"[&|a-z_A-Z.][0-9a-z_A-Z.]+",  A("ID")),
	(r"(?P<p>[\"'])(.+?)(?P=p)", A("STR")),
	(r",\s*",    	    None), # skip commas
	(r"[0-9]+",   	    A("NUM")),
    (r"\{",             A("OPEN")),
    (r"\}",             A("CLOSE")),
	(r"[;\[\]=]+",       None), # Line noise
	(r"\s+", None),
	(r"#(ifdef|endif).*[\n\r]+", None),
])

def parse_opt_block(s):
	results, remainder = scanner.scan(s)
	root = []
	stack = [root]
	for type, token in results:
		if type == "OPEN":
			n = []
			stack[-1].append(n)
			stack.append(n)
		elif type == "CLOSE":
			stack.pop()
		else:
			if type == "STR":
				stack[-1].append(eval(token))
			elif type == "NUM":
				stack[-1].append(int(token))
			elif type == "ID":
				stack[-1].append(unicode(token))
			else:
				stack[-1].append((type, token))
	return root

class OptionParser(NodeVisitor):
	def __init__(self):
		self.commands = []

	def visit_ExprList(self, node):
		bits = [n[1] for n in node.children()]
		if isinstance(bits[0], Constant) and bits[0].type == "string":
			self.add_option_from_c(node, bits)

		self.generic_visit(node)

	def parse_file(self, filename):
		# buf = file(filename).read()
		# buf = DIRECTIVE_RE.sub("", buf)#r"/* directive \1 elided */", buf)
		# buf = comment_remover(buf)
		# t = parser.parse(buf, filename)
		# self.visit(t)
		self.cheap_parse_file(filename)

	def cheap_parse_file(self, filename):
		in_op = 0
		buf = ""
		for line in file(filename, "rU"):
			line = line.rstrip()
			if line.strip().startswith("//"):
				continue
			if re.search("struct uwsgi_option.+=.*\{$", line):
				in_op = 1
				continue
			if in_op and line == "};":

				for x in parse_opt_block(buf):
					if x[0] == 0 or x[0] == "NULL":
						continue
					argument_name = x[1]
					help_text = x[3]
					short_name = x[2]
					name_str = x[0]
					setter = x[4]
					self.put_option(argument_name, help_text, name_str, setter, short_name)

				buf = ""
				in_op = 0
				continue
			if in_op:
				buf += line + "\n"

	def put_option(self, argument_name, help_text, name_str, setter, short_name):
		cmd = {
			"names": [name_str.replace('"', '')],
			"argument": argument_name.replace("_argument", ""),
			"short_name": short_name or None,
			"help": help_text.replace('"', ''),
			"type": None
		}
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
			print >> sys.stderr, "Setter? %s, %r" % (setter, cmd)
			cmd["type"] = repr(setter.replace("uwsgi_opt_", "").replace("_", " "))
		for tcmd in self.commands:
			if cmd["help"] == tcmd.help:
				tcmd.names.append(cmd["names"][0])
				return False
		self.commands.append(DictWrapper(cmd))
		return True

	def add_option_from_c(self, node, bits):
		name_str = bits[0].value
		argument_name = bits[1].name
		help_text = bits[3].value
		shortname_type = bits[2].type
		shortname_value = bits[2].value
		if shortname_type == "char":
			short_name = shortname_value.replace("'", "")
		else:
			short_name = None

		setter = bits[4].name

		return self.put_option(argument_name, help_text, name_str, setter, short_name)

	def write_py(self, name, stream, ignored_names):
		pp_commands = []
		for cmd in self.commands:
			if any(n in ignored_names for n in cmd.names):
				print >>sys.stderr, "Ignoring: %r" % cmd.names
				continue
			else:
				pp_commands.append(cmd)

		if not pp_commands:
			return
		W = stream.write
		W("\n")
		W("\n")
		W("def %s_config():\n" % name)
		W('\tconfig = Config("%s")\n' % name)
		W('\t\n')
		W('\twith config.section("%s", docs = []) as s:\n' % name)



		for cmd in pp_commands:
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


try:
	with file("defined-options.json") as inf:
		ignore_options = set(json.load(inf))
except Exception, exc:
	print "Not loading ignore_options: %s" % exc
	ignored_names = set()

def main(filename):
	op = OptionParser()
	op.parse_file(filename)
	op.write_py(os.path.splitext(os.path.basename(filename))[0], sys.stdout, ignore_options)

def read_touched():
	for filename in file("sources.txt").readlines():
		filename = filename.strip()
		if not os.path.isfile(filename):
			continue
		if filename.endswith(".cc"):  # we don't parse c++ yet.
			continue
		try:
			main(filename)
		except:
			#traceback.print_exc()
			raise


if __name__ == '__main__':
	read_touched()
	#main(sys.argv[1:])