# array(数组), deque
# array 只能存放指定的数据类型 性能高于list

import array

arr = array.array('i')	# 指定int类型

arr.append(1)
# arr.append('a')	会报错