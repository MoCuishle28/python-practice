"""
元类编程 元类是创建类的类
类也是对象 type是创建类的类
type -> class(类) -> 对象
"""

# 动态创建类
def create_class(name):
	if name == 'user':
		class User:
			def __str__(self):
				return 'user'
		return User

	elif name == 'company':
		class Company(object):
			def __str__(self):
				return 'company'
		return Company

def say(self):
	return 'i am ' + self.name

class BaseClass:
	def answer(self):
		return 'I am Base'

# 用metaclass控制类的创建过程
class MetaClass(type):
	def __new__(cls, *args, **kwargs):
		print('MetaClass __new__')
		return super().__new__(cls, *args, **kwargs)	# 这里与之前不同 要加入 *args, **kwargs

# 在创建创建User类的过程 会通过metaclass创建User 若没metaclass则会用type创建
class User2(metaclass=MetaClass):
	def __init__(self, name):
		self.name = name

	def __str__(self):
		return self.name

if __name__ == '__main__':
	MyClass = create_class('user')
	my_obj = MyClass()
	print(my_obj, type(my_obj))
	
	# 通过type动态创建类 参数: 1.类名 2.继承(最后一个要带 , ) 3.属性(变量 方法)
	User = type('User', (BaseClass, ), {'name':'fuck you', 'say':say})
	my_obj = User()
	print(my_obj, type(my_obj))
	print(my_obj.name)
	print(my_obj.answer())
	print(my_obj.say())

	print('---')
	user = User2('bobby')
	print(user)