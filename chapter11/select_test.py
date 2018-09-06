# select 与 epoll
# 在并发高 且连接活跃度低时 epoll好
# 在并发不高 且连接活跃度高时(即建立连接后 会一直有后续操作 不会经常断开) select好


# 通过select 实现http请求
import socket
from urllib.parse import urlparse
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
urls = ["http://www.baidu.com"]
stop = False

class Fetcher:
	def connected(self, key):
		selector.unregister(key.fd)	# 要先注销
		self.client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(self.path, self.host).encode('utf8'))
		selector.register(self.client.fileno(), EVENT_READ, self.readable)	# 又要重新注册读事件

	def readable(self, key):

		# 不要用循环一直recv 因为状态为readable时 并不代表可以一直从内核复制数据到用户空间 会报错
		# 只要是readable状态 就会调用readable函数 所以每次调用只要读一次
		d = self.client.recv(1024)
		if d:
			self.data+=d
		else:
			selector.unregister(key.fd)
			self.data = self.data.decode('utf-8')
			html_data = self.data.split('\r\n\r\n')[1]	# 去掉头信息 只要html部分
			print(html_data)
			self.client.close()
			urls.remove(self.spider_url)	# 每处理完一个url就删除一个
			if not urls:
				global stop
				stop = True

	def get_url(self, url):
		self.spider_url = url
		url = urlparse(url)	# 提取url的各种成分
		self.host = url.netloc	# 主域名
		self.path = url.path
		self.data = b""

		if self.path == "":	# 如果路径为空 则需要改成以下格式
			self.path = "/"

		# 建立socket连接
		self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.client.setblocking(False)	# 连接不阻塞 直接返回
		try:
			self.client.connect((self.host, 80))
		except BlockingIOError as e:
			pass
		
		# 注册	fileno是文件描述符  注册写事件(建立连接后要send)  回调函数(当可写时应该执行的逻辑)
		selector.register(self.client.fileno(), EVENT_WRITE, self.connected)	# 注册完就可以在loop中找到是否准备好

# 回调要自己来做
def loop():
	# 事件循环 不停请求socket状态 并调用回调函数
	while not stop:
		ready = selector.select()
		for key, mask in ready:
			call_back = key.data
			call_back(key)	# 调用回调函数

if __name__ == '__main__':
	fetcher = Fetcher()
	fetcher.get_url("http://www.baidu.com")
	loop()