"""
使用委托生成器 和子生成器的目的？
"""


final_result = {}

# 子生成器
def sales_sum(pro_name):
	total = 0
	nums = []
	while True:
		x = yield		# 这个yield 只用于传入值 不产出值
		print(pro_name+'销量: ', x)
		if not x:
			break
		total += x
		nums.append(x)
	return total, nums	# return会抛出一个异常

# 委托生成器
def middle(key):
	while True:
		# final_result[key] 会接收到sales_sum() return 的值
		final_result[key] = yield from sales_sum(key)
		print(key + '销量统计完成...')

# 调用方
def main():
	data_sets = {
		'面膜':[1200, 1500, 3000],
		'手机':[28, 55, 98, 108],
		'大衣':[280, 560, 778, 70]
	}
	for key, data_set in data_sets.items():
		print('start key:', key)
		m = middle(key)
		m.send(None)	# 预激活middle协程 会执行到子生成器的第一个yield那里停止 等待下一次send
		for value in data_set:
			m.send(value)	# 给协程传递每一组值
		m.send(None)
		print('final_result:', final_result)

if __name__ == '__main__':
	main()