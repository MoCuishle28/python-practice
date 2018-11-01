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

	@classmethod
	def use(cls, command_str):
		result = re.match(r'use (?P<name>\w+)$', command_str)
		if 	not result:
			return False
		name = result.group('name')

		if cls.curr_database == '':			# 当前尚未使用数据库
			if name in cls.database_set:
				cls.curr_database = name
				with open(db_path + '\\' + name + '\\tables.dict', 'r') as f:
					tables = f.read()
					cls.tables_set = set(tables.split())	# 更新数据表集合
			else:
				print(name, '数据库不存在')
				return False
		else:
			print('已使用', cls.curr_database)
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
		result = re.match(r'create (?P<name>\w+)$', command_str)
		if not result:
			return False
		name = result.group('name')

		if cls.curr_database == '':	# 当前未使用数据库 则创建的是数据库
			if name in cls.database_set:
				print(name, '已存在')
				return False
			else:	# 创建数据库
				with open(dict_path+'\\'+'database.dict', 'a') as f:
					f.write('\n'+name)							# 写入数据库数据字典
				cls.database_set = load_database()				# 更新数据库集合

				os.mkdir(db_path + '\\' + name)		# 创建对应文件夹
				with open(db_path + '\\' + name + '\\tables.dict', 'w') as f:	# BUG
					f.write('')
		else:	# 已使用数据库 则创建数据表
			if name in cls.tables_set:
				print(name, '已存在')
				return False
			else:	# 创建表
				cls.createTable(command_str)
		return True


		@classmethod
		def createTable(cls, command_str):
			# 创建Table 添加各种约束
			pass
