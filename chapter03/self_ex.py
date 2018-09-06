"""
Python 的自省机制
"""

from class_method import Date

class Person:
	"""我是__doc__"""
	name = 'user'

class Student(Person):
	def __init__(self, school_name):
		self.school_name = school_name

if __name__ == '__main__':
	user = Student('慕课')
	print(user.__dict__)
	print(user.name)	# name属于Person类的属性
	print(Person.__dict__)