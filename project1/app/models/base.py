"""
开启连接池
"""

import MySQLdb
from DBUtils.PooledDB import PooledDB

 #5为连接池里的最少连接数
def create_connPool():
	global pool
	if not pool:
		pool = PooledDB(
				MySQLdb,
				5,
				host='127.0.0.1',
				user='test',
				passwd='123456',
				db='zonda',
				port=3306, 
				charset='utf8')
		print('创建连接池', pool)
	return pool

pool = None
pool = create_connPool()
print('执行了一次')