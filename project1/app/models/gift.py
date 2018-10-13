from .base import pool
import MySQLdb



class Gift():
	'''
	表示某位用户想赠送某本书
	id auto_increment primary key int(10)
	book_id
	user_id
	launched	是否已经完成赠送
	'''

	@classmethod
	def get_gift(cls,book_id):
		'''
		查询某本书相关的礼物
		'''
		sql = 'select * from gift where book_id=%s;'
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
	def get_user_gift(cls,user_id):
		'''
		查询某用户相关的礼物
		'''
		sql = 'select * from gitf where user_id=%s;'
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