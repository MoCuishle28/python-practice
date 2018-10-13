import redis


r = redis.StrictRedis(host='localhost', port=6379, db=0)

r.set('test', 123)
test = r.get('test')
print(test)

user1 = r.get('user1')
print(user1)
print('---')


class Base(object):
	def __init__(self):
		self.r = redis.StrictRedis(host='localhost', port=6379, db=0)		


class TestString(Base):
	def set(self):
		return self.r.set('user2', 'Amy')
		

	def get(self):
		return self.r.get('user2')


	def mset(self):
		d = {'user3':'bob', 'user4':'Alex'}
		return self.r.mset(d)


	def mget(self):
		keys = ['user3', 'user4']
		return self.r.mget(keys)


	def delete(self):
		return self.r.delete('user4')


class TestList(Base):
	# def __init__(self):
	# 	self.r = redis.Redis(host='localhost', port=6379, db=0)		# 兼容老版本的连接写法


	def lpush(self):
		list_eat = ['Amy', 'Jhon']
		# rpush 同理
		return self.r.lpush('list_eat', *list_eat)		# 需要用 * 解开 否则redis-list的第一个元素为整个list


	def lrange(self):
		return self.r.lrange('list_eat', 0, -1)


	def lpop(self):
		return self.r.lpop('list_eat')


class TestSet(Base):
	def sadd(self):
		l_set = ['Monkey', 'Human']
		return self.r.sadd('zoo', *l_set)


	def smembers(self):
		return self.r.smembers('zoo')


	def srem(self):		# 删除元素
		return self.r.srem('zoo', 'Dog')


	def sinter(self):	# 交集
		return self.r.sinter('zoo', 'zoo1')

def main():
	# 测试 String
	# str_obj = TestString()	
	# print(str_obj.set())
	# print(str_obj.get())
	# print(str_obj.mset())
	# print(str_obj.mget())
	# print(str_obj.delete())


	list_obj = TestList()
	# print(list_obj.lpush())
	print(list_obj.lrange())
	# print(list_obj.lpop())

	set_obj = TestSet()
	print(set_obj.sadd())
	print(set_obj.smembers())
	print(set_obj.srem())
	print(set_obj.sinter())

if __name__ == '__main__':
	main()