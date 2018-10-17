'''
表示完成一次用户之间的交易
'''
from .base import pool
import MySQLdb



class Drift(object):
	'''
	id
	giver_id		赠予人
	recipient_id	接收人
	book_id
	message			备注
	status			交易状态(待寄出/已寄出/待签收/已签收  待处理/已拒绝)
	'''


	def __init__(self, giver_id, recipient_id, book_id, message, status):
		self.giver_id = giver_id
		self.recipient_id = recipient_id
		self.book_id = book_id
		self.message = message
		self.status = status


	def insert(self):
		ret = True
		try:
			sql = 'insert into drift (`giver_id`, `recipient_id`, `message`, `status`, `book_id`) values(%s, %s, %s, %s, %s);'
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (self.giver_id, self.recipient_id, self.message, self.status, self.book_id))
			conn.commit()
		except Exception as e:
			print('Drift Insert Error', e)
			ret = False
			conn.rollback()	# 一条sql失败 则全部都不会提交
		finally:
			cur.close()
			conn.close()
		return ret


	# @classmethod
	# def update(cls, target_item, new_value, condition_item, condition_value, book_id):
	# 	ret = True
	# 	try:
	# 		sql = 'update gift set {} = %s where {} = %s and book_id={};'.format(target_item, condition_item, book_id)
	# 		print(sql)
	# 		conn = pool.connection()
	# 		cur = conn.cursor()
	# 		cur.execute(sql, (new_value, condition_value, ))
	# 		conn.commit()
	# 	except Exception as e:
	# 		print('Gift Update Error', e)
	# 		ret = False
	# 		conn.rollback()	# 一条sql失败 则全部都不会提交
	# 	finally:
	# 		cur.close()
	# 		conn.close()
	# 	return ret


	@classmethod
	def update(cls, drift_id, item, new_value):
		ret = True
		try:
			sql = 'update drift set {} = %s where id=%s;'.format(item)
			print(sql)
			conn = pool.connection()
			cur = conn.cursor()
			cur.execute(sql, (new_value, drift_id, ))
			conn.commit()
		except Exception as e:
			print('Drift Update Error', e)
			ret = False
			conn.rollback()	# 一条sql失败 则全部都不会提交
		finally:
			cur.close()
			conn.close()
		return ret


	@classmethod
	def find_drift_by_ID(cls, d_id):
		sql = 'select * from drift where id=%s;'
		conn = pool.connection()
		cur = conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
		cur.execute(sql,(d_id, ))
		ret = cur.fetchone()
		cur.close()
		conn.close()
		return ret


	@classmethod
	def valid_drift(cls, gid, rid, bid):
		sql = 'select * from drift where giver_id=%s and recipient_id=%s and book_id=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(gid, rid, bid,))
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret


	@classmethod
	def get_giver_drift(cls,user_id):
		'''
		查询某位用户赠予别人的礼物
		'''
		sql = 'select d.id,b.id as book_id,title,u.nickname,status from drift d,user u,book b where giver_id=%s and u.id=recipient_id and b.id=book_id;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(user_id,))
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret


	@classmethod
	def get_recipient_id_drift(cls,user_id):
		'''
		查询某位用户接收别人的礼物
		'''
		sql = 'select d.id,b.id as book_id,title,nickname,status from drift d,user u,book b where recipient_id=%s and u.id=giver_id and b.id=book_id;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(user_id,))
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret