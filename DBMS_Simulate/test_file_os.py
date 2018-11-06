import linecache

the_line = linecache.getline('test.db', 3)
print (the_line)

# linecache读取并缓存文件中所有的文本
# 若文件很大，而只读一行，则效率低下
# 可显示使用循环, 注意enumerate从0开始计数，而line_number从1开始
def getline(the_file_path, line_number):
	if line_number < 1:
		return ''
	for cur_line_number, line in enumerate(open(the_file_path, 'r')):
		if cur_line_number == line_number-1:
			return line
	return ''

the_line = linecache.getline('test.db', 4)
print (the_line)

print(getline('test.db', 3))


# os.mkdir('testFile') # 创建文件目录

data = [1, 'a']
with open('test1.db', 'a') as f:
	f.write(str(data)+';'+'\n')


with open('test1.db', 'r') as f:
	data = f.read().replace('\n', '')
	print(data)
	data = data.split(';')


print('=====================')
for x in data:
	print(x)

class A(object):
	
	@classmethod
	def f(cls, a):
		print(a)

	@classmethod
	def f(cls, a, b):
		print(a, b)


A.f(1)
A.f(100, 200)