# 测试连接数据库

import orm, re, hashlib, json
from aiohttp import web
from models import * 
import aiomysql, asyncio
from coroweb import get, post
from apis import *
from config import configs

# async def test(loop):
# 		print('start...')
# 		await orm.create_pool(loop, user='root',password='mysql',db='awesome')

# 		u = User(name = 'Test', email = 'w.3097652.rt@163.com', passwd = 'wangrui', image = 'about:blank')
# 		await u.save()
# 		print('baocun')

COOKIE_NAME = 'awesession'
_COOKIE_KEY = configs.get('session').get('secret')
def user2cookie(user, max_age):
	# 构建cookie字符串，sha1形式
	expires = str(int(time.time()+max_age))
	s = '%s-%s-%s-%s' %(user.id, user.passwd, expires, _COOKIE_KEY)
	l = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
	return '-'.join(l)

# async def cookie2user(cookie_str):


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


@get('/register')
async def register():
	return {
		'__template__' : 'register.html'
	}


_RE_EMAIL = re.compile('^[a-z0-9\.\-\_]+\@[a-z0-9\-\_]+(\.[a-z0-9\-\_]+){1,4}$')
_RE_SHA1 = re.compile('^[0-9a-z]{40}$')

@post('/api/users')
async def aip_register_users(*, name, email, passwd):
		if not name or not name.strip():
			raise APIValueError('name')
		if not email or not _RE_EMAIL.match(email):
			raise APIValueError('email')
		if not passwd or not _RE_SHA1.match(passwd):
			raise APIValueError('passwd')
		users = await User.findAll('email=?',[email])
		if len(users) > 0:
			raise APIError('register failed', 'email', 'email is already in use')
		uid = next_id()
		sha1_passwd = '%s:%s'%(uid, passwd)
		users = User(id=uid, name=name.strip(),email=email, passwd=hashlib.sha1(sha1_passwd.encode('utf-8')).hexdigest(),
			image = 'http://www.gravatar.com/avatar/%s?d=mm&s=120'% hashlib.md5(email.encode('utf-8')).hexdigest()
			)
		await users.save()
		r = web.Response()
		r.set_cookie(COOKIE_NAME, user2cookie(users, 86400), max_age = 86400, httponly = True)
		users.passwd = '******'
		r.content_type = 'application/json'
		r.body = json.dumps(users, ensure_ascii=False).encode('utf-8')
		return r

