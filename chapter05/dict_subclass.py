# 比建议继承dict 和 list

class Mydict(dict):
	def __setitem__(self, key, value):
		super().__setitem__(key, value*2)

my_dict = Mydict(one=1)
print(my_dict)	# 并没调用重写的 __setitem__ 魔法函数

my_dict['one'] = 1	# 但是这时却调用了重写的函数
print(my_dict)
# 可见 在某些情况下重写的魔法函数不起作用(因为dict是用C语言实现的)

# 若非要继承 则应该继承 UserDict(完全用python重写过的)
from collections import UserDict
class Mydict(UserDict):
	def __setitem__(self, key, value):
		super().__setitem__(key, value*2)

print('---')
my_dict = Mydict(one=1)
print(my_dict)

my_dict['one'] = 10
print(my_dict)

from collections import defaultdict
my_dict = defaultdict(dict)	# 找不到时默认返回{} 若传入int则返回0 str->''
value = my_dict['bobby']
print(value == '')