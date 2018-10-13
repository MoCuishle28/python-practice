from .base import pool



class User(object):
	'''
	id int(10) primary key
	username unique
	password
	nickname unique
	address
	phone
	email
	'''

	@classmethod
	def valid_user(cls, username):
		sql = 'select username,password from user where username=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(username,))
		# 拿结果 直接拿不知道是什么? 是字典?
		# ret = cur.fetchall()
		# 这条怎么理解?  解包?
		ret = cur.fetchone()
		cur.close()
		conn.close()
		return ret