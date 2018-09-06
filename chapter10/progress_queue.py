# 多进程的通信
# 共享全局变量不适用与多进程 各个进程中的数据是完全隔离的

from multiprocessing import Process, Queue # 这个Queue可以用来通信 但这个Queue不能用于进程池
from multiprocessing import Manager # 用于进程池的通信 它里面有Queue, dict, list 等 方便共享变量

# from queue import Queue # 多进程中不能用多线程中的Queue 应该用multiprocessing中的Queue

import time
from multiprocessing import Pipe # 也可用于进程间通信 pipe性能高于Queue

# 生产者
def producer(queue):
	queue
	time.sleep(2)

# 消费者
def comsumer(queue):
	time.sleep(2)
	print(queue.get())

# 生产者
def producer2(pipe):
	pipe.send('booby')
	time.sleep(2)

# 消费者
def comsumer2(pipe):
	print(pipe.recv())

if __name__ == '__main__':
	queue = Queue(10)
	a = 1
	queue.put(a)
	my_producer = Process(target=producer, args=(queue,))
	my_comsumer = Process(target=comsumer, args=(queue,))

	my_producer.start()
	my_comsumer.start()
	my_producer.join()
	my_comsumer.join()

	recevie_pipe, send_pipe = Pipe()	# pipe只能用于两个进程间通信
	my_producer = Process(target=producer2, args=(send_pipe,))
	my_comsumer = Process(target=comsumer2, args=(recevie_pipe,))
	my_producer.start()
	my_comsumer.start()
	my_producer.join()
	my_comsumer.join()