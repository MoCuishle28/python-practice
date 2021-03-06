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

	def __init__(self, book_id, user_id, launched):
		self.book_id = book_id
		self.user_id = user_id
		self.launched = launched


	def insert(self):
		ret = True
		try:
			sql = 'insert into gift (`book_id`, `user_id`, `launched`) values(%s, %s, %s)'
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (self.book_id, self.user_id, self.launched))
			conn.commit()
		except:
			print('Error')
			ret = False
			conn.rollback()	# 一条sql失败 则全部都不会提交
		finally:
			cur.close()
			conn.close()
		return ret


	@classmethod
	def update(cls, u_id, item, new_value, book_id):
		ret = True
		try:
			sql = 'update gift set {} = %s where user_id=%s and book_id={};'.format(item, book_id)
			print(sql)
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (new_value, u_id, ))
			conn.commit()
		except Exception as e:
			print('Gift Update Error', e)
			ret = False
			conn.rollback()	# 一条sql失败 则全部都不会提交
		finally:
			cur.close()
			conn.close()
		return ret


	@classmethod
	def get_giftInfo(cls,book_id):
		'''
		查询某本书相关的礼物
		'''
		sql = 'select user_id,nickname,launched from user u,gift g where g.book_id=%s and g.user_id=u.id and launched=%s;'
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
		return ret 	# 返回列表 每个元素为一个字典


	@classmethod
	def get_user_gift_by_username(cls,username):
		'''
		查询某用户相关的礼物
		'''
		sql = 'select isbn,title,author,launched from gift,user u,book b where username=%s and user_id=u.id and b.id=book_id;'
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
			sql = 'delete from gift where book_id=(select id from book where isbn=%s);'
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
	def valid_gift_exists(cls, book_id, user_id):
		sql = 'select * from gift where book_id=%s and user_id=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(book_id, user_id ))
		ret = cur.fetchone()
		cur.close()
		conn.close()
		return ret