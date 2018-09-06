# 3.5之后支持原生的协程
# 引入 async await(可以对比于yield from) 

from collections import Awaitable # 关键在实现 __await__ 魔法函数

# 要有async才能放在await后 或者 加上types.coroutine装饰器(要import types)
async def downloader(url):
	return 'bob'	# 和子生成器一样 return会抛出异常

async def download_url(url):
	# 在async不能用yield 和 yield from
	# await 后面的是Awaitable对象
	html = await downloader(url)	# await 只能在async中
	return html

if __name__ == '__main__':
	coro = download_url('http://www.xxx.com')
	coro.send(None)