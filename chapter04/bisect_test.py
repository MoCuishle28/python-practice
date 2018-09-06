import bisect
"""处理已排序序列"""

# 二分查找
inter_list = []
bisect.insort(inter_list, 3)
bisect.insort(inter_list, 2)
bisect.insort(inter_list, 5)
bisect.insort(inter_list, 1)
bisect.insort(inter_list, 6)
# 以这种方式插入 维护一个增序的序列

print(inter_list)

print(bisect.bisect(inter_list, 3))	# 返回应该插入的位置
print(bisect.bisect_left(inter_list, 3))	# 返回应该插入的位置	若相等则插入到左边
print(bisect.bisect_left(inter_list, 4))	# 返回应该插入的位置

# 适用于任何序列类型
from collections import deque

inter_list = deque()
bisect.insort(inter_list, 3)
bisect.insort(inter_list, 2)
bisect.insort(inter_list, 5)
bisect.insort(inter_list, 1)
bisect.insort(inter_list, 6)

print('---')
print(inter_list)