import MySQLdb
from .base import pool


class Book(object):
	'''
	id = Column(Integer, primary_key=True, autoincrement=True)
	title = Column(String(50), nullable=False)	# 最大长度50
	author = Column(String(30), default='未名')
	publisher = Column(String(50))
	isbn = Column(String(15), nullable=False, unique=True)
	summary = Column(String(1000))
	image = Column(String(50))

	封装一些书籍信息的SQL操作
	'''

	@classmethod
	def find_all(cls, **key_value):
		sql = 'select * from book;'
		if key_value:
			sql = sql[:-1]
			sql += ' where '
			cnt = 0
			for k,v in key_value.items():
				if cnt != 0:
					sql += ' and '
				sql = sql + k + '=\'' + v + '\''
				cnt += 1
			sql += ';'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql)
		# 拿结果 直接拿不知道是什么? 是字典?
		# ret = cur.fetchall()
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret