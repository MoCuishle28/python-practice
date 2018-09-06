def function():
	try:
		print(1)
		raise Exception
		return 1
	except Exception as e:
		print(2)
		return 2
	else:
		print(3)
		return 3
	finally:
		print(4)
		return 4
	return 5	# 不会放入堆栈？

print('function:',function())

# 上下文管理器协议
class Sample:
	a = 10
	def __enter__(self):
		print('enter')
		return self

	def __exit__(self, exc_type, exc_val, exc_tb):
		print('exit')

	def do(self):
		print('do')

with Sample() as s:
	s.do()