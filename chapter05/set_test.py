# set集合 frozenset(冻集)不可变集合
# 可hash的对象可作为key 如：str frozenset tuple 自己实现的类中实现了__hash__返回一个不可变的值

s = set('abcdee')
print(s)

s = frozenset('abcde')	# 一旦设置好则无法修改(适合作为dict的key)
print(s)

s = {'a', 'b', 'c', 'd'}
another_set = set('efg')
s.update(another_set)
print(s)
print(s.pop())

# 找不同 difference
s = {'a','b','c','d'}
another_set = set('cdef')
res_set = s.difference(another_set)	# s中不同于another_set的 (即差集 s - another_set)
print('---')
print('s - another_set = ',res_set)
print('s:',s)
print('another_set:',another_set)

# 集合运算
re_set = []
re_set.append(s - another_set)
re_set.append(s & another_set) 	# 交集
re_set.append(s | another_set)	# 并集
print('集合运算 - & |')
for re_item in re_set:
	print(re_item)

# 是否为子集
print(s.issubset(re_set[-1]))