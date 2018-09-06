# 列表生成式 (列表推导式)
# 性能高于列表操作

# 提取出1-20的奇数
odd_list = []
for i in range(21):
	if i%2 == 1:
		odd_list.append(i)
print(odd_list, type(odd_list))

# 以上可以用一行代码实现
odd_list = [i for i in range(21) if i % 2 == 1]
print(odd_list, type(odd_list))

# 逻辑复杂的情况
def handle_item(item):
	return item*item

odd_list = [handle_item(i) for i in range(21) if i % 2 == 1]
print(odd_list)

# 生成器表达式
odd_gen = (i for i in range(21) if i % 2 == 1)
print(odd_gen, '----------',type(odd_gen))
# 通过循环迭代操作
for i in odd_gen:
	print(i)

# 字典推导式
my_dict = {'a':22, 'b':20, 'c':3}
# 需求: 反转键和值
reversed_dict = {v:k for k, v in my_dict.items()}
print(my_dict, type(my_dict))
print(reversed_dict, type(reversed_dict))

# 集合推导式
my_set = {key for key, value in my_dict.items()}
print(my_set, type(my_set))