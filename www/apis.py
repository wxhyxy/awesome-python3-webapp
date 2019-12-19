#coding = utf-8

import json, logging, inspect, functools

class APIError(Exception):
	def __init__(self, error, data='', message=''):
		super(APIError, self).__init__(message)
		self.error = error
		self.data = data
		self.message = message


class APIValueError(Exception):

	def __init__(self, field, message = ''):
		super(APIValueError, self).__init__('value:invalid', field, message)


class APIResourcelNotFoundError(APIError):

	def __init__(self, field, message):
		super(APIResourcelNotFoundError, self).__init__('value:not found', field, message)


class APIermissionError(APIError):

	def __init__(self, message = ''):
		super(APIermissionError, self).__init__('permission:forbidden', 'permission', message)