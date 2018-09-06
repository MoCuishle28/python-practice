class A:
	pass

class B(A):
	pass

b = B()

print(isinstance(b, B))
print(isinstance(b, A))

# is 不能和 == 混用
# is 是是否指向同一对象  == 是值是否相等
print(type(b) is B)
print(type(b) == B)