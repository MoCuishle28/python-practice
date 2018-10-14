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


	def __init__(self, book_id, user_id, launched):
		self.book_id = book_id
		self.user_id = user_id
		self.launched = launched


	def insert(self):
		ret = True
		try:
			sql = 'insert into wish (`book_id`, `user_id`, `launched`) values(%s, %s, %s)'
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (self.book_id, self.user_id, self.launched))
			conn.commit()
		except Exception as e:
			print('Wish Insert Error', e)
			ret = False
			conn.rollback()	# 一条sql失败 则全部都不会提交
		finally:
			cur.close()
			conn.close()
		return ret


	@classmethod
	def get_wishInfo(cls,book_id):
		'''
		查询某本书相关的心愿
		'''
		sql = 'select user_id,nickname,launched from wish w,user u where w.book_id=%s and w.user_id=u.id and launched=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(book_id,'0', ))
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