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
	def update(cls, target_item, new_value, condition_item, condition_value, book_id):
		ret = True
		try:
			sql = 'update wish set {} = %s where {} = %s and book_id={};'.format(target_item, condition_item, book_id)
			print(sql)
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (new_value, condition_value, ))
			conn.commit()
		except Exception as e:
			print('Wish Update Error', e)
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
		sql = 'select user_id,nickname,launched,address from wish w,user u where w.book_id=%s and w.user_id=u.id and launched=%s;'
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
	def get_user_wish_by_username(cls,username):
		'''
		查询某位用户相关的心愿
		'''
		sql = 'select isbn,title,author,launched from wish,user u,book b where username=%s and user_id=u.id and b.id=book_id;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(username,))
		# 拿结果 直接拿不知道是什么? 是字典?
		# ret = cur.fetchall()
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret


	@classmethod
	def delete_by_ISBN(cls, isbn):
		try:
			sql = 'delete from wish where book_id=(select id from book where isbn=%s);'
			conn = pool.connection()
			cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)	# 设置返回字典
			cur.execute(sql,(isbn, ))
			conn.commit()
			ret = cur.fetchall()	# 得到一个元组 每个元素为一个字典
		except Exception as e:
			print('Error',e)
			conn.rollback()
		finally:
			cur.close()
			conn.close()
		return ret


	@classmethod
	def valid_wish_exists(cls, book_id, user_id):
		sql = 'select * from wish where book_id=%s and user_id=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(book_id, user_id ))
		ret = cur.fetchone()
		cur.close()
		conn.close()
		return ret