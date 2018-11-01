import re


while True:
	s = input('>')

	# create table t(id char(10) auto_increment, name varchar(12) not null, primary_key(id))
	# .匹配除换行以外任何字符      + 一个或以上
	result = re.match(r'create table (?P<name>\w+)\((?P<permission>.+)\)$', s)
	
	if result:
		print(result.groupdict())
		print(result.group('permission').split(','))
		arr = result.group('permission').split(',')
		for i,value in enumerate(arr):
			print(i, value)
	else:
		print(result)