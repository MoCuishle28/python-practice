import socket
"""socket是和http同一层的 是个与TCP,UDP那一层的接触的接口 可以用socket编写自己的应用层协议"""
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 8000))
print('server start...')
server.listen()

def handot_socket(sock, addr):
	while True:
		# 获取从客户端发送的数据
		data = sock.recv(1024)	# 一次获取1k(1024)的数据
		print(data.decode('utf-8'))

		ret_data = input()
		sock.send(ret_data.encode('utf-8'))

cnt = 1
while True:
	sock, addr = server.accept()
	print('No.',cnt,'client enter.')
	cnt+=1
	# 用线程处理新接收的连接
	client_thread = threading.Thread(target=handot_socket, args=(sock, addr))
	client_thread.start()

print('server close...')
sock.close()
server.close()