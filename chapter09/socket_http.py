# 用socket模拟http
import socket
from urllib.parse import urlparse

def get_url(url):
	# 通过socket请求html
	url = urlparse(url)	# 提取url的各种成分
	host = url.netloc	# 主域名
	path = url.path
	if path == "":	# 如果路径为空 则需要改成以下格式
		path = "/"

	# 建立socket连接
	client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.connect((host, 80))

	# http的格式
	client.send("GET {} HTTP/1.1\r\nHost:{}\r\nConnection:close\r\n\r\n".format(path, host).encode('utf8'))

	data = b""
	while True:
		d = client.recv(1024)
		if d:
			data+=d
		else:
			break

	data = data.decode('utf-8')
	html_data = data.split('\r\n\r\n')[1]	# 去掉头信息 只要html部分
	print(data)
	client.close()

if __name__ == '__main__':
	get_url("http://www.baidu.com")