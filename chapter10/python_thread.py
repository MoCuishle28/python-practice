# 对于I/O操作为主的程序 多线程和多进程性能差别不大
import time
import threading

def get_detail_html(url):
	print('get_detail_html started')
	time.sleep(2)
	print('get_detail_html end')

def get_detail_url(url):
	print('get_detail_url started')
	time.sleep(4)
	print('get_detail_url end')

# 还可以通过继承Thread实现线程
class GetDetailHtml(threading.Thread):
	def __init__(self, name):
		super().__init__(name=name)

	# 重载run方法
	def run(self):
		print('get_detail_html started')
		time.sleep(2)
		print('get_detail_html end')		

class GetDetailUrl(threading.Thread):
	def __init__(self, name):
		super().__init__(name=name)

	def run(self):
		print('get_detail_url started')
		time.sleep(4)
		print('get_detail_url end')

if __name__ == '__main__':
	t1 = threading.Thread(target=get_detail_html, args=("",))
	t2 = threading.Thread(target=get_detail_url, args=("",))

	t1.setDaemon(True)	# 当主线程退出时,子线程kill(原来不会kill) 即设置为守护线程
	t2.setDaemon(True)

	start_time = time.time()
	t1.start()
	t2.start()

	t1.join()
	t2.join()
	print('last time:{}'.format(time.time() - start_time))

	print('---')
	t1 = GetDetailHtml('A')
	t2 = GetDetailUrl('B')
	start_time = time.time()
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	print('last time:{}'.format(time.time() - start_time))