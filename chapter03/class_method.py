class Date:
	def __init__(self, year, month, day):
		self.year = year
		self.month = month
		self.day = day

	def tomorrow(self):
		self.day += 1

	@staticmethod	# 一般无需返回实例对象则用静态方法
	def parse_ftom_string(date_str):	# 静态方法没有cls
		year, month, day = tuple(day_str.split('-'))
		return Date(int(year), int(month), int(day))

	@classmethod
	def from_string(cls, date_str):		# 类方法有cls(改成其他名字也可以 习惯上用cls)
		year, month, day = tuple(day_str.split('-'))
		return cls(int(year), int(month), int(day))

	def __str__(self):
		return "{year}/{month}/{day}".format(year=self.year, month=self.month, day=self.day)

if __name__ == '__main__':
	day = Date(2018, 12, 31)
	print(day)
	day.tomorrow()
	print(day)

	day_str = '2018-12-31'
	new_day = Date.parse_ftom_string(day_str)
	print(new_day)
	
	print('---')
	new_day = Date.from_string(day_str)
	print(new_day)