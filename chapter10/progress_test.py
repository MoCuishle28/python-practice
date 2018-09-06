"""
多进程编程
耗cpu操作(计算) 用多进程编程
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# 多进程
from concurrent.futures import ProcessPoolExecutor

# 举个耗cpu的例子
def fib(n):
	if n<=2:
		return 1
	return fib(n-1)+fib(n-2)

# 模拟IO操作
def random_sleep(n):
	time.sleep(n)
	return n

# 在windows下用线程池和进程池 要放入 if __name__ == '__main__' 内部
if __name__ == '__main__':
	# 以下模拟一个在计算量大情况下 多进程优于多线程的例子
	with ThreadPoolExecutor(3) as executor:
		all_task = [executor.submit(fib, (num)) for num in range(25, 35)]
		start_time = time.time()
		for future in as_completed(all_task):
			data = future.result()
			print("{} done".format(data))

		print("last time is {}".format(time.time() - start_time))


	with ProcessPoolExecutor(3) as executor:
		all_task = [executor.submit(fib, (num)) for num in range(25, 35)]
		start_time = time.time()
		for future in as_completed(all_task):
			data = future.result()
			print("{} done".format(data))

		print("last time is {}".format(time.time() - start_time))

	print('----------')

	# 模拟多IO操作下 多线程优于多进程
	with ThreadPoolExecutor(3) as executor:
		all_task = [executor.submit(random_sleep, (num)) for num in [2]*30]
		start_time = time.time()
		for future in as_completed(all_task):
			data = future.result()
			print("{} done".format(data))

		print("last time is {}".format(time.time() - start_time))


	with ProcessPoolExecutor(3) as executor:
		all_task = [executor.submit(random_sleep, (num)) for num in [2]*30]
		start_time = time.time()
		for future in as_completed(all_task):
			data = future.result()
			print("{} done".format(data))

		print("last time is {}".format(time.time() - start_time))