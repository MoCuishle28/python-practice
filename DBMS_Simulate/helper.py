'''
救救孩子吧
'''
import os
import re
import json


from config import db_path, dict_path
from valid import Valid


class Helper(object):

	# 讲default 后面的值转换为指定的约束
	@classmethod
	def form_default_value(cls,operates_list , default_value):
		result = re.match(r'(?P<field_name>\w+)=(?P<value>.+)', default_value)
		if not result:
			print(default_value, '语法错误')
			return False, False
		field_name = result.group('field_name')
		default_value = result.group('value')

		for item in operates_list:	# 数据转换
			if 'int' in item and '\'' not in default_value:
				default_value = int(default_value)
				break
			elif 'float' in item and '\'' not in default_value:
				default_value = float(default_value)
				break
			elif ('int' in item or 'float' in item) and '\'' in default_value:
				print(default_value, '不符合约束', item)
				return False, False
			elif 'char' in item:
				default_value = default_value.replace('\'','')
		return field_name, default_value


	@classmethod
	def set_default_in_old_data(cls, curr_database, table_name, table_dict, new_field):
		'''
		对原有数据设置 新增/修改 字段默认取值
		'''
		with open(db_path + '\\' + curr_database + '\\'+table_name+'.db', 'r') as f:
			old_data = f.read().strip().replace('\n','').split(';')
			old_data = [item.replace('\'','') for item in old_data]
			old_data.pop()
			old_data = Valid.form_table_data(old_data, table_dict)	# 对读取出来的字符串列表进行规范化处理 组成一个二维列表
		new_data = []
		field_name, value = new_field 	# 拆包
		for item in old_data:
			item.append(value)
			new_data.append(item)
		with open(db_path + '\\' + curr_database + '\\'+table_name+'.db', 'w') as f:
			for item in new_data:
				f.write('\n' + str(item) + ';')


	@classmethod
	def add_field(cls, table_name, table_dict, operates_list, key_word, default_value, curr_database):
		'''
		添加字段
		operates_list:	操作列表(包含：字段名 字段约束)
		default_value:	设置默认数值的字符串
		return:			修改后的数据字典	/ False
		'''
		field_name, default_value = cls.form_default_value(operates_list, default_value)
		if field_name == False:
			return False
		new_field = (field_name, default_value)
		end_index = 0
		# 找到最后一个索引值
		for k,v in table_dict.items():
			if k != 'primary_key' and v[-1] >= end_index:
				end_index = v[-1] + 1

		new_field_dict = cls.create_table_dict([operates_list], key_word)
		if new_field_dict == False:
			return False

		for k,v in new_field_dict.items():
			v[-1] = end_index
			end_index += 1
			table_dict[k] = v
		# 为原来的添加默认值
		cls.set_default_in_old_data(curr_database, table_name, table_dict, new_field)
		return table_dict


	@classmethod
	def drop_field(cls, table_name, table_dict, operates_list):
		'''
		删除字段
		operates_list:	操作列表(包含：字段名 字段约束)
		return:			修改后的数据字典	/ False
		'''
		pass


	@classmethod
	def modify_field(cls, table_name, table_dict, operates_list, key_word, default_value, curr_database):
		'''
		修改字段
		operates_list:	操作列表(包含：字段名 字段约束)
		return:			修改后的数据字典	/ False
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


	# 加载数据库集合
	@classmethod
	def load_database(cls):
		with open(dict_path+'\\database.dict', 'r') as f:
			database = f.read()
		return set(database.split())	# 现有的数据库


	# 添加数据库名字到对应数据库的数据字典中
	@classmethod
	def add_to_database_dict(cls, table_name, curr_database, tables_set):
		with open(db_path+'\\'+curr_database+'\\'+'tables.dict', 'a') as f:
			f.write('\n'+table_name)
		tables_set.add(table_name)