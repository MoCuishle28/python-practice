from concurrent.futures import ThreadPoolExecutor, as_completed	# 用于获取已经完成的任务(是一个生成器)
from concurrent.futures import wait, FIRST_COMPLETED
# 多进程 多线程的包 （有线程池）

# 为什么用线程池?
# 主线程可以获得某个线程的状态和返回值
# 当某线程完成时 主线程能立即知道
# futures能让多线程 多进程的编码接口一致

import time

def get_html(times):
	time.sleep(times)
	print("get page {} success".format(times))
	return times

# 实例化线程池
executor = ThreadPoolExecutor(max_workers=2)	# max_workers=2 该线程池同时运行的线程个数 可以提交任意多个执行任务

# 提交执行的函数到线程池中 线程池会自己调度
task1 = executor.submit(get_html, (2))	# 返回的是futures对象 会立即返回 不会阻塞
task2 = executor.submit(get_html, (1))

print(task1.done())	# 可以知道此线程是否完成
print('cancel result:',task2.cancel())	# 可以取消一个执行(返回True/False) 执行中不能取消 若未执行则能取消

time.sleep(3)
print(task1.done())

print(task1.result())	# 是一个阻塞的结果 得到执行的返回值
print('---')

# 常用的模式
urls = [3,2,4]	# 假设有3个url
all_task = [executor.submit(get_html, (url)) for url in urls]	# 批量提交
for future in as_completed(all_task):
	data = future.result()
	print("{} done".format(data))

print('---')
# 通过 executor 执行并同时获取已经完成的任务 data的获得顺序不是执行完成的先后顺序 而是urls里的顺序
for data in executor.map(get_html, urls):	# map即将urls的内容逐个提交到前面参数传入的函数里执行
	print("{} done".format(data))

wait(all_task)	# 让主线程等待所有线程完成 亦可以通过参数return_when=FIRST_COMPLETED使第一个线程完成就继续
print("all_task done")