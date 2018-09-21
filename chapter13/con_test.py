import MySQLdb

try:
	conn = MySQLdb.connect(
			host='127.0.0.1',
			port=3306,
			user='root',
			passwd='zhang4409211',
			db='mydatabase',
			charset='utf8'
			)

	cursor = conn.cursor()	# 得到游标(中间人)
	cursor.execute('select `name`, `nickname` from `students`;')
	ret = cursor.fetchone()		# 查一条
	print(ret)

	conn.close()
except MySQLdb.Error as e:
	print('Error: %s' % e)