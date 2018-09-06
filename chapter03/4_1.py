"""Python 的鸭子类型(多态)"""

class Cat(object):
	def say(self):
		print('cat')

class Dog(object):
	def say(self):
		print('Dog')

class Duck(object):
	def say(self):
		print('duck')

a = Cat
a().say()
print('---')
a_list = [Cat, Dog, Duck]
for t in a_list:
	t().say()

a = [1,2]
b = set()
b.add('a')
b.add(4)
a.extend(b)	# 只要是可迭代的对象都行
print(a)