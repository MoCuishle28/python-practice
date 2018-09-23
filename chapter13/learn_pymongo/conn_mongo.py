from pymongo import MongoClient
# client.close()	# 不需要关闭 pymongo内置有连接池自动管理连接

from datetime import datetime
from bson.objectid import ObjectId


class TestMongo(object):

	def __init__(self):
		self.client = MongoClient()
		self.db = self.client['learn']


	def add_one(self):
		post = {
			'title':'铁锤的一百五十八中锤法',
			'content':'嘣嘣嘣...',
			'x':1,
			'created': datetime.now()
		}
		return self.db.blog.posts.insert_one(post)


	def get_one(self):	# 获取一条数据
		return self.db.blog.posts.find_one()	# 反回的是dict类型


	def get_more(self):
		return self.db.blog.posts.find({'title':'标题1'})		# 获取多条数据 里面也可以加查询条件(条件用字典格式 {} )


	def get_one_from_oid(self, oid):	# 获取某个id的数据
		obj = ObjectId(oid)		# 必须通过bson模块下的ObjectId处理 不然查询不到
		return self.db.blog.posts.find_one({'_id':obj})

	def update(self):
		'''修改数据'''
		ret = self.db.blog.posts.update_one({'x':1}, {'$inc':{'x':5}})	# 改变一条数据 对查找到的第一条x=1的数据 x增加5
		return ret


	def update_many(self):
		return self.db.blog.posts.update_many({'x':6}, {'$inc':{'x':2}})	# 改变多条数据


	def delete(self):
		# 删除一条数据
		return self.db.blog.posts.delete_one({'x':1})	# 删除查询到的第一天x为1的数据


	def delete_many(self):
		# 删除多条数据
		return self.db.blog.posts.delete_many({'x':8})	# 删除查询到的第一天x为1的数据


def main():
	obj = TestMongo()
	# print(obj.add_one())
	print('------')
	# print(obj.db.blog.posts.count())	# 查看有多少条数据

	# print(obj.get_one())

	d = obj.get_more()
	for item in d:
		print(item.get('title'), item.get('content'))


	print('------')
	print(obj.get_one_from_oid('5ba5f4601223561a94f636fb'))		# 按照 _id 查
	print('------')

	# ret = obj.update()	# 改变一条数据
	# print(ret.matched_count, ret.modified_count)

	# ret = obj.update_many()	# 改变多条数据
	# print(ret.matched_count, ret.modified_count)

	# ret = obj.delete()	# 删除一条数据
	# print('deleted_count:', ret.deleted_count)

	ret = obj.delete_many()
	print('deleted_count:', ret.deleted_count)

if __name__ == '__main__':
	main()