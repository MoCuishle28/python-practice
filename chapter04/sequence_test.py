my_list = []
my_list.append(1)
my_list.append('a')
print(my_list)

from collections import abc

c = []
print('c:',id(c))
a = [1,2]
c = a + [3,4]
print(c,'c:',id(c))

print('a:',id(a))
a += (3,4)
print(a, 'a:',id(a))

print('---')
print('a:', id(a))
a.extend(range(3))
print(a,'a:', id(a))