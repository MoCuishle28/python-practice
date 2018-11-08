'''
验证数据
'''
import os
import re
import json


from config import db_path, dict_path


class Valid(object):

	# 检验属性是否存在
	@classmethod
	def valid_items_exist(cls, target_items, table_dict):
		for item in target_items:
			if item not in table_dict.keys():
				print(item," 不存在")
				return False
		return True


	# 验证不带制定字段的插入
	@classmethod
	def valid_items_limit_without_targetItems(cls, values_list, table_dict, table_name, curr_database):
		filds_cnt =	len(table_dict) if 'primary_key' not in table_dict else len(table_dict) - 1 # 字段数
		target_items = []
		# 有省略了某些可以为空的数据
		if len(values_list) == filds_cnt:
			target_items = [k for k in table_dict.keys()]
			if 'primary_key' in target_items:
				target_items.remove('primary_key')
		elif len(values_list) != filds_cnt:
			for k,v in table_dict.items():
				if 'notnull' in v:
					target_items.append(k)
		return cls.valid_items_limit(values_list, target_items, table_dict, table_name, curr_database)		


	# 找到自动增长的当前值
	@classmethod
	def find_auto_increment(cls, old_data, table_dict, key):
		curr_max = 0
		for item in old_data:
			if item[table_dict.get(key)[-1]] > curr_max:
				curr_max = item[table_dict.get(key)[-1]]
		return curr_max+1


	# 根据数据字典判定插入数据的约束是否成立 带values的
	@classmethod
	def valid_items_limit(cls, values_list, target_items, table_dict, table_name, curr_database):
		'''
		values_list:		插入数据列表	(values中指定的内容)
		target_items:		字段列表
		table_dict:			数据字典
		'''
		if len(values_list) != len(target_items):
			print('插入数据数量与字段数不匹配')
			return False
		with open(db_path + '\\' + curr_database + '\\'+table_name+'.db', 'r') as f:
			old_data = f.read().strip().replace('\n','').split(';')
			old_data = [item.replace('\'','') for item in old_data]
			old_data.pop()
			old_data = cls.form_table_data(old_data, table_dict)	# 对读取出来的字符串列表进行规范化处理 组成一个二维列表

		# 对空值进行判定
		index = 0
		cls.form_values_list(values_list, table_dict)	# 把values_list中的int float进行转换
		for k,v in table_dict.items():
			if k == 'primary_key':
				continue
			if ('auto_increment' not in table_dict[k]) and ('notnull' in table_dict[k] or k in table_dict['primary_key']) and (k not in target_items or values_list[index]=='\'\'' or values_list[index] == '\' \''):
				print(k,'不能为空')
				return False
			elif k not in table_dict.get('primary_key') and 'notnull' not in table_dict[k] and k not in target_items:
				values_list.insert(index, '')
				target_items.insert(index, k)
			elif ('auto_increment' in table_dict[k]) and k not in target_items:	# 能自动增加的必然不会是可以为null的
				curr = cls.find_auto_increment(old_data, table_dict, k)
				values_list.insert(index, curr)
				target_items.insert(index, k)
			index += 1

		for index,value in enumerate(values_list):
			if not cls.valid_type_limit(table_dict, target_items, value, index):
				return False
			# 判定唯一性约束是否成立
			if 'unique' in table_dict.get(target_items[index], []) or target_items[index] in table_dict['primary_key']:
				# 判定是否唯一
				for item in old_data:
					value = value.replace('\'','') if type(value) == str and '\'' in value else value
					value = value.replace('\"','') if type(value) == str and '\"' in value else value
					if item[ table_dict.get(target_items[index])[-1] ] == value:
						print(value,"重复出现,不符合约束要求")
						return False
			# 判断 foreign_key
			if 'foreign_key' in table_dict.get(target_items[index], []):
				# TODO
				pass
		return True


	# 验证类型及大小是否匹配
	@classmethod
	def valid_type_limit(cls, table_dict, target_items, value, index):
		is_item_size = lambda x: 'char' in x or 'int' in x		# 判断是否是长度约束
		item_size = 5
		tar_item = ''	# 数据类型
		for item in table_dict.get(target_items[index], []):
			if is_item_size(item):
				item_size = int(re.findall(r'[(](.*?)[)]', item).pop())
				tar_item = item.split('(')[0]
				break
		limit_size = item_size 	# 数据长度约束
		if tar_item == 'int' and (type(value) is int or value.isdigit()):
			if len(bin(int(value))) > limit_size:
				print(value,'长度大于',limit_size)
				return False
		elif tar_item == 'char' and ('\'' in value or not value.isdigit()):
			if len(value) > limit_size:
				print(value,'长度大于',limit_size)
				return False
		else:
			print(value,"不是",tar_item,'类型的')
			return False
		return True


	# 对读取的数据表数据进行规范化 转换为二维列表 包含 int 和 float的转换
	@classmethod
	def form_table_data(cls, old_data, table_dict):
		ret = []
		for item in old_data:
			item = item.replace('[', '')
			item = item.replace(']', '')
			item = item.replace('\"', '')
			item = item.replace(' ','').split(',')
			for k,v in table_dict.items():
				for x in v[:-1]:
					if 'int' in x:
						item[v[-1]] = int(item[v[-1]])
						break
					elif 'double' in x:
						item[v[-1]] = float(item[v[-1]])
						break
			ret.append(item)
		return ret


	# 对待插入数据进行 int 和 float的转换
	@classmethod
	def form_values_list(cls, values_list, table_dict):
		ret = []
		for k,v in table_dict.items():
			for x in v[:-1]:
				if 'int' in x and ('\'' not in values_list[v[-1]] and '\"' not in values_list[v[-1]]):
					values_list[v[-1]] = int(values_list[v[-1]])
				elif 'float' in x and ('\'' not in values_list[v[-1]] and '\"' not in values_list[v[-1]]):
					values_list[v[-1]] = float(values_list[v[-1]])