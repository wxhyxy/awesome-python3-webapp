# coding = utf-8

import asyncio, os, inspect, logging, functools

from urllib import parse

from aiohttp import web

def get(path):

	def decorator(func):
		@functools.wrapper
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wapper.__method__ = 'GET'
		wapper.__route__ = 'path'
		return wrapper
	return decorator

def post(path):
	def decorator(func):
		@functools.wrapper
		def wrapper(*args, **kw):
			return func(*args, **kw)
		wapper.__method__ = 'POST'
		wapper.__route__ = path
		return wapper
	return decorator

def get_required_kw_args(fn):
	args = []
	params = inspect.signature(fn).parameters
	for name, param in params.items():
		if param.kind == inspect.Parameter.KEYWORD_ONLY and param.default == inspect.Parameter.empty:
			args.append(name)
	return tuple(args)