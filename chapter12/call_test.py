import asyncio

def callback(sleep_times):
	print('sleep {} success at {}'.format(sleep_times, loop.time()))

def stop_loop(loop):
	loop.stop()

if __name__ == '__main__':
	loop = asyncio.get_event_loop()
	# callback的参数 2
	loop.call_soon(callback, 2)	# 在loop中可以插入函数 在队列中等待到下一次循环到来就马上执行
	# loop.call_soon(stop_loop, loop)

	now = loop.time()	# loop内部的时间
	loop.call_at(now + 1, callback, 3)	# 在特定时间调用
	# 内部也是调用了call_at函数
	loop.call_later(3, stop_loop, loop)		# 4秒后调用 若有多个 不会按添加顺序调用 会根据时间排定调用的先后顺序

	loop.run_forever()		# 启动loop 不是协程要用run_forever() 会一直运行