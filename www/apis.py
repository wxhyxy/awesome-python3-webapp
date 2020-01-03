#coding = utf-8

import json, logging, inspect, functools


# 分页功能

class Page(object):

	def __init__(self, item_count, page_index=1, page_size = 10):
		self.item_count = item_count
		self.page_size = page_size
		self.page_count = item_count//page_size+(1 if item_count%page_size>0 else 0)
		if (item_count==0) or (page_index > self.page_count):
			self.offset = 0
			self.limit = 0
			self.page_index = 1
		else:
			self.page_index = page_index
			self.offset = self.page_size * (page_index-1)
			self.limit = self.page_index < self.page_count
		self.has_next = self.page_index < self.page_count
		self.has_prev = self.page_index > 1

	def __str__(self):
		return 'item_count:%s,page_count:%s,page_index:%s,page_size:%s,offset:%s. limit:%s'%(self.item_count
			,self.page_count,self.page_index, slef.page_size, self.offset, self.limit)

	__repr__ = __str__

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