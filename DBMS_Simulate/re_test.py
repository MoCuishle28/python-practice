import re
import json


while True:
	s = input('>')
	# select id,name from book,user by where uid in (select id from book where bid <= 10);
	# .匹配除换行以外任何字符      + 一个或以上
	result = re.match(r'\s*select\s*(?P<items>.+)\s*from\s*(?P<table_list>.+)\s*by where\s*(?P<judge>.*)\s*$', s)
	
	if result:
		for k,v in result.groupdict().items():
			print(k, ': ', v)
	else:
		print('None')