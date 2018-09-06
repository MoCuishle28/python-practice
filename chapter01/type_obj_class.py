a = 1
b = 'abc'
print(type(1))
print(type(int))
print(type(b))
print(type(str))
# type -> int -> 1 生成关系
# type -> class -> obj
# 类是由type生成的对象

class Student:
	pass

class MyStudent(Student):
	pass

stu = Student()
print(type(stu))
print(type(Student))
print('---')
mystu = MyStudent()
print(type(mystu))
print(type(MyStudent))

print('---')
print(int.__bases__)
print(type.__bases__)
print(object.__bases__)