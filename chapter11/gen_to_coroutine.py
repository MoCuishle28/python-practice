"""
对协程的期望
1.用同步的方式编写异步代码
2.在适当的时候暂停函数 和 启动函数

协程的调度：事件循环+协程模式
"""

# 生成器的状态 (类似于进程的状态)
import inspect	# 用于查看生成器状态

def gen_func():
	# 含义 ： 1.返回值给调用方  2.通过send方式给gen发送值
	value = yield 1
	return  'gen_func END'

if __name__ == '__main__':
	gen = gen_func()
	print(inspect.getgeneratorstate(gen))	# 查看状态
	next(gen)
	print(inspect.getgeneratorstate(gen))
	try:
		next(gen)
	except StopIteration:
		pass
	print(inspect.getgeneratorstate(gen))