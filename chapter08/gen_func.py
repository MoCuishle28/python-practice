
# 生成器函数 函数里只有yield
def gen_func():
	yield 1
	yield 2

def func():
	return 1

# 用生成器做斐波那契数列 不消耗内存
def fib(index):
	n, a, b = 0, 0, 1
	while n<index:
		yield b
		a,b = b, a+b
		n += 1

if __name__ == '__main__':
	gen = gen_func()	# 返回一个生成器对象	python编译字节码的时候就产生了
	f = func()
	print(type(gen), type(f))
	print(gen, f)
	print('---')

	for value in gen:	# 相当于调用next(gen)
		print(value)

	print('---')
	
	for data in fib(10):
		print(data, end=' ')
	print()