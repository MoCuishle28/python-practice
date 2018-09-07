import asyncio
from asyncio import Lock	# 接口与多线程的Lock一致
from asyncio import Queue	# asyncio 的Queue 通信时用到

import aiohttp
# asyncio 需要锁的情况

lock = Lock()
cache = {}

async def get_stuff(url):
	# 协程的lock是代码级别的 因为协程是单线程的 不需要OS的lock
	async with lock:	# 请求一把锁是要等待的(协程) 所以加await 或在前面加async 这里等同于lock.acquired() lock.release()
		if url in cache:
			return cache[url]
		stuff = await aiohttp.request('GET', url)
		cache[url] = stuff
		return stuff

async def parse_stuff():
	stuff = await get_stuff('http://www.baidu.com')
	# do something parse

async def use_stuff():
	stuff = await get_stuff('http://www.baidu.com')
	# use stuff to do something interesting

tasks = [parse_stuff(), use_stuff()]