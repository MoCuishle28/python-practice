class A(object):
	
	a = 10

	@classmethod
	def f1(cls, a):
		print(cls.a)
		print(a)
		print("=====================")
		cls.f2(100)


	@classmethod
	def f2(cls, b):
		print(cls.a)
		print(b)


if __name__ == '__main__':
	A.f1(21)