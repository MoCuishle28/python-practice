class  Company:
	def __init__(self, employee_list):
		self.employee = employee_list

	def __getitem__(self, item):
		return self.employee[item]

	def __len__(self):
		return len(self.employee)

	def __repr__(self):	# 交互环境下打印
		return ','.join(self.employee)

	def __str__(self):	# print时调用
		return ','.join(self.employee)

class ExtCompany(Company):
	def __init__(self, l):
		self.l = l

# 魔法函数不会被继承
# e = ExtCompany(['a','b','c'])
# print(e)

c = Company(['tom','bob','jane'])
# employee = c.employee
# for em in employee:
# 	print(em)

tmp = c[:2]
print(c)
print(len(c))

# getitem的作用
for em in tmp:
	print(em)

# 有getitem()就可迭代 应该是...
a = [1,2,3]
a.extend(c)
print(a)