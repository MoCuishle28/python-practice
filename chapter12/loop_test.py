#三要点: 事件循环 + 回调(驱动生成器) + epoll(IO多路复用)
# asyncio 是python用于解决异步IO编程的一整套解决方案
# 框架 tornado(实现了web服务器,可以直接部署), gevent, twisted (scrapy, django channels)

# 使用asyncio
import asyncio
import time

from functools import partial	# 用于包装函数

async def get_html(url):
	print("start get url")
	await asyncio.sleep(2)	# 不能使用传统的time 这种同步阻塞IO(用sleep模拟IO操作)
	# time.sleep(2)	# 用这种同步阻塞会慢很多
	print('end get url')

async def get_html2(url):
	print("start get url")
	await asyncio.sleep(2)
	return 'END'

def callback(name, future):	# 这个future即是task 会自己传递进去 函数自身逻辑用到的参数 如：name要放在前面
	print('send email to ' + name)

if __name__ == '__main__':
	start_time = time.time()
	loop = asyncio.get_event_loop()	# 自带的事件循环 完成select操作 loop类似心脏

	# 批量提交
	tasks = [get_html('http://www.imooc.com') for i in range(10)]
	loop.run_until_complete(asyncio.wait(tasks))		# 阻塞的方法 类似于join方法 传入协程函数

	print('time:', time.time() - start_time)

	print('---')
	# 获取协程的返回值
	loop = asyncio.get_event_loop()

	# 这里没有传递loop 如何注册到loop的？ 没传递会自己去拿到loop 同一线程只有一个loop
	# get_future = asyncio.ensure_future(get_html2('http://www.imooc.com'))	# 返回一个future对象
	task = loop.create_task(get_html2('http://www.imooc.com'))	# 等效于上面的 asyncio.ensure_future

	task.add_done_callback(partial(callback, 'bobby'))	# 完成后callback的函数	若要传递其他参数 需要用到偏函数partial

	# loop.run_until_complete(get_future)	# 也可以接受future类型	也可以接收上面的task
	loop.run_until_complete(task)

	# print(get_future.result())	# 通过future拿到返回值		task也有result()
	print(task.result())