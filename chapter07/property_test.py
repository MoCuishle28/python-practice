from datetime import date, datetime

class User(object):
	def __init__(self, name, birthday):
		self.name = name
		self.birthday = birthday
		self._age = 0

	def get_age(self):
		return datetime.now().year - self.birthday.year

	@property
	def age(self):
		return datetime.now().year - self.birthday.year		

	# 可通过此函数赋值
	@age.setter
	def age(self, value):
		self._age = value

if __name__ == '__main__':
	user = User('bobby', date(year=1997, month=5, day=30))
	print(user.get_age())
	print(user.age)
	user.age = 1000
	print(user.age, user._age)