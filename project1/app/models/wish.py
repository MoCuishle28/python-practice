from .base import pool
import MySQLdb



class Wish():
	'''
	表示某位用户想要某本书
	id auto_increment primary key int(10)
	book_id
	user_id
	launched	是否已经满足
	'''

	@classmethod
	def get_wish(cls,book_id):
		'''
		查询某本书相关的心愿
		'''
		sql = 'select * from wish where book_id=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(book_id,))
		# 拿结果 直接拿不知道是什么? 是字典?
		# ret = cur.fetchall()
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret


	@classmethod
	def get_user_wish(cls,user_id):
		'''
		查询某位用户相关的心愿
		'''
		sql = 'select * from wish where user_id=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(user_id,))
		# 拿结果 直接拿不知道是什么? 是字典?
		# ret = cur.fetchall()
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret