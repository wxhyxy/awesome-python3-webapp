# 测试连接数据库

import orm
from models import *
import aiomysql, asyncio


def test(loop):
	print('start...')
	yield from orm.create_pool(loop, user='root',password='mysql',db='awesome')

	u = User(name = 'Test', password = 'wangrui', email = 'w.3097652.rt@163.com', image = 'about:blank')

	yield from u.save()
	print('baocun')


print(123)
test()