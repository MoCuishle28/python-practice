# 通过 asyncio 完成http请求
# asyncio 没有提供http的接口	(aiohttp是基于asyncio的 提供了)

import asyncio
import socket
from urllib.parse import urlparse

import time

# 改为协程的方式
async def get_url(url):
	url = urlparse(url)	# 提取url的各种成分
	host = url.netloc	# 主域名
	path = url.path
	if path == "":	# 如果路径为空 则需要改成以下格式
		path = "/"

	# 用协程建立socket连接
	reader, writer = await asyncio.open_connection(host, 80)	# 参数 -> host 和 端口

	# 类比socket那里的send write内部还是调用了send
	writer.write("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode('utf8'))

	all_lines = []
	async for raw_line in reader:	# 新语法  将for循环语法异步化
		data = raw_line.decode('utf-8')
		all_lines.append(data)
	html = "\n".join(all_lines)
	return html

async def main():
	tasks = []	# 管理多个task
	for url in range(20):
		url = "http://shop.projectsedu.com/goods/{}/".format(url)
		tasks.append(asyncio.ensure_future(get_url(url)))	# 套上ensure_future 可以返回future 方便获得协程的结果 状态 等
	for task in asyncio.as_completed(tasks):	# 某一个协程完成 则立马返回
		result = await task 	# 完成一个 拿到一个结果
		print(result)

if __name__ == '__main__':
	start_time = time.time()
	loop = asyncio.get_event_loop()

	# tasks = []	# 管理多个task
	# for url in range(20):
	# 	url = "http://shop.projectsedu.com/goods/{}/".format(url)
	# 	tasks.append(asyncio.ensure_future(get_url(url)))	# 套上ensure_future 可以返回future 方便获得协程的结果 状态 等
	# loop.run_until_complete(asyncio.wait(tasks))

	loop.run_until_complete(main())	# 想要每完成一个协程就操作一个结果 需要借组main协程

	# for task in tasks:	# 全部完成后拿出结果
	# 	print(task.result())

	print('last time :', time.time() - start_time)