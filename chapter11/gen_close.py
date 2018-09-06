# 关闭生成器

def gen_func():
	html = yield  'http://xxx.com'
	print(html)
	yield 2
	yield 3
	return 'END'

if __name__ == '__main__':
	gen = gen_func()
	print(next(gen))
	gen.close()	# 生成器内部抛出一个异常 且是继承BaseException(最基础的异常) 没有继承 Exception
	next(gen)