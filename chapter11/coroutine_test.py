# 协程 -> 可以暂停的函数	(生成器可以暂停)
# 生成器不止可以产出值 还可以接收值

def gen_func():
	# 1.可以产出值	2.可以接收值
	html = yield 'http://projectsedu.com'
	print('gen_func:',html)
	yield 2
	return 'END'

if __name__ == '__main__':
	gen = gen_func()
	# 启动生成器的方式: 1.next()	2.send
	# 在调用send发送非none值之前 必须先启动一次生成器	方式: 1.gen.send(None) 2.next(gen)
	url = next(gen)	# 第一次调用生成器时 只能send(None)
	html = 'booby'
	print(gen.send(html))	# send可以传入值到生成器内部	同时可以重启生成器到下一个yield的位置(即 send也包含了next的效果 但未启动一次生成器前特殊)
	