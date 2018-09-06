class  Company:
	def __init__(self, employee_list):
		self.employee = employee_list

	def __len__(self):
		return len(self.employee)

com = Company(['a','b'])
print(hasattr(com, '__len__'))

from collections.abc import Sized
print(isinstance(com, Sized))

# 抽象基类
import abc

class CacheBase(metaclass=abc.ABCMeta):

	@abc.abstractmethod
	def get(self, key):
		pass

	@abc.abstractmethod
	def set(self, key, value):
		pass

class RedisCache(CacheBase):
	def set(self, key, value):
		pass