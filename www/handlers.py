# 测试连接数据库

import orm
from models import User 
import aiomysql, asyncio
print(1)
from coroweb import get, post

# async def test(loop):
# 		print('start...')
# 		await orm.create_pool(loop, user='root',password='mysql',db='awesome')

# 		u = User(name = 'Test', email = 'w.3097652.rt@163.com', passwd = 'wangrui', image = 'about:blank')

# 		await u.save()
# 		print('baocun')

@get('/')
async def index(request):
		users = await User.findAll()
		return {
			'__template__' : 'test.html',
			'users' : users,
		}


# if __name__ == '__main__':
# 	loop = asyncio.get_event_loop()
# 	loop.run_until_complete(test(loop))
# 	print(123)
# 	loop.close()