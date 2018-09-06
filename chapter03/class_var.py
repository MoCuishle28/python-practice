class A:
	aa = 1 	# 类变量
	def __init__(self, x, y):
		self.x = x
		self.y = y

a = A(2, 3)
print(a.x, a.y, a.aa)
a.aa = 10
print(A.aa, a.aa)
A.aa = 0
a2 = A(100, 100)
print(a2.x, a2.y, a2.aa, a.aa, A.aa)
a2.aa = -10
print(a.aa, a2.aa, A.aa)

print('---')

class B:
	name = 'B'
	def __init__(self):
		self.name = 'obj'

b = B()
print(b.name, B.name)
print('---')

"""
python2.3 之后多继承下属性搜索算法：C3

"""
class D:
	pass
class C(D):
	pass
class B(D):
	pass
class A(B, C):
	pass

print(A.__mro__)