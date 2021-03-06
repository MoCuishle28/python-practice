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
from BTree import B_Plus_Tree


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
		result = re.match(r'\s*show\s*(?P<show_type>\w+)\s*$', command_str)
		if not result:
			print('sql错误')
			return False
		show_type = result.group('show_type')
		if show_type == 'databases':
			print('----------')
			print('Databases:')
			print('----------')
			if not cls.database_set:
				print('(NULL)')
			for item in cls.database_set:				
				print(item)
		elif show_type == 'tables':
			if not cls.curr_database:
				print('请先选择数据库')
				return False
			print('----------')
			print('Tables:')
			print('----------')
			if not cls.tables_set:
				print('(NULL)')
			for item in cls.tables_set:
				print(item)
		elif show_type == 'user':
			print('----------')
			print('User:')
			print('----------')
			with open(dict_path+'\\user.json', 'r') as f:
				user_data = json.load(f)
			for k,v in user_data.items():
				print(k, end='> ')
				for k2,v2 in v.items():
					if k2 != 'password':
						print(v2.split(';'))
				print('----------')
		else:
			return False
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
		elif operate_type == 'user':
			return Helper.create_user(command_str)
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
		# alter table t (add/drop)
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
		# alter table b add t3 char(10) notnull default t3='007';
		if alter_type == 'add':
			if field_name in table_dict:
				print(field_name, '字段已经存在')
				return False
			# 添加字段				
			table_dict = Helper.add_field(table_name, table_dict, operates_list, cls.key_word, default_value, cls.curr_database)
		# alter table b drop t3;
		elif alter_type == 'drop':
			if field_name not in table_dict:
				print(field_name, '字段不存在')
				return False
			table_dict = Helper.drop_field(table_name, table_dict, operates_list, cls.key_word, cls.curr_database, cls.tables_set)	# 删除字段
		# alter table b modify t3 int(10) notnull default t=1;
		elif alter_type == 'modify':
			if field_name not in table_dict:
				print(field_name, '字段不存在')
				return False
			# 修改字段
			table_dict = Helper.modify_field(table_name, table_dict, operates_list, cls.key_word, default_value, cls.curr_database, cls.tables_set)
		# alter table b index_add t1;
		elif alter_type == 'index_add':	# 添加索引
			Helper.add_index(cls.curr_database, table_name, field_name, table_dict)
		# alter table b index_drop t1;
		elif alter_type == 'index_drop':
			Helper.drop_index(cls.curr_database, table_name, field_name, table_dict)
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
		elif operate_type == 'user':		
			with open(dict_path+'\\user.json', 'r') as f:
				user_data = json.load(f)

			if name not in user_data:
				print(name, '用户不存在')
				return False

			del user_data[name]
			with open(dict_path+'\\user.json', 'w') as f:
				json.dump(user_data, f)
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
		# 检查有无索引
		old_data = Helper.load_old_data_in_list(cls.curr_database, table_name, table_dict)
		for k,v in table_dict.items():
			for item in v:
				if type(item) is str and '_index' in item:	# 说明有索引
					value = values_list[v[-1]]
					index_name = '_'+table_name+'_'+k+'_index'
					tree = B_Plus_Tree(3)
					tree.load(db_path + '\\' + cls.curr_database + '\\' + index_name)
					tree.insert([value, len(old_data) - 1])
					tree.show()
					tree.save(db_path + '\\' + cls.curr_database + '\\' + index_name)
					break
		return True


	@classmethod
	def delete(cls, command_str):
		# delete from t where...
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
	def update(cls, command_str):
		# update t1 set str2 = 'a' where id >= 3;
		result = re.match(r'\s*update\s*(?P<table_name>\w+)\s*set\s*(?P<field_name>\w+)\s*=\s*(?P<value>.+)\s*where\s*(?P<judge_list>.*)\s*$', command_str)
		if not result:
			result = re.match(r'\s*update\s*(?P<table_name>\w+)\s*set\s*(?P<field_name>\w+)\s*=\s*(?P<value>.+)\s*$', command_str)
			if not result or not cls.curr_database:
				print('sql错误')
				return False

		table_name = result.group('table_name')
		field_tuple = (result.group('field_name'), result.group('value').strip())
		judge_list = result.group('judge_list') if 'judge_list' in result.groupdict() else ''

		with open(db_path + '\\' + cls.curr_database + '\\'+table_name+'.json', 'r') as f:
			table_dict = json.load(f)
		if table_name not in cls.tables_set or field_tuple[0] not in table_dict:
			print(table_name if table_name not in cls.tables_set else field_tuple[0], '不存在')
			return False

		if judge_list:	# 带 where 的更新
			Helper.update_with_where(cls.curr_database, table_name, field_tuple, judge_list, table_dict)
		else:			# 不带 where 的更新
			Helper.update_without_where(cls.curr_database, table_name, field_tuple, table_dict)
		return True


	@classmethod
	def select(cls, command_str):
		# 先匹配有where的
		# select * from t1 as t,t2 where t.id <= 1 or (s1 = 't2_a2' and id >= 2);  多表查询
		# select s.name,c.name,s from stu as s,course as c,score where sid=s.id and cid = c.id;
		# select * from b,t where id = t1 and id != 4;
		result = re.match(r'\s*select\s*(?P<items_list>.+)\s*from\s*(?P<table_name>.+)\s*where\s*(?P<judge_list>.*)\s*$', command_str)
		if not result or not cls.curr_database:
			result = re.match(r'\s*select\s*(?P<items_list>.+)\s*from\s*(?P<table_name>\w+)\s*$', command_str)
			if not result or not cls.curr_database:
				print('sql错误')
				return False

		items_list = [item.strip() for item in result.group('items_list').split(',')]		# 投影项
		table_name_list = result.group('table_name').split(',')
		table_name_list = [ x.strip() for x in table_name_list ]
		judge_list = result.group('judge_list') if 'judge_list' in result.groupdict() else ''

		table_dict_list,old_data_list,new_field_list, name_to_index, old_table_dict_list = Helper.load_dict_and_data(cls.curr_database, table_name_list, cls.tables_set, items_list)

		if len(table_name_list) > 1:	# 如果有多个表
			table_dict, old_data = Helper.cartesian_product(table_dict_list, old_data_list)
		else:							# 否则单个表处理
			table_dict = table_dict_list
			old_data = old_data_list

		# select t.id,t1,t.s1,t2 from b, t1 as t where t.id = t1;
		for item in new_field_list:
			if 'count' not in item and item != '*' and (item not in table_dict or item == 'primary_key'):
				print(item, '字段不存在')
				return False
		if judge_list:	# 带 where 的查询
			project_data,items_list = Helper.select_with_where(old_data, table_dict, items_list, judge_list, name_to_index, old_data_list, old_table_dict_list, curr_database=cls.curr_database)
		else:
			project_data = old_data
		Helper.project(table_dict, project_data, items_list)
		return True


	@classmethod
	def describe(cls, command_str):
		# describe table t1;
		result = re.match(r'\s*describe\s*(?P<desc_type>\w+)\s*(?P<name>\w+)\s*$', command_str)
		# result = re.match(r'\s*show\s*databases\s*$', command_str)
		if not result or not cls.curr_database:
			print('sql错误')
			return False

		desc_type = result.group('desc_type')
		if desc_type == 'table':
			table_name = result.group('name')
			if table_name not in cls.tables_set:
				print(table_name, '表不存在')
			Helper.describe_table(cls.curr_database, table_name)	# 显示表结构
		else:
			print(desc_type, '未知操作')
			return False
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