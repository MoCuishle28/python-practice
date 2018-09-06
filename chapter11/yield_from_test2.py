"""
main 调用方  g1 委托生成器	gen 子生成器

yield from 会在调用方和子生成器之间建立一个双向通道
"""

def gen_func():
	a = yield from 1
	return 'END'

# gen是子生成器
def g1(gen):
	yield from gen

def main():
	gen = gen_func()
	g = g1(gen)
	g.send(None)	# 会发送给子生成器 gen


# 分析子生成器
def sales_sum(pro_name):
	total = 0
	nums = []
	while True:
		x = yield		# 这个yield 只用于传入值 不产出值
		print(pro_name+'销量: ', x)
		if not x:	# None时会break
			break
		total += x
		nums.append(x)
	return total, nums	# return时会抛出异常 StopIteration

if __name__ == '__main__':
	gen = sales_sum('手机')
	gen.send(None)
	gen.send(1200)
	gen.send(1500)
	gen.send(3000)

	try:
		gen.send(None)
	except StopIteration as e:	# 若用yield from 可以自己处理这个异常
		pass
