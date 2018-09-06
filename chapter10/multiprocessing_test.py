# import os
# import time

# # fork() 只能在linux/unix 下用 会创建一个子进程
# pid = os.fork()
# print('MoCuishle')
# if pid == 0:
# 	print('子进程 {}, 父进程 {}'.format(os.getpid(), os.getppid()))
# else:
# 	print('我是父进程 {}'.format(pid))

# time.sleep(2)

from concurrent.futures import ProcessPoolExecutor	# 推荐使用这个做多进程
import multiprocessing	# 较为偏底层 不推荐
import time

def get_html(n):
	time.sleep(n)
	print('get html success')
	return n

if __name__ == '__main__':
	# 较为底层的多进程编程方式
	progress = multiprocessing.Process(target=get_html, args=(1,))	# 也可以通过继承的方式 （同线程）
	print('pid',progress.pid)	# 进程id
	progress.start()
	print('pid',progress.pid)
	progress.join()
	print('main end')
	print('---')

	# 进程池
	pool = multiprocessing.Pool(multiprocessing.cpu_count())	# 若不传入参数则默认进程数为cpu数量

	# 逐个任务提交的写法
	# result = pool.apply_async(get_html, args=(3,))	# 提交任务

	# pool.close()	# join之前必须close 即池不再接收任务
	# pool.join()	# 等待所有任务完成
	# print(result.get())

	# 以下为批量提交写法
	# imap() 类似之前ProcessPoolExecutor的map方法
	for result in pool.imap(get_html, [5,1,3]):	# result顺序和添加顺序一样
		print("{} done".format(result))

	for result in pool.imap_unordered(get_html, [5,1,3]):	# 谁先完成 打印谁
		print("{} done".format(result))