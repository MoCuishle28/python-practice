from threading import Lock, RLock 
# RLock是 python提供的可重入的锁（即 在同一线程可以连续多次调用acquire，不同线程间还是只能由一次 不过要有相应次数的release）
# 锁影响性能
# 可能引起死锁

total = 0
lock = Lock()	# 声明一把锁

def add():
	global total
	global lock
	for i in range(1000000):
		lock.acquire()
		total += 1
		lock.release()

def desc():
	global total
	global lock
	for i in range(1000000):
		lock.acquire()
		total -= 1
		lock.release()

import threading

thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)
thread1.start()
thread2.start()

thread1.join()
thread2.join()
print(total)