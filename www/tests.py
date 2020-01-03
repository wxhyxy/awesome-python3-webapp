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

def check_admin(request):
	if request.__user__ is None or not request.__user__.admin:
		raise APIPermissionErroor()
# 加密cookie
def user2cookie(user, max_age):
	# 构建cookie字符串，sha1形式
	expires = str(int(time.time()+max_age))
	s = '%s-%s-%s-%s' %(user.id, user.passwd, expires, _COOKIE_KEY)
	l = [user.id, expires, hashlib.sha1(s.encode('utf-8')).hexdigest()]
	return '-'.join(l)

# async def cookie2user(cookie_str):

@post('/api/authenticate')
async def authenticate(*, email, passwd):
		if not email:
			raise APIValueError('email', 'Invalid email.')
		if not passwd:
			raise APIValueError('passwd', 'Invalid passwd.')
		users = await User.findAll('email=?', [email])
		if len(users) == 0:
			raise APIValueError('email', 'Email not exist')
		user = users[0]
		sha1 = hashlib.sha1()
		sha1.update(user.id.encode('utf-8'))
		sha1.update(b':')
		sha1.update(passwd.encode('utf-8'))
		if user.passwd != sha1.hexdigest():
			raise APIValueError('passwd', 'Invalid password')
		r = web.Response()
		r.set_cookie(COOKIE_NAME, user2cookie(user, 86400), max_age=86400, httponly=True)
		user.passwd = '******'
		r.content_type = 'application/json'
		r.body = json.dumps(user, ensure_ascii=False).encode('utf-8')
		return r 


@get('/signout')
def signout(request):
	referer = request.headers.get('Referer')
	r = web.HTTPFound(referer or '/')
	r.set_cookie(COOKIE_NAME, '-deleted-', max_age=0, httponly=True)
	logging.info('user signed out')
	return r

# 解码cookie
async def cookie2user(cookie_str):
	if not cookie_str:
		return None
	try:
		l = cookie_str.split('-')
		if len(l) != 3:
			return None
		uid, expires, sha1 = l
		if int(expires) < time.time():
			return None
		user = await User.find(uid)
		if user is None:
			return None	
		s = '%s-%s-%s-%s'%(uid, user.passwd, expires, _COOKIE_KEY)
		if sha1 != hashlib.sha1(s.encode('utf-8')).hexdigest():
			logging.info('invalid sha1')
			return None
		user.passwd = '*******'
		return user
	except Exception as e:
		logging.exception(e)
		return None


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


@get('/signin')
async def signin():
	return {
		'__template__' :'siginin.html'
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


@post('/api/blogs')
async def api_create_blog(request, *, name, summary, content):
		check_admin(request)
		if not name or not name.strip():
			raise APIValueError('name', 'name cannot be empty')
		if not summary or not summary.strip():
			raise APIValueError('summary', 'summary cannot be empty')
		if not content or not content.strip():
			raise APIValueError('content', 'content cannot be empty')
		blogs = Blog(user_id = request.__user__.id, user_name = request.__user__.name,
			user_image = request.__user__.image, name = name.strip(), summary = summary.strip(), content = content.strip())
		await blogs.save()
		return blogs

@get('/manage/blogs/create')
def manage_create_blog():
	return {
	'__template__':'manage_blog_edit.html',	
	'id':'',
	'action':'/api/blogs'
	}