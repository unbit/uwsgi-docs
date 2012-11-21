import re

rules = []
rule_funcs = {}

def rule(regexp, type, func=(lambda m: m.groupdict() or {}), update_prior_token=None):
	rules.append((re.compile(regexp), type, update_prior_token))
	rule_funcs[type] = func

def parse(text, coalesce=True):
	text = text.splitlines()
	tokens = []
	for line in text:
		for regexp, type, update_prior_token in rules:
			m = regexp.match(line)
			if m:
				res = rule_funcs[type](m)
				if update_prior_token:
					for tok in reversed(tokens):
						if (not isinstance(tok, basestring)) and tok[0] == update_prior_token:
							tok[1].update(res)
							res = None
							break
							
				if res is not None:
					tokens.append((type, res))
				break
		else:
			tokens.append(line + "\n")
	
	if coalesce:
		coalesce_bare(tokens)
	
	return tokens

def coalesce_bare(tokens):
	i = 1
	while i < len(tokens) - 1:
		if isinstance(tokens[i], basestring) and isinstance(tokens[i-1], basestring):
			tokens[i-1] += tokens[i]
			tokens.pop(i)
		else:
			i += 1

rule(r"^\{{3}$", "begin_code")
rule(r"^\}{3}$", "end_code")
rule(r"^#!(?P<lang>\w+)$", "lang", update_prior_token="begin_code")
rule(r"^(?P<n>=+)\s*(?P<text>.+?)\s*=*$", "heading")
