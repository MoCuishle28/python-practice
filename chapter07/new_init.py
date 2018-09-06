class User:
	# 允许我们在生成对象之前加入逻辑 传入类cls args是元组的形式 kw是字典
	def __new__(cls, *args, **kwargs):
		print('__new__', 'tuple:',args, 'dict:',kwargs)
		
		# 如果__new__不返回对象 则不会调用__init__
		return super().__new__(cls)

	def __init__(self, age,name):
		print('__init__')
		self.name = name
		self.age = age

if __name__ == '__main__':
	user = User(10, name='a')	# 10放入args    name:'a'放入kw
	print(user.name, user.age)