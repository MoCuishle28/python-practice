# asyncio 爬虫 去重 入库
# 使用PyQuery解析html时发生参数类型异常

import asyncio
import re

import aiohttp
import aiomysql
from pyquery import PyQuery
from secure import PASSWORD, DB

stopping = False

start_url = "http://www.jobbole.com/"

waiting_urls = []	# 待爬去的队列
seen_urls = set()	# 已经爬去的url	如果上亿条url 则需要用布隆过滤器

sem = asyncio.Semaphore(2)	# 并发度为3

async def fetch(url, session):
	# 没必要每个url都建立一次连接 session
	async with sem:	# 限制并发度为3
		await asyncio.sleep(1)
		try:
			async with session.get(url) as resp:	# get是一个网络IO的过程 需要用到async with语法
				print("url status: {}".format(resp.status))		# 状态码
				if resp.status in [200, 201]:
					data = await resp.text()	# 这里也需要await
					return data
		except Exception as e:
			print(e)

async def article_hander(url, session, pool):
	# 获取文章详情 并解析入库
	html = await fetch(url, session)
	seen_urls.add(url)

	extract_urls(html)	# 详情页里也有很多url 可以放入waiting_urls(爬去队列)内
	pq = PyQuery(html)
	title = pq("title").text()
	async with pool.acquire() as conn:
		async with conn.cursor() as cur:
			await cur.execute('SELECT 42;')
			insert_sql = "insert into article_test(title) value('{}')".format(title)
			await cur.execute(insert_sql)


# 不停地从waitting_urls 找到数据 一旦有了就启动协程完成抓取
async def consumer(pool):
	async with aiohttp.ClientSession() as session:	
		while not stopping:
			if len(waiting_urls) == 0:	# 若使用asyncio的Queue 则不需要
				await asyncio.sleep(0.5)
				continue

			url = waiting_urls.pop()	# 若消费得过快 即列表还为空时 会抛异常
			print("start get url: {}".format(url))
			if re.match("http://.*?jobbole.com/\d+/", url):	# 文章详情页的正则表达式
				if url not in seen_urls:
					asyncio.ensure_future(article_hander(url, session, pool))
					await asyncio.sleep(2)
			else:	# 若不match 即不是详情页
				if url not in seen_urls:
					# 提取该页的url
					asyncio.ensure_future(init_urls(url, session))

# 解析url
def extract_urls(html):
	urls = []
	pq = PyQuery(html)	# 使用PyQuery解析html时发生参数类型异常	TODO
	for link in pq.items('a'):	# 提取a标签 即连接
		url = link.attr('href')
		# 过滤掉空 不以http开头的 已经爬取过的 url
		if (url is not None) and (url.startswith("http")) and (url not in seen_urls):
			urls.append(url)
			waiting_urls.append(url)
	# return urls # 已经加入到waiting_urls 了，可以不用返回值

# 从网页中解析出待爬取得url
async def init_urls(url, session):
	html = await fetch(url, session)
	seen_urls.add(url)
	extract_urls(html)

async def main(loop):
	# 等待mysql连接池建立好
	pool = await aiomysql.create_pool(host='127.0.0.1', port=3306,
										user='root', password=PASSWORD,
										db=DB, loop=loop,
										charset='utf8', autocommit=True)

	# 先为url建立连接 session 的创建放在这里 就只有一次建立连接
	async with aiohttp.ClientSession() as session:	# 首先申请一个session 在session下完成
		html = await fetch(start_url, session)
		seen_urls.add(start_url)
		extract_urls(html)

	asyncio.ensure_future(consumer(pool))

if __name__ == '__main__':
	# 只要创建loop 然后不停把协程扔进去等待他的调度就好
	loop = asyncio.get_event_loop()
	asyncio.ensure_future(main(loop))
	loop.run_forever()