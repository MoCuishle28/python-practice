'''
数据库定义语言
如：create, alter, drop
'''
import os
import re
import json
from config import db_path, dict_path


def load_database():
	with open(dict_path+'\\database.dict', 'r') as f:
		database = f.read()
	return set(database.split())	# 现有的数据库


class SQL_Func(object):

	database_set = load_database()	# 所有数据库集合
	curr_database = ''				# 当前使用的数据库
	tables_set = set()				# 当前数据库的表
	# 保留字集合
	key_word = {'auto_increment', 'notnull', 'primary_key', 'foreign_key', 'unique', 'char', 'int'}

	@classmethod
	def use(cls, command_str):
		result = re.match(r'use (?P<name>\w+)$', command_str)
		if 	not result:
			return False
		name = result.group('name')

		if name in cls.database_set:
			cls.curr_database = name
			with open(db_path + '\\' + name + '\\tables.dict', 'r') as f:
				tables = f.read()
				cls.tables_set = set(tables.split())	# 更新数据表集合
		else:
			print(name, '数据库不存在')
			return False
		return True


	@classmethod
	def show(cls, command_str):
		if cls.curr_database == '':
			result = re.match(r'show databases$', command_str)
			if not result:
				return False
			print('----------')
			print('Databases:')
			print('----------')
			if not cls.database_set:
				print('(NULL)')
			for item in cls.database_set:				
				print(item)
		else:
			result = re.match(r'show tables$', command_str)
			if not result:
				return False
			print('----------')
			print('Tables:')
			print('----------')
			if not cls.tables_set:
				print('(NULL)')
			for item in cls.tables_set:
				print(item)
		print('----------')
		return True


	@classmethod
	def create(cls, command_str):
		if cls.curr_database == '':	# 当前未使用数据库 则创建的是数据库
			result = re.match(r'create (?P<name>\w+)$', command_str)
			if not result:
				return False
			name = result.group('name')

			if name in cls.database_set:
				print(name, '已存在')
				return False
			else:	# 创建数据库
				with open(dict_path+'\\'+'database.dict', 'a') as f:
					f.write('\n'+name)							# 写入数据库数据字典
				cls.database_set = load_database()				# 更新数据库集合

				os.mkdir(db_path + '\\' + name)		# 创建对应文件夹
				with open(db_path + '\\' + name + '\\tables.dict', 'w') as f:
					f.write('')
		else:	# 已使用数据库 则创建数据表
			return cls.createTable(command_str)
		return True


	# 创建Table 添加各种约束
	@classmethod 
	def createTable(cls, command_str):
		is_not_key_word = lambda x: x not in cls.key_word and 'char' not in x and 'int' not in x
		is_key_word = lambda x: x in cls.key_word or 'char' in x or 'int' in x
		# create table t(id int(11) notnull auto_increment, name char(20) notnull, primary_key(id));
		result = re.match(r'create table (?P<name>\w+)\((?P<permission>.+)\)$', command_str)
		if not result:
			return False

		name = result.group('name')
		if name in cls.tables_set:
			print(name, '已存在')
			return False

		tmp_arr = result.group('permission').split(',')
		permission = []
		for x in tmp_arr:
			permission.append(x.split())
		table_dict = {}		# 创建表的数据字典

		for x in permission:
			if 'primary_key' in x[0]:
				key_list = re.findall(r'[(](.*?)[)]', x[0])
				key_list = key_list[0].split('/') if key_list else []
				table_dict['primary_key'] = key_list;	# 主键可能有多个
				continue

			field_name = filter(is_not_key_word, x)	# 得到一个符合 is_not_key_word 要求的迭代器
			tar_name = ''
			for field in field_name:
				table_dict[field] = []
				tar_name = field
				break
			field_name = tar_name
			for value in x:
				if value != field_name and is_key_word(value):	# 不是表名并且是关键字
					table_dict[field_name].append(value)
				elif value != field_name and not is_key_word(value):
					print(value+' 不是关键字')
					return False
					
		cls.add_to_database_dict(name)	# 把表名写入对应数据库的数据字典
		with open(db_path + '\\' + cls.curr_database + '\\'+name+'.json', 'w') as f:
			json.dump(table_dict, f)
		with open(db_path + '\\' + cls.curr_database + '\\'+name+'.txt', 'w') as f:
			f.write('')
		return True


	@classmethod
	def insert(cls, command_str):
		# insert into t('id','name') values(1, 'a');
		result = re.match(r'insert into (?P<table_name>\w+)(?P<target_items>.*) values\((?P<values_list>.+)\)$', command_str)
		if not result or not cls.curr_database:
			print('sql error')
			return False
		
		table_name = result.group('table_name')
		# 值列表
		values_list = result.group('values_list').split(',')
		# 指定字段列表 可能为空
		target_items = re.findall(r'[(](.*?)[)]', result.group('target_items'))
		target_items = [ item.replace('\'','') for item in (target_items.pop().split(',') if target_items else []) ]

		table_dict = {}
		if table_name not in cls.tables_set:
			print(table_name+' 该表不存在')
			return False
		with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.json', 'r') as f:
			table_dict = json.load(f)

		# 检验合法性
		
		if target_items:	# 带指定插入内容
			if not cls.valid_items_exist(target_items, table_dict):
				return False
			# 是否全部待插入数据约束判定都成立
			if cls.valid_items_limit(values_list, target_items ,table_dict, table_name):
				# 如果约束成立 则将数据插入
				print('Insert')
				pass
			else:
				return False
		else:	# 不带的指定字段的插入
			# TODO


	@classmethod
	def cls(cls, command_str):
		if not re.match(r'cls$', command_str):
			return False
		os.system('cls')
		return True


	@classmethod
	def exit(cls, command_str):
		if not re.match(r'exit$', command_str):
			return False
		print('bye!')
		exit()
		return True


	# 添加数据库名字到对应数据库的数据字典中
	@classmethod
	def add_to_database_dict(cls, table_name):
		with open(db_path+'\\'+cls.curr_database+'\\'+'tables.dict', 'a') as f:
			f.write('\n'+table_name)
		cls.tables_set.add(table_name)


	# 检验属性是否存在
	@classmethod
	def valid_items_exist(cls, target_items, table_dict):
		for item in target_items:
			if item not in table_dict.keys():
				print(item+" 不存在")
				return False
		return True


	# 根据数据字典判定插入数据的约束是否成立
	@classmethod
	def valid_items_limit(cls, values_list, target_items, table_dict, table_name):
		'''
		value_list:		插入数据列表
		target_items:	字段列表
		table_dict:		数据字典
		'''
		if len(values_list) != len(target_items):
			print('插入数据数量与字段数不匹配')
			return False
		is_item_size = lambda x: 'char' in x or 'int' in x		# 判断是否是长度约束
		for index,value in enumerate(values_list):
			item_size = 5
			tar_item = ''	# 数据类型
			for item in table_dict.get(target_items[index], []):
				if is_item_size(item):
					item_size = int(re.findall(r'[(](.*?)[)]', item).pop())
					tar_item = item.split('(')[0]
					break
			limit_size = item_size 	# 数据长度约束
			if tar_item == 'int' and value.isdigit():
				if len(bin(int(value))) > limit_size:
					print(value+'长度大于'+limit_size)
					return False
			elif tar_item == 'char' and '\'' in value:
				if len(value) > limit_size:
					print(value+'长度大于'+limit_size)
					return False
			else:
				print(value+" 不是"+tar_item+'类型的')
				return False

			with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.txt', 'r') as f:
				if 'unique' in table_dict.get(target_items[index], []) or table_dict['primary_key'] == value:
					# TODO 	判定是否唯一
					pass
				if 'auto_increment'	 in table_dict.get(target_items[index], []):
					curr_max = 0
					# TODO	找到最大的
					
			# TODO 	还要判断 foreign_key
		return True