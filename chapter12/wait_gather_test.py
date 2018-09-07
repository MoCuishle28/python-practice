import asyncio
import time

# wait gather
async def get_html(url):
	print("start get url"+url)
	await asyncio.sleep(2)	# 不能使用传统的time 这种同步阻塞IO(用sleep模拟IO操作)
	print('end get url')

if __name__ == '__main__':
	start_time = time.time()
	loop = asyncio.get_event_loop()	# 自带的事件循环 完成select操作

	tasks = [get_html('http://www.imooc.com') for i in range(10)]

	# wait() 可以对应于线程池的wait
	loop.run_until_complete(asyncio.wait(tasks))		# 阻塞的方法 类似于join方法 传入协程函数
	# loop.run_until_complete(asyncio.gather(*tasks))

	print('time:', time.time() - start_time)
	print('---')

	"""
	gather 和 wait 的区别:
	1.gather 更加高层
	2.gather 可以分组取消(cancel函数)
	3.gather 更灵活
	推荐优先使用gather
	"""
	start_time = time.time()
	loop = asyncio.get_event_loop()	# 自带的事件循环 完成select操作

	group1 = [get_html('http://www.imooc.com') for i in range(3)]
	group2 = [get_html('http://www.baidu.com') for i in range(3)]


	group1 = asyncio.gather(*group1)
	group2 = asyncio.gather(*group2)
	loop.run_until_complete(asyncio.gather(group1, group2))	

	# 另一种写法 省略对group1 group2的两步预处理
	# loop.run_until_complete(asyncio.gather(*group1, *group2))

	print('time:', time.time() - start_time)