from .base import pool
import MySQLdb


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

	def __init__(self, username, password, nickname, address, phone, email, _id):
		self.username = username
		self.password = password
		self.nickname = nickname
		self.address = address
		self.phone = phone
		self.email = email
		self.id = int(_id)


	def insert(self):
		ret = True
		try:
			sql = 'insert into user (`username`,`password`,`nickname`,`address`,`phone`,`email`) values(%s,%s,%s,%s,%s,%s)'
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (self.username,self.password,self.nickname,self.address,self.phone,self.email))
			conn.commit()
		except Exception as e:
			print('User Insert Error', e)
			ret = False
			conn.rollback()	# 一条sql失败 则全部都不会提交
		finally:
			cur.close()
			conn.close()
		return ret


	def update(self):
		ret = True
		try:
			sql = 'update user set username=%s,password=%s,nickname=%s,address=%s,phone=%s,email=%s where id=%s;'
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (self.username,self.password,self.nickname,self.address,self.phone,self.email, self.id))
			conn.commit()
		except Exception as e:
			print('User update Error', e)
			ret = False
			conn.rollback()	# 一条sql失败 则全部都不会提交
		finally:
			cur.close()
			conn.close()
		return ret


	@classmethod
	def valid_nickname(cls, nickname):
		sql = 'select id from user where nickname=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(nickname,))
		# 拿结果 直接拿不知道是什么? 是字典?
		# ret = cur.fetchall()
		# 这条怎么理解?  解包?
		ret = cur.fetchone()
		cur.close()
		conn.close()
		return ret


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


	@classmethod
	def find_oneID_by_username(cls, username):
		sql = 'select id from user where username=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql, (username,))
		ret = cur.fetchone()	# 得到的是元祖
		cur.close()
		conn.close()
		# 返回的是元组
		return ret


	@classmethod
	def find_user_by_username(cls, username):
		sql = 'select * from user where username=%s;'
		conn = pool.connection()
		cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)	# 设置返回字典
		cur.execute(sql, (username,))
		ret = cur.fetchall()	# 得到一个元组 每个元素为一个字典
		cur.close()
		conn.close()
		return ret



	@classmethod
	def find_user_by_ID(cls, _id):
		sql = 'select * from user where id=%s;'
		conn = pool.connection()
		cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)	# 设置返回字典
		cur.execute(sql, (_id,))
		ret = cur.fetchall()	# 得到一个元组 每个元素为一个字典
		cur.close()
		conn.close()
		return ret