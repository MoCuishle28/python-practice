'''
数据库定义语言
如：create, alter, drop
'''
import os
import re
import json
import shutil


from config import db_path, dict_path
from valid import Valid
from helper import Helper


class SQL_Func(object):

	database_set = Helper.load_database()	# 所有数据库集合
	curr_database = ''				# 当前使用的数据库
	tables_set = set()				# 当前数据库的表
	# 保留字集合
	key_word = {'auto_increment', 'notnull', 'primary_key', 'foreign_key', 'unique', 'char', 'int', 'float'}


	@classmethod
	def use(cls, command_str):
		result = re.match(r'\s*use\s*(?P<name>\w+)\s*$', command_str)
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
		result = re.match(r'\s*show\s*databases\s*$', command_str)
		if result:
			print('----------')
			print('Databases:')
			print('----------')
			if not cls.database_set:
				print('(NULL)')
			for item in cls.database_set:				
				print(item)
		else:
			result = re.match(r'\s*show\s*tables\s*$', command_str)
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
		result = re.match(r'\s*create\s*(?P<operate_type>\w+)\s*(?P<name>\w+).*\s*$', command_str)
		if not result:
			return False

		operate_type = result.group('operate_type')
		name = result.group('name')

		if operate_type == 'database':
			if name in cls.database_set:
				print(name, '已存在')
				return False
			else:	# 创建数据库
				with open(dict_path+'\\'+'database.dict', 'a') as f:
					f.write('\n'+name)							# 写入数据库数据字典
				cls.database_set = Helper.load_database()				# 更新数据库集合

				os.mkdir(db_path + '\\' + name)		# 创建对应文件夹
				with open(db_path + '\\' + name + '\\tables.dict', 'w') as f:
					f.write('')
		elif operate_type == 'index':
			pass
		elif operate_type == 'user':
			pass
		else:	# 已使用数据库 则创建数据表
			return cls.createTable(command_str)
		return True


	# 创建Table 添加各种约束
	@classmethod 
	def createTable(cls, command_str):
		# create table t(id int(11) notnull auto_increment, name char(20) notnull, primary_key(id));
		result = re.match(r'\s*create\s*table\s*(?P<name>\w+)\((?P<permission>.+)\)\s*$', command_str)
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
		# table_dict = {}		# 创建表的数据字典
		table_dict = Helper.create_table_dict(permission, cls.key_word)
		if table_dict == False:
			return False
					
		Helper.add_to_database_dict(name, cls.curr_database, cls.tables_set)	# 把表名写入对应数据库的数据字典
		with open(db_path + '\\' + cls.curr_database + '\\'+name+'.json', 'w') as f:
			json.dump(table_dict, f)
		with open(db_path + '\\' + cls.curr_database + '\\'+name+'.db', 'w') as f:
			f.write('')
		return True


	# alter操作 包含数据表字段的增删改
	@classmethod
	def alter(cls, command_str):
		if cls.curr_database == '':
			print('请先选择数据库')
			return False
		result = re.match(r'\s*alter\s*table\s*(?P<table_name>\w+)\s*(?P<alter_type>\w+)\s*(?P<operate>.+)\s*default\s*(?P<default_value>.+)\s*$',command_str)
		if not result:
			result = re.match(r'\s*alter\s*table\s*(?P<table_name>\w+)\s*(?P<alter_type>\w+)\s*(?P<operate>.+)\s*', command_str)
			if not result:
				print('sql error')
				return False
		table_name = result.group('table_name')
		alter_type = result.group('alter_type')
		operates_list = result.group('operate').split()
		field_name = operates_list[0]
		default_value = result.group('default_value') if 'default_value' in result.groupdict() else ''

		with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.json', 'r') as f:
			table_dict = json.load(f)

		if table_name not in cls.tables_set:
			print(table_name, '不存在')
			return False
		# alter table t add launched char(10) notnull default launched='0';
		if alter_type == 'add':
			if field_name in table_dict:
				print(field_name, '字段已经存在')
				return False
			# 添加字段				
			table_dict = Helper.add_field(table_name, table_dict, operates_list, cls.key_word, default_value, cls.curr_database)
		# alter table b drop launched;
		elif alter_type == 'drop':
			if field_name not in table_dict:
				print(field_name, '字段不存在')
				return False
			table_dict = Helper.drop_field(table_name, table_dict, operates_list, cls.key_word, cls.curr_database, cls.tables_set)	# 删除字段
		elif alter_type == 'modify':
			if field_name not in table_dict:
				print(field_name, '字段不存在')
				return False
			# 修改字段
			table_dict = Helper.modify_field(table_name, table_dict, operates_list, cls.key_word, default_value, cls.curr_database)
		else:
			print(alter_type, '操作不存在')
			return False
		if table_dict != False:
			with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.json', 'w') as f:
				json.dump(table_dict, f)
			return True
		return False



	@classmethod
	def drop(cls, command_str):
		'''
		删除 数据库/表/索引/用户 等
		'''
		result = re.match(r'\s*drop\s*(?P<operate_type>\w+)\s*(?P<name>\w+)\s*$', command_str)
		if not result:
			print(command_str, 'sql语句错误')
			return False
		operate_type = result.group('operate_type')
		name = result.group('name')
		if operate_type == 'database':
			if name not in cls.database_set:
				print(name, '不存在')
				return False
			Helper.drop_database(name)
			cls.database_set = Helper.load_database()	# 更新数据库集合
			cls.curr_database = ''
		elif operate_type == 'table':
			if name not in cls.tables_set:
				print(name, '不存在')
				return False
			Helper.drop_table(cls.curr_database, name, cls.tables_set)
		elif operate_type == 'index':
			pass
		else:
			print(operate_type, '输入错误')
			return False	
		return True



	@classmethod
	def insert(cls, command_str):
		# insert into t('id','name') values(1, 'a');
		result = re.match(r'\s*insert\s*into\s*(?P<table_name>\w+)(?P<target_items>.*)\s*values\((?P<values_list>.+)\)\s*$', command_str)
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

		# 检验合法性:
		if target_items:	# 带指定插入内容
			if not Valid.valid_items_exist(target_items, table_dict):
				return False
			# 是否全部待插入数据约束判定都成立
			if Valid.valid_items_limit(values_list, target_items ,table_dict, table_name, cls.curr_database):
				# 如果约束成立 则将数据插入
				with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.db', 'a') as f:
					f.write('\n' + str(values_list) + ';')
			else:
				return False
		# 不带的指定字段的插入  验证默认插入顺序
		elif Valid.valid_items_limit_without_targetItems(values_list, table_dict, table_name, cls.curr_database):
			with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.db', 'a') as f:
				f.write('\n' + str(values_list) + ';')
		else:
			return False
		return True


	@classmethod
	def delete(cls, command_str):
		result = re.match(r'\s*delete\s*from\s*(?P<table_name>\w+)\s*(where)?\s*(?P<judge_list>.*)$', command_str)
		if not result or not cls.curr_database:
			print('sql错误')
			return False
		table_name = result.group('table_name')
		judge_list = result.group('judge_list')
		if table_name not in cls.tables_set:
			print(table_name, '不存在')
			return False
			
		if 'where' not in command_str:
			Helper.delete_without_where(cls.curr_database, table_name)
		elif 'where' in command_str:
			with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.json', 'r') as f:
				table_dict = json.load(f)
			return Helper.delete_with_where(cls.curr_database, table_name, judge_list, table_dict)
		return True


	@classmethod
	def cls(cls, command_str):
		if not re.match(r'\s*cls\s*$', command_str):
			return False
		os.system('cls')
		return True


	@classmethod
	def exit(cls, command_str):
		if not re.match(r'\s*exit\s*$', command_str):
			return False
		print('bye!')
		exit()
		return True