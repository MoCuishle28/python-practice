"""经典错误"""

def add(a, b):
	a += b
	print('id(a)',id(a))
	return a

class Company:
	# 当不传入参数2时 多个创建对象会公用一个默认列表对象
	def __init__(self, name, staffs=[]):
		self.name = name
		self.staffs = staffs

	def add(self, staff_name):
		self.staffs.append(staff_name)

	def remove(self, staff_name):
		self.staffs.remove(staff_name)

if __name__ == '__main__':
	a = 1
	b = 2
	c = add(a, b)
	print('id(a)',id(a))
	print(c, a, b,end='\n\n')

	a = [1, 2]
	b = [3, 4]
	c = add(a, b)	# 传入参数a, b 是可变对象 传入的a b 是引用 a对象被 += 修改了
	print('id(a)',id(a))
	print(c, a, b,end='\n\n')

	a = (1, 2)
	b = (3, 4)
	c = add(a, b)	# 传入的元组对象是副本
	print('id(a)',id(a))
	print(c, a, b,end='\n\n')

	com1 = Company('com1',['a', 'b'])
	com1.add('c')
	com1.remove('a')
	print(com1.staffs)

	com2 = Company('com2')
	com2.add('a')
	print(com2.name, com2.staffs)

	com3 = Company('com3')
	com3.add('a5')

	print(com2.name, com2.staffs)
	print(com3.name, com3.staffs)
	print(id(com2.staffs) == id(com3.staffs))

	print('---')
	print(Company.__init__.__defaults__)