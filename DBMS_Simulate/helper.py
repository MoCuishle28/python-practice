'''
救救孩子吧
'''
import os
import re
import json


from config import db_path, dict_path
from valid import Valid


class Helper(object):


	@classmethod
	def add_field(cls, table_name, table_dict, operates_list):
		'''
		添加字段
		operates_list:	操作列表(包含：字段名 字段约束)
		'''
		pass


	@classmethod
	def drop_field(cls, table_name, table_dict, operates_list):
		'''
		删除字段
		table_dict:		数据字典
		TODO
		'''
		pass


	@classmethod
	def modify_field(cls, table_name, table_dict, operates_list):
		'''
		修改字段
		table_dict:		数据字典
		TODO
		'''
		pass


	@classmethod
	def create_table_dict(cls, permission, key_word):
		'''
		创建数据字典
		permission:		包含字段名和字段约束的list
		'''
		is_not_key_word = lambda x: x not in key_word and 'char' not in x and 'int' not in x
		is_key_word = lambda x: x in key_word or 'char' in x or 'int' in x
		table_dict = {}		# 创建表的数据字典

		for index,x in enumerate(permission):
			if 'primary_key' in x[0]:
				key_list = re.findall(r'[(](.*?)[)]', x[0])
				key_list = key_list[0].split('/') if key_list else []
				table_dict['primary_key'] = key_list;	# 主键可能有多个
				continue

			field_name = filter(is_not_key_word, x)	# 得到一个符合 is_not_key_word 要求的迭代器
			tar_name = ''
			for field in field_name:
				if field in table_dict:
					print(field,'属性名重复')
					return False
				table_dict[field] = []
				tar_name = field
				break
			field_name = tar_name
			for value in x:										# 添加约束
				if value != field_name and is_key_word(value):	# 不是表名并且是关键字
					table_dict[field_name].append(value)
				elif value != field_name and not is_key_word(value):
					print(value+' 不是关键字')
					return False
			table_dict[field_name].append(index)	# 制定当前字段在数据表的第几列
		return table_dict


	# 添加数据库名字到对应数据库的数据字典中
	@classmethod
	def add_to_database_dict(cls, table_name, curr_database, tables_set):
		with open(db_path+'\\'+curr_database+'\\'+'tables.dict', 'a') as f:
			f.write('\n'+table_name)
		tables_set.add(table_name)