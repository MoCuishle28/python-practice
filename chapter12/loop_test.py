#三要点: 事件循环 + 回调(驱动生成器) + epoll(IO多路复用)
# asyncio 是python用于解决异步IO编程的一整套解决方案
# 框架 tornado(实现了web服务器,可以直接部署), gevent, twisted (scrapy, django channels)

# 使用asyncio
import asyncio
import time

async def get_html(url):
	print("start get url")
	await asyncio.sleep(2)	# 不能使用传统的time 这种同步阻塞IO(用sleep模拟IO操作)
	# time.sleep(2)	# 用这种同步阻塞会慢很多
	print('end get url')

if __name__ == '__main__':
	start_time = time.time()
	loop = asyncio.get_event_loop()	# 自带的事件循环 完成select操作 loop类似心脏

	# 批量提交
	tasks = [get_html('http://www.imooc.com') for i in range(10)]
	loop.run_until_complete(asyncio.wait(tasks))		# 阻塞的方法 类似于join方法 传入协程函数

	print('time:', time.time() - start_time)