# 测试连接数据库

import orm
from models import * 
import aiomysql, asyncio
from coroweb import get, post

# async def test(loop):
# 		print('start...')
# 		await orm.create_pool(loop, user='root',password='mysql',db='awesome')

# 		u = User(name = 'Test', email = 'w.3097652.rt@163.com', passwd = 'wangrui', image = 'about:blank')

# 		await u.save()
# 		print('baocun')
@get('/')
async def index(request):
		summary = 'Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua'
		blogs = [
			Blog(id='1', name='Test Blog', summary=summary, created_at = time.time()-120),
			Blog(id='2', name='王瑞', summary=summary, created_at = time.time()-3600),
			Blog(id='3', name='yxy', summary=summary, created_at = time.time()-7200)
		]
		return {
			'__template__': 'test.html',
			'blogs': blogs
		}

# if __name__ == '__main__':
# 	loop = asyncio.get_event_loop()
# 	loop.run_until_complete(test(loop))
# 	print(123)
	# loop.close()
@get('/api/users')
async def api_get_users():
		users = await User.findAll(orderBy='created_at desc')
		for u in users:
			u.passwd = '******'
		return dict(users = users)