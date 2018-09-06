# 500G文件读取 如何用生成器部分读取
# 若该文件只有一行 用{|}做分隔符 则不能用 file = open()    for line in file:... 的方式读(一行500G)
# 1.可以用f = open() 重复用f.read(4096)读取

def myreadline(f, newline):
	buf = ""	# 已经读出来的数据
	while True:
		while newline in buf:
			pos = buf.index(newline)	# 以{|}分割再返回
			yield buf[:pos]
			buf = buf[pos + len(newline):]

		chunk = f.read(4096*10)
		# print('func:',chunk)	# 可能把多个{|} 分割的部分都读入了
		if not chunk:
			yield buf
			break
		buf += chunk

with open("input.txt") as f:
	for line in myreadline(f, "{|}"):
		print(line)