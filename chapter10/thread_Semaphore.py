"""
semaphore 信号量
用于控制进入数量的锁	比如爬虫并发太高会被封
"""

import threading
import time

class HtmlSpider(threading.Thread):
	def __init__(self, url, sem):
		super().__init__()
		self.url = url
		self.sem = sem

	def run(self):
		time.sleep(2)
		print('got html text success.')
		self.sem.release()

class UrlProducer(threading.Thread):
	def __init__(self, sem):
		super().__init__()
		self.sem = sem

	def run(self):
		for i in range(20):
			self.sem.acquire()	# 每调用一次 数量减一(这里初始设定是3) 为0时会阻塞
			html_thread = HtmlSpider("http://baidu.com/{}".format(i), self.sem)
			html_thread.start()

if __name__ == '__main__':
	sem = threading.Semaphore(3)	# 一次允许3个并发
	url_producer = UrlProducer(sem)
	url_producer.start()