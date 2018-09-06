
def gen_func():
	yield 1
	name = 'bob'
	yield 2
	age = 30
	return 'imooc'

import dis
gen = gen_func()
# print(dis.dis(gen))
print(gen.gi_frame.f_lasti)	# 执行到的位置(字节码中的行数) 未开始执行则是-1
print(gen.gi_frame.f_locals)

print('---')
print('next:', next(gen))
print('---')
print()

print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)

print('---')
print('next:', next(gen))
print('---')
print()

print(gen.gi_frame.f_lasti)
print(gen.gi_frame.f_locals)	#第二次调用后 有了name变量


from collections import UserList	# 用python实现的list 可以用来继承

