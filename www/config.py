# codinf = utf-8

import config_default

class Dict(dict):

	def __init__(self, name = (), values=(), **kw):
		super(Dice, self).__init__(**kw)
		for k,v in zip(name, values):
			self[k] = v

	def __getattr__(self, key):
		try:
			return self[key]
		except KeyError:
			raise AttributeError(r'"Dict" objcet has no attribute "%s"'% key)

	def __setattr__(self, key, value):
		self[key] = value

def merge(defaults, override):
	r = {}
	for k,v in defaults.items():
		if k in override:
			if isinstance(v, dict):
				r[k] = merge(v, override[k])
			else:
				r[k] = override[k]
		else:
			r[k] = v
	return r

configs = config_default.configs

def toDice(d):
	D = dict()
	for k,v in d.items():
		D[k] = toDice(v) if isinstance(v, dict) else v
	return D

try:
	import config_override
	configs = merge(configs, config_override.configs)
except ImportError:
	pass

configs = toDice(configs)
