# __getattr__ 	查找不到属性时调用
# __getattribute__	找不找得到都会调用

class User:
	def __init__(self, name):
		self.name = name

	def __getattr__(self, item):
		print('item:',item)
		return 'not find this attr'

	# 尽量不要重写
	# def __getattribute__(self, item):
	# 	return 'fuck me!'

if __name__ == '__main__':
	user = User('a')
	print(user.name)
	print('---')
	print(user.fuck)	# 找不到此属性 会调用__getattr__()