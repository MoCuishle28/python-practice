# python的垃圾回收是采用	引用计数器

a = 1
b = a	# 1的引用计数器加一

del a	# 1的引用计数器减一	a变量也没了
print(b)

a = object()
b = a
del a
print(b)
# print(a) 会报错

class A(object):
	# 当python解析器回收对象时会被调用
	def __del__(self):
		pass