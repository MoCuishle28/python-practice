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
	key_word = {'auto_increment', 'notnull', 'primary_key', 'unique', 'char', 'int'}

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
		is_key_word = lambda x: x not in cls.key_word and 'char' not in x and 'int' not in x	
		# create table t(id int(11) notnull auto_increment, name char(20) notnull, primary_key(id));
		result = re.match(r'create table (?P<name>\w+)\((?P<permission>.+)\)$', command_str)
		if not result:
			return False

		name = result.group('name')
		if name in cls.tables_set:
			print(name, '已存在')
			return False

		cls.add_to_database_dict(name)	# 把表名写入对应数据库的数据字典
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

			field_name = filter(is_key_word, x)	# 得到一个符合 is_key_word 要求的迭代器
			tar_name = ''
			for field in field_name:
				table_dict[field] = []
				tar_name = field
			field_name = tar_name
			for value in x:
				if value != field_name:
					table_dict[field_name].append(value)
		
		with open(db_path + '\\' + cls.curr_database + '\\'+name+'.json', 'w') as f:
			json.dump(table_dict, f)
		return True



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