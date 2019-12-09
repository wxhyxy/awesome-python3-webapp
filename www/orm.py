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
async def execute(sql, args):
	log(sql)
	async with __pool.get as conn:
		try:
			async with conn.coursor() as cur:
				affected = cur.rowcount()
		except BaseException as e:
			raise 
		return affected