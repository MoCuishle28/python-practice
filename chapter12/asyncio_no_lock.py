import asyncio
# asyncio 不需要锁
# 只要不涉及到IO await操作 都是顺序执行

total = 0

async def add():
	global total
	for i in range(1000000):
		total += 1

async def desc():
	global total
	for i in range(1000000):
		total -= 1

if __name__ == '__main__':
	tasks = [add(), desc()]
	loop = asyncio.get_event_loop()
	loop.run_until_complete(asyncio.wait(tasks))
	print(total)