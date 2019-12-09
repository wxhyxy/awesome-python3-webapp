import aiomysql
import asyncio
import logging


async def create_pool(loop, **kw):
		logging.info('create database connection pool...')
		global __pool
		# 数据库连接设置
		__pool = await aiomysql.create_pool( 
			host = kw.get('host', 'localhost'),
			port = kw.get('port', 3306),
			user = kw['user'],
			password = kw['password'],
			db = kw['db'],
			charset = kw.get('charset', 'utf8'),
			autocommit = kw.get('autocommit', True),
			maxsize = kw.get('maxsize', 10),
			minsize = kw.get('minsize', 1),
			loop = loop
			)


# 执行select语句，用select函数执行。
async def select(sql, args, size=None):
	log(sql, args)
	global __pool
	async with __pool.get as conn:
		await with conn.cursor(aiomysql.DictCursor) as cur:
			await cur.execute(sql.replace('?', '%s'), args or ())
			if size: # 如果传入size，获取最多指定数量的记录否则返回所有的数据
				rs = await cur.fetchmany(size)
			else:
				rs = await cur.fetchall()
			logging.info('rows returned: %s' %len(rs))
			return rs

# 要执行INSERT、UPDATE、DELETE语句，可以定义一个通用的execute()函数，因为这3种SQL的执行都需要相同的参数，以及返回一个整数表示影响的行数：
async def execute(sql, args, autocommit=True):
	log(sql)
	async with __pool.get as conn:
		if not autocommit:
			await conn.begin()
		try:
			async with conn.coursor() as cur:
				await cur.execute(sql.execute(sql.replace('?', '%s'), args))
				affected = cur.rowcount
			if not autocommit:
				await conn.begin()
		except BaseException as e:
			if not autocommit:
				await conn.rollback()
			raise 
		return affected


def craete_args_string(num):
	l = []
	for n in range(num):
		l.append('?')
	return ','.join(l)


class Field(object):

	def __init__(self, name, column_type, primary_key, default):
		self.name = name
		self.column_type = column_type
		self.primary_key = primary_key
		self.default = default


	def __str__(self):
		return '<%s, %s:%s>' % (self.__class__.__name__, self.column_type, self.name)


class StringField(Field):

	def __init__(self, name = None, primary_key=False, default=None, ddl='varchar(100)'):
		super().__init__(name, ddl, primary_key, default)

class BooleanField(Field):

	def __init__(self, name = None, default=False):
		super().__init__(name, 'boolean', False, default)

class IntegerField(Field):

	def __init__(self, name = None, primary_key=False, default=0):
		super.__init__(self, 'bigint', primary_key, default)

class FloatField(Field):

	def __init__(self, name=None, primary_key=False, default=0.0):
		super.__init__(self, 'real',primary_key, default)

class TextField(Field):

	def __init__(self, name = None, default=None):
		










