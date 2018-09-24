
from mongoengine import connect, Document, StringField, IntField, FloatField, \
	EmbeddedDocument, ListField, EmbeddedDocumentField

# connect('student')

SEX_CHOICES = (
	('male', '男'),
	('female', '女'),
)


class Grade(EmbeddedDocument):
	'''成绩'''
	name = StringField(required=True)
	score = FloatField(required=True)


class Student(Document):
	name = StringField(max_length=32, required=True)	# required=True 必须填写
	age = IntField(max_length=32, required=True)
	sex = StringField(choices=SEX_CHOICES, required=True)	# choices指定选择
	grade = FloatField()
	address = StringField()
	grades = ListField(EmbeddedDocumentField(Grade))	# 嵌套类型
	# remark = StringField()

	meta = {
		'collection':'student',		# 指定连接 student 集合
		'ordering':['-age']			# 返回数据时按照年龄从大到小排序
	}

class TestMongoEngine(object):

	def add_one(self):
		English = Grade(
			name='英语',
			score=550)		
		Math = Grade(
			name='数学',
			score=150)
		stu = Student(
			name='Rose',
			age=20,
			sex='female',
			grades=[English, Math]
			)
		# stu.remark = 'remark'
		stu.save()
		return stu


	def get_one(self):
		'''查询一条数据'''
		return Student.objects.first()


	def get_more(self):
		return Student.objects.all()


	def get_from_oid(self, oid):
		return Student.objects.filter(pk=oid)	# 根据id选


	def update(self):
		return Student.objects.filter(sex='male').update(dec__age=1)	# 修改 age 减一
		# 若只修改一条数据 Student.objects.filter(sex='male').update_one(dec__age=1)


	def delete(self):
		return Student.objects.filter(sex='male').first().delete()	# 删除一条男生数据 删除多条则不加first()


def main():
	connect('student')
	obj = TestMongoEngine()

	# ret = obj.add_one()
	# print(ret.pk)

	print(obj.get_one()['name'])
	print('---')
	ret = obj.get_more()
	for x in ret:
		print(x['name'], x['grades'][0].name, x['grades'][0].score, x['age'])

	print('---')
	print(obj.update())

	# print(obj.delete())	# 删除

if __name__ == '__main__':
	main()