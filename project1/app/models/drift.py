'''
表示完成一次用户之间的交易
'''


class Drift(object):
	'''
	id
	giver_id		赠予人
	recipient_id	接收人
	book_id
	message			备注
	status			交易状态(待寄出/已寄出/待签收/已签收)
	'''

	@classmethod
	def get_giver_drift(cls,user_id):
		'''
		查询某位用户赠予别人的礼物
		'''
		sql = 'select * from drift where giver_id=%s;'
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
		sql = 'select * from drift where recipient_id=%s;'
		conn = pool.connection()
		cur = conn.cursor()
		cur.execute(sql,(user_id,))
		# 这条怎么理解?  解包?
		ret = [ dict(zip([ k[0] for k in cur.description ], row))
				for row in cur.fetchall() ]		# 多条数据 用list
		cur.close()
		conn.close()
		return ret