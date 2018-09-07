"""loop会被放入future中"""

import asyncio
import time

# 如何取消future (task)

async def get_html(sleep_times):
	print('waiting')
	await asyncio.sleep(sleep_times)
	print("done after {}s".format(sleep_times))

if __name__ == '__main__':
	task1 = get_html(2)
	task2 = get_html(3)
	task3 = get_html(3)

	tasks = [task1, task2, task3]

	loop = asyncio.get_event_loop()
	try:
		loop.run_until_complete(asyncio.wait(tasks))		# 原生注册了回调函数里有stop loop的功能
	except KeyboardInterrupt as e:	# ctrl + c
		all_tasks = asyncio.Task.all_tasks()	# 获取所有的task
		for task in all_tasks:
			print('cancel task')
			print(task.cancel())
		loop.stop()
		loop.run_forever()	# stop之后还要调用一次run_forever() 否则会抛异常
	finally:
		loop.close()
