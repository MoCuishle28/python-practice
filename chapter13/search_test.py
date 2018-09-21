import MySQLdb

class MysqlSearch(object):

	def __init__(self):
		self.get_conn()


	def get_conn(self):
		try:
			self.conn = MySQLdb.connect(
				host='127.0.0.1',
				port=3306,
				user='test',
				passwd='123456',
				db='mydatabase',
				charset='utf8'
			)
		except MySQLdb.Error as e:
			print('Error: %s' % e)


	def get_one(self):
		# 1.准备SQL	
		sql = 'select * from `news` where `types` = %s order by `created_at` desc;'
		# 2.找到cursor
		cursor = self.conn.cursor()
		# 3.执行SQL
		cursor.execute(sql, ('民生',))
		# 4.拿到结果
		# ret = cursor.fetchone()
		ret = dict(	zip([ k[0] for k in cursor.description ], cursor.fetchone()) )	# 拿到一个字典
		# 5.处理数据

		# 6.关闭连接
		return ret


	def get_more(self, page, page_size):
		"""
		page: 		第几页
		page_size: 	页面大小
		"""
		offset = (page - 1) * page_size
		sql = 'select * from `news` order by `created_at` desc limit %s, %s;'
		cursor = self.conn.cursor()
		cursor.execute(sql, (offset, page_size, ))
		ret = [ dict(zip([ k[0] for k in cursor.description ], row))
				for row in cursor.fetchall() ]		# 多条数据 用list
		return ret


	def add_one(self):
		try:
			sql = """insert into `news` (`title`, `image`, `content`, `types`, `is_valid`)
					 value (%s, %s, %s, %s, %s);"""
			cursor = self.conn.cursor()
			cursor.execute(sql, ('全国人民喜迎油价上涨', '..', '好贵啊好贵啊好贵啊', '推荐', 1, ))
			self.conn.commit()
		except :
			print('Error')
			self.conn.rollback()	# 一条sql失败 则全部都不会提交

	def close_conn(self):
		try:
			self.conn.close()
		except MySQLdb.Error as e:
			print('Error: %s' % e)


def main():
	obj = MysqlSearch()
	ret = obj.get_one()
	print(ret)
	print('Content', ret['content'])

	ret = obj.get_more(1, 2)	# 第1页 页面大小2
	print('------')
	for row in ret:
		print(row)

	obj.add_one()
	obj.close_conn()

if __name__ == '__main__':
	main()