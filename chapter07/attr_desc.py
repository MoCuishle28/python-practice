import numbers

# 属性描述符
class IntField:
	def __get__(self, instance, owner):
		return self.value

	# 赋值时调用
	def __set__(self, instance, value):
		print('__set__')
		# 判断是否为int类型
		if not isinstance(value, numbers.Integral):
			raise ValueError('I need int!!!!!!!!!')
		if value < 0:
			raise ValueError('Must larger zero!!!!!!!!')
		# instance就是该类的实例本身 没错则把value保存起来
		self.value = value

	def __delete__(self, instance):
		pass

class NonDataIntField:
	pass
	# 非属性描述符
	# def __get__(self, instance, owner):
	# 	return self.value

# 数据库的映射模型
class User:
	# 数据描述符会优先用__get__
	age = IntField()	# 不会放入user的__dict__

	# 非属性描述符会优先在__dict__中找
	# age = NonDataIntField()	# 非属性描述符 会放入__dict__

if __name__ == '__main__':
	user = User()
	user.age = 30
	print('dict', user.__dict__)
	print(getattr(user, 'age'))
	# print(user.age)
	print('||||||||||')

	user.age = 'a'
	print(user.age)