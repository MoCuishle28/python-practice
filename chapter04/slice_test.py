"""
切片模式 [start:end:step]

start:	默认为零
end:	默认为列表长度
step:	默认为1, 负数时表示反向切片
"""

a = [3, 4, 5, 6, 7, 9, 11, 13, 15, 17]
print(a[::], id(a) == id(a[::]))	# 返回包含原列表的所有元素的新列表

print('---')
print(a[::-1])	# 列表反转

print(a[::2])	# 步长为2 即取0和偶数位置的元素
print(a[1::2])	# 取基数位置

print('---')
print(a[0:1000])	# 结束位置超过长度 从尾部截断
print(a[1000:0])	# 起始位置大于列表 返回空值

print('---')
a[len(a):] = [9]	# 在列表尾部增加元素
print(a, id(a), id(a[len(a):]))

a[:0] = [1,2]	# 在头部插入元素
print(a)

print('---')
b = a[0:3]
print(b, id(b))
b[0] = 10
print(a, b, id(b))

print('---')
a[3:3] = [-4]	# 中间插入
print(a)

a = [1,2,3,4,5]
a[::2] = [0] * 3	# 各一个修改一个
print(a)

del a[::2]	# 隔一个删除
print(a)