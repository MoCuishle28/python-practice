# Global Interpreter Lock	(cpython)
# gil使得同一时刻 只有一个线程在一个cpu上执行字节码 无法将多个线程映射到多个cpu上(无法体现多核的优势)

# 但是在某种情况下gil会被释放
# 根据字节码执行的行数 或 时间片释放 还有I/O操作也会释放
# 类似于OS的进程调度
total = 0

def add():
	global total
	for i in range(1000000):
		total += 1

def desc():
	global total
	for i in range(1000000):
		total -= 1

import threading

thread1 = threading.Thread(target=add)
thread2 = threading.Thread(target=desc)
thread1.start()
thread2.start()

thread1.join()
thread2.join()
print(total)