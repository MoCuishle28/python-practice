"""
python3.3的新加语法 yield from
yield from	后面跟一个iterable对象
"""

from itertools import chain	# 可以将迭代对象链起来 通过一次迭代访问

my_list = [1,2,3]
my_dict = {
	'bob1':'http://www.xxx.com',
	'bob2':'http://www.yyy.com'
}

# 自己实现一个chain
def my_chain(*args, **kwargs):
	for my_iterable in args:
		for value in my_iterable:
			yield value

# 通过yield from 实现的版本
def my_chain_yield_from(*args, **kwargs):
	for my_iterable in args:
		print('====',my_iterable)
		yield from my_iterable	# 可以将my_iterable(迭代器) 里面的值一个一个地yield出来

for value in chain(my_list, my_dict, range(5,10)):
	print(value)

print('---')
for value in my_chain(my_list, my_dict, range(5,10)):
	print(value)

# yield from 会把后面的迭代器的值拿出来 一个一个地yield
print('---')
for value in my_chain_yield_from(my_list, my_dict, range(5,10)):
	print(value)

"""------------------------------------------------------------------------------"""

def g1(iterable):
	yield iterable

def g2(iterable):
	yield from iterable

for value in g1(range(5)):
	print(value)

print('---')
for value in g2(range(5)):
	print(value)