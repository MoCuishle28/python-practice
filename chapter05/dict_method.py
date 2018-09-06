a = {'a':{'b':1}, 'b':{'b':2}, 'c':{'b':3}}

# 浅拷贝
new_a = a.copy()
print(id(new_a) == id(a))
new_a['a']['b'] = 100	# a也跟着变 因为浅拷贝只是指向同一对象(如果value是数字 则不会改变 因为改变数字即指向一个新数字?)
print(new_a)
print(a)

# 深拷贝
import copy
new_a = copy.deepcopy(a)
new_a['a']['b'] = -1000
print('---')
print(new_a)
print(a)
print('---')

b = {'a':1, 'b':2, 'c':3}
new_b = b.copy()
new_b['b'] = -2
print(new_b, '----------', b)

# dict.fromkeys()
new_list = ['a', 'b']
new_dict = dict.fromkeys(new_list, {'k':'v'})	# 从new_list(只要是可迭代的)中提取key 以参数二为默认value
print(new_dict)

# get找不到key方法可以不抛异常
print(new_dict.get('c', {}))	# 若无key为'c' 则返回{}

# setdefault()
print('---setdefault---')
print( new_dict.setdefault('c', {'k_else':'v_else'}) )	# 若找不到 则将参数二设置进去
print( new_dict.setdefault('a', {'k_else':'v_else'}) )
print(new_dict)

# update()
new_dict.update({'d':1}) # 合并两个dict(或则说是可迭代的对象)
print(new_dict)

# 另一种update方式
new_dict.update(e=1, f=1)
print(new_dict)

# 以列表(可迭代对象)中带元组的方式传入key value
new_dict.update([('bobby', 'imooc')])
print(new_dict)

# new_dict.update([('aa','bb','cc')])	报错 元组内是 (key, value)
# print(new_dict)