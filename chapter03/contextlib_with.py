import contextlib
# python 内置的上下文管理器装饰器

@contextlib.contextmanager
def file_open(file_name):
	print('file open')	# 模拟打开
	yield {'fuck':100}
	print('file end')	# 模拟关闭文件流

with file_open('f') as f:
	print(f)
	print('doing')