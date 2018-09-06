import numbers

class Field:
	pass

# 属性描述符
class IntField(Field):

	def __init__(self, db_column,min_value=None, max_value=None):
		self._value = None
		self.min_value = min_value
		self.max_value = max_value
		self.db_column = db_column
		# 检查
		if min_value is not None:
			if not isinstance(min_value, numbers.Integral):
				raise ValueError('min_value must be int')
			elif min_value < 0:
				raise ValueError('min_value must be positive int')

		if max_value is not None:
			if not isinstance(max_value, numbers.Integral):
				raise ValueError('min_value must be int')
			elif max_value < 0:
				raise ValueError('min_value must be positive int')

		if min_value is not None and max_value is not None:
			if min_value > max_value:
				raise ValueError('min_value must be smaller than max_value')

	def __get__(self, instance, owner):
		return self.value

	# 赋值时调用
	def __set__(self, instance, value):
		# 判断是否为int类型
		if not isinstance(value, numbers.Integral):
			raise ValueError('I need int!!!!!!!!!')
		if value < self.min_value or value > self.max_value:
			raise ValueError('value must be between min_value and max_value')
		# instance就是该类的实例本身 没错则把value保存起来
		self.value = value

class CharField(Field):
	def __init__(self, db_column, max_length=None):
		self.value = None
		self.db_column = db_column
		if max_length is None:
			raise ValueError('must have max_length')
		self.max_length = max_length

	def __get__(self, instance, owner):
		return self.value

	def  __set__(self, instance, value):
		if not isinstance(value, str):
			raise ValueError('String must be need')
		if len(value) > self.max_length:
			raise ValueError('len(value) must be smaller than max_length')
		self.value = value

class ModelMetaClass(type):
	# 参数不写 *args 则会被裁剪为 name bases attrs(类的属性)
	def __new__(cls, name, bases, attrs, **kwargs):
		if name == 'BaseModel':
			print('BaseModel __new__')
			# 即 在创建BaseModel类时 他没有要处理的内容(field) 所以直接用type创建
			return super().__new__(cls, name, bases, attrs, **kwargs)

		print('Else __new__')
		print('attrs: ', attrs)

		fields = {}	# 取出所有的Field
		for key, value in attrs.items():
			if isinstance(value, Field):
				fields[key] = value

		attrs_meta = attrs.get('Meta', None)	# 处理Meta属性类中的属性 先去出Meta类
		_meta = {}
		db_table = name.lower()	# 表名默认为name

		if attrs_meta is not None:
			table = getattr(attrs_meta, 'db_table', None)
			if table is not None:
				db_table = table

		# 给子类添加其他东西
		_meta['db_table'] = db_table
		attrs['_meta'] = _meta
		attrs['fields'] = fields    # 把整理好的fields放入attrs
		del attrs['Meta']

		return super().__new__(cls, name, bases, attrs, **kwargs)

class BaseModel(metaclass=ModelMetaClass):
	def __init__(self, *args, **kw):
		print('BaseModel __init__')
		for key, value in kw.items():
			setattr(self, key, value)
		return super().__init__()

	def save(self):
		fields = []
		values = []
		print('save: self.__dict__ -> ', self.__dict__)
		for key, value in self.fields.items():	# 通过self.fields能拿到之前整理好的fields(为什么??????????)
			db_column = value.db_column
			if db_column is None:
				db_column = key.lower()
			fields.append(db_column)	# 列名
			value = getattr(self, key)
			values.append(str(value))

		sql = "insert {db_table} ({fields}) value({values})".format(
			db_table=self._meta['db_table'], fields=','.join(fields), values=','.join(values))
		
# 把__init__放入BaseModel
class User(BaseModel):
	# 定义列
	name = CharField(db_column="name", max_length=10)
	age = IntField(db_column="age", min_value=0, max_value=100)

	# 定义其他的
	class Meta:
		db_table = "user"	# 表名

if __name__ == '__main__':
	user = User()
	user.name = 'booby'
	user.age = 28
	print(user.__dict__)
	user.save()	# 保存入数据库