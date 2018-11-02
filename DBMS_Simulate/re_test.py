import re
import json


while True:
	s = input('>')

	# create table t(id char(10) auto_increment, name varchar(12) notnull, primary_key(id))
	# create table a(id int(10) auto_increment, name varchar(12) notnull unique, primary_key(id))
	# .匹配除换行以外任何字符      + 一个或以上
	result = re.match(r'create table (?P<name>\w+)\((?P<permission>.+)\)$', s)
	
	if result:
		print(result.groupdict())
		print(result.group('permission').split(','))
		arr = result.group('permission').split(',')

		data = {}
		for x in arr:
			if 'primary_key' in x:
				key = re.findall(r'[(](.*?)[)]', x)
				data['primary_key'] = key[0]
				continue
			x = x.split()
			data[x[0]] = []
			for i,y in enumerate(x):
				if i == 0:
					continue
				data[x[0]].append(y)

		for k,v in data.items():
			print(k, v)
		with open('test.json', 'w') as f:	# 不能是a 一个json存一个字典
			json.dump(data, f)
	else:
		print(result)