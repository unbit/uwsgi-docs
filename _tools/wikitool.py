import pprint
import os
import sys
from trac_miniparser import parse

class IndentingOutput(object):
	def __init__(self, stream):
		self.stream = stream
		self.indent = 0

	def _change_indent(self, delta, pre=None, post=None):
		if pre:
			self.write(pre)
		self.indent += delta
		assert self.indent >= 0
		if post:
			self.write(post)

	def begin(self, pre=None, post=None): self._change_indent(1, pre, post)
	def end(self, pre=None, post=None): self._change_indent(-1, pre, post)

	def write(self, str=""):
		indent = ("    " * self.indent)
		for line in str.splitlines():
			self.stream.write(indent + line + "\n")

def rewrite_wiki_inline(str):
	return str


def write_rst(tokens, output):
	iout = IndentingOutput(output)
	for token in tokens:
		if isinstance(token, basestring):
			iout.write(rewrite_wiki_inline(token))
			continue
		else:
			type, data = token
			if type == "begin_code":
				iout.begin(".. code-block:: %s\n\n" % data.get("lang", "xxx"))
				continue
			elif type == "end_code":
				iout.end()
			elif type == "heading":
				level = len(data["n"])
				text = data["text"]
				foot = '=-^^'[level] * len(text)
				iout.write(text)
				iout.write(foot)
				iout.write()
			else:
				raise NotImplementedError("No idea what to do with token %r" % token)


def transmogrify(filename):
	basename = os.path.basename(filename).split(".")[0]
	text = file(filename, "rb").read().decode("UTF-8")
	tokens = parse(text, coalesce=True)
	write_rst(tokens, sys.stdout)

	#print basename

if __name__ == '__main__':
	transmogrify(sys.argv[1])
