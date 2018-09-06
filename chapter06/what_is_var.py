a = [1,2,3,4]
b = [1,2,3,4]
print(a is b, a == b)	# == 时是调用魔法函数__eq__

a = 1
b = 1
print(id(a) == id(b))	# 只对小整数会指向同一个空间的数字

a = 1.0
b = 1.0
print(id(a) == id(b), a == b, a is b)