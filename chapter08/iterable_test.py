# 迭代协议 -> __iter__
# 迭代器必须实现 __iter__()   __next__()
# 可迭代类型只需要实现 __iter__()

from collections.abc import Iterable, Iterator

class Company(object):
	def __init__(self, employee_list):
		self.employee_list = employee_list

	def __getitem__(self, item):
		return self.employee_list[item]

# 用自定义迭代器维护其他自定义类的迭代
class MyIterator(Iterator):
	def __init__(self, employee_list):
		self.employee_list = employee_list
		self.index = 0	# 用于返回迭代位置

	# 真正返回迭代值得逻辑
	def __next__(self):
		try:
			word = self.employee_list[self.index]
		except IndexError:
			raise StopIteration
		self.index += 1
		return word
		
# 把 Company 做成迭代器	把__next__放在迭代器里实现
class Iter_Company(MyIterator):
	def __init__(self, employee_list):
		self.employee_list = employee_list

	def __iter__(self):
		return MyIterator(self.employee_list)
		

if __name__ == '__main__':
	a = [1, 2]
	print(isinstance(a, Iterable))
	print(isinstance(a, Iterator))

	iter_rator = iter(a)	# 会返回迭代器
	print(isinstance(iter_rator, Iterator))
	print('---')

	c = Company(['tom', 'jane', 'bob'])
	for item in c:		# 实际上 在for循环时 python会尝试调用 iter(c) 若有__iter__则调用 若没有则用__getitem__创建一个迭代器
		print(item)
	print('---')

	my_itor = iter(c)
	while True:
		try:
			print(next(my_itor))	# next接收一个iterator对象 for循环内部也是在不停调用next直到抛出异常
		except StopIteration:
			print('---END---')
			break
	
	c = Iter_Company(['bob', 'jane', 'tom'])
	for i in c:
		print(i)