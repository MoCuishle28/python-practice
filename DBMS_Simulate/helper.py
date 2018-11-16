'''
救救孩子吧
'''
import os
import re
import json
import shutil
import itertools


from config import db_path, dict_path
from valid import Valid
from BTree import B_Plus_Tree


class Helper(object):

	# 讲default 后面的值转换为指定的约束
	@classmethod
	def form_default_value(cls, operates_list ,default_value):
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
	def delete_field_data(cls, curr_database, table_name, table_dict, delete_field):
		'''
		删除指定字段的数据
		'''
		with open(db_path + '\\' + curr_database + '\\'+table_name+'.db', 'r') as f:
			old_data = f.read().strip().replace('\n','').split(';')
			old_data = [item.replace('\'','') for item in old_data]
			old_data.pop()
			old_data = Valid.form_table_data(old_data, table_dict)	# 对读取出来的字符串列表进行规范化处理 组成一个二维列表

		del_index = table_dict[delete_field][-1]
		for x in old_data:
			x.pop(del_index)
		with open(db_path + '\\' + curr_database + '\\'+ table_name +'.db', 'w') as f:
			for item in old_data:
				f.write('\n' + str(item) + ';')


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
		# 为原来的添加默认值
		cls.set_default_in_old_data(curr_database, table_name, table_dict, new_field)

		for k,v in new_field_dict.items():
			v[-1] = end_index
			end_index += 1
			table_dict[k] = v
		return table_dict


	@classmethod
	def drop_field(cls, table_name, table_dict, operates_list, key_word, curr_database, tables_set):
		'''
		删除字段
		operates_list:	字段名
		return:			修改后的数据字典	/ False
		'''
		# 删除数据中对应字段的数据项
		cls.delete_field_data(curr_database, table_name, table_dict, operates_list[0])
		del table_dict[operates_list[0]]
		if operates_list[0] in table_dict.get('primary_key', []):
			table_dict.get('primary_key', []).remove(operates_list[0])
			if table_dict.get('primary_key', []) == []:
				del table_dict['primary_key']
		if not table_dict:	# 若已经删除所有字段 则删除表
			cls.drop_table(curr_database, table_name, tables_set)
			return False

		index = 0
		for k,v in table_dict.items():
			if k != 'primary_key':
				table_dict[k][-1] = index
				index += 1
		return table_dict


	@classmethod
	def modify_field(cls, table_name, table_dict, operates_list, key_word, default_value, curr_database, tables_set):
		'''
		修改字段
		operates_list:	操作列表(包含：字段名 字段约束)
		return:			修改后的数据字典	/ False
		'''
		table_dict = cls.drop_field(table_name, table_dict, operates_list, key_word, curr_database, tables_set)
		return cls.add_field(table_name, table_dict, operates_list, key_word, default_value, curr_database)



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


	@classmethod
	def drop_database(cls, database_name):
		with open(dict_path+'\\'+'database.dict', 'r') as f:
			database_list = f.read().split()
		database_list.remove(database_name)
		with open(dict_path+'\\'+'database.dict', 'w') as f:
			for x in database_list:
				f.write('\n'+x)
		shutil.rmtree('data\\'+database_name)	# 删除对应文件夹


	@classmethod
	def drop_table(cls, curr_database, table_name, tables_set):
		with open(db_path + '\\' + curr_database + '\\tables.dict', 'r') as f:
			tables_list = f.read().split()
		tables_list.remove(table_name)
		with open(db_path + '\\' + curr_database + '\\tables.dict', 'w') as f:
			for x in tables_list:
				f.write('\n'+x)
		os.remove(db_path + '\\' + curr_database + '\\'+table_name+'.json')
		os.remove(db_path + '\\' + curr_database + '\\'+table_name+'.db')
		tables_set.remove(table_name)


	@classmethod
	def calculate(cls, var_tuple, sign, old_data, table_dict, **kw):
		'''
		按照布尔计算得出结果集合
		return:		行号的集合(set)
		'''
		sign_set = {'<':lambda v1,v2: v1<v2, '>':lambda v1,v2: v1>v2,
					'=':lambda v1,v2: v1==v2, '!=':lambda v1,v2: v1!=v2,
					'<=':lambda v1,v2: v1<=v2, '>=':lambda v1,v2: v1>=v2,
					'in':lambda v,s: v in s, 'notin':lambda v,s: v not in s}

		field_name, value = var_tuple
		name_to_index = kw.get('name_to_index', {})
		old_data_list = kw.get('old_data_list', [])
		field_table = kw.get('field_table', '')
		value_table = kw.get('value_table', '')
		field_table_dict = kw.get('field_table_dict', {})
		value_table_dict = kw.get('value_table_dict', {})

		if 'select' in value:
			# TODO 先用 select 函数得到结果集
			pass
		elif value in table_dict:				# if value

			out_data = old_data_list[name_to_index[field_table]]		# 外循环数据
			iner_data = old_data_list[name_to_index[value_table]]			# 内循环
			if len(out_data) < len(iner_data):						# 让小的数据在内循环
				out_data, iner_data = iner_data, old_data
				field_name, value = value, field_name
				field_table_dict, value_table_dict = value_table_dict, field_table_dict


			judge_func = sign_set[sign] if sign in sign_set else 'exist'		# TODO 写 exist
			index = field_table_dict[field_name][-1]		# 内循环字段在哪一列
			value_index = value_table_dict[value][-1]		# 外循环字段

			link_list = []	# 选出来的列表合并后放入此列表
			for x in out_data:
				for y in iner_data:
					if judge_func(x[index], y[value_index]):
						link_list.append(x + y)

			f1 = lambda v1,v2: v1 == v2
			f2 = lambda v1,v2: set(v1).issubset(set(v2))
			# judge_func = f1 if len(old_data[0]) == len(link_list[0]) else f2
			judge_func = f2
			
			ret = set()
			for line_num, item in enumerate(old_data):
				for judge_item in link_list:
					# select * from t,t1 as tt where s1 = tt.s1;
					if judge_func(judge_item, item):
						ret.add(line_num)
						break
		else:
			value = cls.form_value(table_dict, field_name, value)
			judge_func = sign_set[sign] if sign in sign_set else 'exist'		# TODO 写 exist
			index = table_dict[field_name][-1]	# 字段在哪一列
			ret = set()
			for line_num, item in enumerate(old_data):
				if judge_func(item[index], value):
					ret.add(line_num)
		return ret


	@classmethod
	def union_calculate(cls, set_tuple, sign):
		'''
		对两个集合进行 并, 交 运算	| -> 并集 ,  & -> 交集
		return:		行号的集合(set)
		'''
		s1, s2 = set_tuple
		return s1 & s2 if sign == 'and' else s1 | s2


	@classmethod
	def parse_where_judge(cls, judge_list, old_data, table_dict, **kw):
		'''
		TODO:	in ( select ... ) 也许可以先笛卡儿积合并成一个 old_data 再处理?
		解析where后面的字符串 并计算得出结果
		judge_list:	where后的字符串
		return:		计算结果 一个集合	(元素为符合条件的数据元组行号)? / False
		'''
		calculate_set = {'>', '<', '=', '!=', '>=', '<=', 'in', 'notin', 'exist', 'not', '!'}
		union_set = {'and', 'or'}
		var_stack = []				# 存待计算变量的栈	如：id > 1 的 id,1
		calculate_sign_stack = []	# 存计算符号的栈		如：>, in, !=, not in 等
		union_sign_stack = []		# 存集合运算的栈		如：and, or
		result_stack = []			# 存计算结果	元素为集合(set)

		name_to_index = kw.get('name_to_index', {})
		old_data_list = kw.get('old_data_list', [])
		table_dict_list = kw.get('table_dict_list', [])

		# 加上空格 方便分割
		for item in calculate_set | union_set | {'(',')'}:
			judge_list = judge_list.replace(item, ' '+item+' ')
		judge_list = judge_list.split()
		size = len(judge_list)
		for i,x in enumerate(judge_list):	# 把 >=, <=, !=, not in 合并成一个字符串
			if i+1 < size and judge_list[i] in calculate_set and judge_list[i+1] in calculate_set:
				judge_list[i] = judge_list[i] + judge_list[i+1]
				judge_list.pop(i+1)

		# 进行运算
		try:
			for item in judge_list:
				if item == '(':
					var_stack.append(item)
				elif item in calculate_set:
					calculate_sign_stack.append(item)
				elif item in union_set:
					union_sign_stack.append(item)
				elif item == ')':
					# 集合计算
					if var_stack[-1] != '(':
						print('sql输入错误')
						return False
					else:
						var_stack.pop()
						if union_sign_stack != []:
							set_tuple = (result_stack.pop(), result_stack.pop())	# 待计算的集合
							result_stack.append(cls.union_calculate(set_tuple, union_sign_stack.pop()))
				else:	# 否则为field, value 或者 feild in (select...)
					var_stack.append(item)
					if calculate_sign_stack != []:
						# 计算 并放入 result_stack中
						value = var_stack.pop()
						field = var_stack.pop()
						if field not in table_dict or field == 'primary_key':
							print('{}属性不存在'.format(field))
							return False
						if value not in table_dict and not Valid.valid_type_limit(table_dict, [field], value, 0):
							print('属性类型不匹配{},{}'.format(field, value))
							return False
						field_table = ''
						value_table = ''
						field_table_dict = {}
						value_table_dict = {}
						for i,td in enumerate(table_dict_list):
							if field in td:	# 如何获取表名?
								field_table = name_to_index[i]
								field_table_dict = td
							if value in td:
								value_table = name_to_index[i]
								value_table_dict = td
						result_stack.append(cls.calculate((field, value), calculate_sign_stack.pop(), old_data, table_dict, name_to_index=name_to_index, old_data_list=old_data_list, field_table=field_table, value_table=value_table, field_table_dict=field_table_dict, value_table_dict=value_table_dict))

			while union_sign_stack and len(result_stack) > 1:
				set_tuple = (result_stack.pop(), result_stack.pop())
				result_stack.append(cls.union_calculate(set_tuple, union_sign_stack.pop()))

		except Exception as e:
			print('sql输入错误', e)
			raise e

		if len(result_stack) != 1 or var_stack != [] or calculate_sign_stack != [] or union_sign_stack != []:
			print('sql输入错误')
			return False
		return result_stack.pop()


	@classmethod
	def delete_with_where(cls, curr_database, table_name, judge_list, table_dict):
		'''
		delete from t where id = 3
		delete from t where id >3 or ( name = 'a0' or ( name = 'a1' and id= 1));
		delete from t where id >= 4 or ( (id <= 2 and name = 'a2') or (id=1 and name='a1') );
		TODO 加上 in (select ...) 的嵌套
		'''
		with open(db_path + '\\' + curr_database + '\\' + table_name + '.db', 'r') as f:
			old_data = f.read().strip().replace('\n','').split(';')
			old_data = [item.replace('\'','') for item in old_data]
			old_data.pop()
			old_data = Valid.form_table_data(old_data, table_dict)	# 对读取出来的字符串列表进行规范化处理 组成一个二维列表
		if judge_list[0] != '(':
			judge_list = '( '+judge_list+' )'

		# 分析where中的内容 得到行号集合
		try:
			del_index_set = cls.parse_where_judge(judge_list, old_data, table_dict)
			with open(db_path + '\\' + curr_database + '\\'+ table_name +'.db', 'w') as f:
				for index,item in enumerate(old_data):
					if index not in del_index_set:
						f.write('\n' + str(item) + ';')
				print('受影响元组数', len(del_index_set))

			items = Valid.have_index(table_dict)	# 拿到拥有索引的字段列表
			if not items or not del_index_set:
				return True
			# 调整索引
			cls.modify_B_Plus_Tree(curr_database, table_name, items, table_dict)
		except Exception as e:
			print(e)
			return False
		return True


	@classmethod
	def delete_without_where(cls, curr_database, table_name):
		# 删除表的所有数据
		tree = B_Plus_Tree(3)
		with open(db_path + '\\' + curr_database + '\\'+table_name+'.json', 'r') as f:
			table_dict = json.load(f)
		items = Valid.have_index(table_dict)
		if not items:
			return
		for item in items:
			index_name = index_name = '_'+table_name+'_'+item+'_index'
			tree.save(db_path + '\\' + curr_database + '\\' + index_name)
		with open(db_path + '\\' + curr_database + '\\'+ table_name +'.db', 'w') as f:
			f.write('')


	@classmethod
	def update_with_where(cls, curr_database, table_name, field_tuple, judge_list, table_dict):
		'''
		judge_list:		where 后的判定条件
		update t1 set str2 = '1' where id >= 3 and id < 6 and str1='a3';
		'''
		field_name, value = field_tuple
		if not Valid.valid_type_limit(table_dict, [field_name], value, 0):
			print(field_name, ':', value, '不符合类型')
			return False
		old_data = cls.load_old_data_in_list(curr_database, table_name, table_dict)
		if judge_list[0] != '(':
			judge_list = '( '+judge_list+' )'

		change_index = table_dict[field_name][-1]
		judge_set = cls.parse_where_judge(judge_list, old_data, table_dict)	# 解析出符合条件的行号(从0起)集合

		if ('unique' in table_dict[field_name] or field_name in table_dict['primary_key']) and len(judge_set) > 1:
			print(field_name, '不能重复')
			return False
		if 'notnull' in table_dict[field_name] and value == '':
			print(field_name, '不能为空')
			return False

		with open(db_path + '\\' + curr_database + '\\'+ table_name +'.db', 'w') as f:
			for index,item in enumerate(old_data):
				if index in judge_set:		# 符合条件则修改
					item[change_index] = value
				f.write('\n' + str(item) + ';')
		print('受影响元组数', len(judge_set))
		
		for item in table_dict[field_name]:
			if type(item) is str and '_index' in item:
				cls.modify_B_Plus_Tree(curr_database, table_name, [field_name], table_dict)	# 调整索引
				break
		return True

	@classmethod
	def update_without_where(cls, curr_database, table_name, field_tuple, table_dict):
		field_name, value = field_tuple
		old_data = cls.load_old_data_in_list(curr_database, table_name, table_dict)
		if not Valid.valid_type_limit(table_dict, [field_name], value, 0):
			print(field_name, ':', value, '不符合类型')
			return False
		if ('unique' in table_dict[field_name] or field_name in table_dict['primary_key']) and len(old_data) > 1:
			print(field_name, '不能重复')
			return False
		if 'notnull' in table_dict[field_name] and value == '':
			print(field_name, '不能为空')
			return False
		index = table_dict[field_name][-1]
		with open(db_path + '\\' + curr_database + '\\'+ table_name +'.db', 'w') as f:
			for item in old_data:
				item[index] = value
				f.write('\n' + str(item) + ';')

		items = Valid.have_index(table_dict)	# 拿到拥有索引的字段列表
		if not items:
			return True
		cls.modify_B_Plus_Tree(curr_database, table_name, items, table_dict)	# 调整索引
		# TODO 有相同元素时 删除产生的和插入产生的少个单引号...


	@classmethod
	def project(cls, table_dict, data, items_list):
		'''
		投影操作
		items_list:		需要投影的字段
		'''
		if not data:
			print('(NULL)')
			return 
		project_index = []
		if items_list[-1] == '*':
			items_list.pop()
			for k in table_dict.keys():
				if k != 'primary_key':
					items_list.append(k)
		elif 'count' in items_list[-1]:
			item = re.findall(r'[(](.*?)[)]', items_list[-1])
			if item[-1] == '*':
				print(len(data))
				return

		print('------------')
		for item in items_list:
			print(item, end='  ')
			project_index.append(table_dict[item][-1])
		print()
		print('------------')
		for item in data:
			for index in project_index:
				print(item[index], end='  ')
			print()
		print('------------')


	@classmethod
	def select_with_where(cls, old_data, table_dict, items_list, judge_list, name_to_index, old_data_list, table_dict_list):
		'''
		name_to_index:	表名到 old_data_list 位置的映射
		return:			符合条件的列表, 被选择出的字段
		'''
		if judge_list[0] != '(':
			judge_list = '( '+judge_list+' )'
		judge_set = cls.parse_where_judge(judge_list, old_data, table_dict, name_to_index=name_to_index, old_data_list=old_data_list, table_dict_list=table_dict_list)
		if judge_set == False:
			return [], []
		project_data = []
		for i,item in enumerate(old_data):
			if i in judge_set:
				project_data.append(item)
		return project_data, items_list


	@classmethod
	def load_dict_and_data(cls, curr_database, table_name_list, tables_set, items_list):
		'''
		处理 from 后面多个表名（包括 as ,此时需要对数据字典对应的key改名） 读取数据字典, 数据
		table_name_list:	以 , 分割的数据表名list
		return:				返回 table_dict_list, old_data_list, 新字段名, 每个表在old_data_list中的位置
		'''
		if len(table_name_list) == 1:	# 如果只有一个表 不必笛卡儿积
			table_name = table_name_list[-1]
			if table_name not in tables_set:
				print(table_name, '表不存在')
				return [], [], [], {}, []
			with open(db_path + '\\' + curr_database + '\\'+table_name+'.json', 'r') as f:
				table_dict = json.load(f)
			old_data = cls.load_old_data_in_list(curr_database, table_name, table_dict)
			return table_dict, old_data, items_list, {}, []

		old_table_name = []
		new_table_name = []
		table_dict_list = []
		old_data_list = []
		map_new_to_old_name = {}		# 新旧表名映射
		table_name_to_index_map = {}	# 新表名:在old_data_list 中的位置
		# 取出 as 后面的重命名
		for table_name in table_name_list:
			new_name = ''
			old_table_name.append(table_name.split('as')[0].strip())
			if old_table_name[-1] not in tables_set:
				print(old_table_name[-1], '表不存在')
				return [], [], [], {}, []
			if 'as' in table_name:
				new_name = table_name.split('as')[-1].strip()
			new_table_name.append(new_name if new_name else table_name.split('as')[0].strip())
			map_new_to_old_name[table_name.split('as')[0].strip()] = new_name if new_name else table_name.split('as')[0].strip()

		index = 0
		for name in old_table_name:
			with open(db_path + '\\' + curr_database + '\\'+ name + '.json', 'r') as f:
				table_dict = json.load(f)
			table_dict_list.append(table_dict)		# 放入字典列表
			old_data_list.append(cls.load_old_data_in_list(curr_database, name, table_dict))	# 放入原数据列表
			table_name_to_index_map[map_new_to_old_name[name]] = index
			table_name_to_index_map[index] = map_new_to_old_name[name]
			index += 1

		index = 0
		tmp_dict = {}
		old_new_dict = {}
		new_table_dict_list = []
		new_field_list = []
		old_table_dict_list = []
		# 对对应的数据字典 进行字段改名
		for i,table_dict in enumerate(table_dict_list):
			del table_dict['primary_key']
			if old_table_name[i] != new_table_name[i]:
				for k,v in table_dict.items():
					tmp_v = v.copy()
					tmp_v[-1] = index
					index += 1
					tmp_dict[new_table_name[i]+'.'+k] = tmp_v
					old_new_dict[new_table_name[i]+'.'+k] = v
					new_field_list.append(new_table_name[i]+'.'+k)
			else:
				for k,v in table_dict.items():
					tmp_v = v.copy()
					tmp_v[-1] = index
					index += 1
					tmp_dict[k] = tmp_v
					old_new_dict[k] = v
					new_field_list.append(k)
			new_table_dict_list.append(tmp_dict)
			old_table_dict_list.append(old_new_dict)	# 维护一个有新名字 和 旧属性的字典列表
			tmp_dict = {}
			old_new_dict = {}
		return new_table_dict_list, old_data_list, new_field_list, table_name_to_index_map, old_table_dict_list


	@classmethod
	def descartes(cls, table_dict_list, old_data_list):
		'''
		table_dict_list:	包含多个表的数据字典list
		old_data_list:		包含多个表的数据 每个元素是一个表的 old_data
		return:				笛卡儿积后的数据字典,  笛卡儿积后的old_data
		'''
		curr_data = []
		curr_table_dict = {}
		for d in table_dict_list:
			curr_table_dict = {**curr_table_dict, **d}

		for item in itertools.product(*old_data_list):
			curr_data.append(item)

		ret_data = []
		for item in curr_data:
			tmp = []
			for x in item:
				tmp.extend(x)
			ret_data.append(tmp)
		return curr_table_dict, ret_data


	@classmethod
	def describe_table(cls, curr_database, table_name):
		with open(db_path + '\\' + curr_database + '\\'+table_name+'.json', 'r') as f:
			table_dict = json.load(f)
		print('----------------')
		print('Tabel: ', table_name)
		print('----------------')
		for k,v in table_dict.items():
			value = str(v)
			value = value.replace('[', '')
			value = value.replace(']', '')
			print(k+':   ', value)
		print('----------------')


	@classmethod
	def add_index(cls, curr_database, table_name, field_name, table_dict):
		if field_name not in table_dict:
			print(field_name, '不存在')
			return False

		index_name = '_'+table_name+'_'+field_name+'_index'
		if index_name in table_dict[field_name]:
			print(field_name, '已经存在索引')
			return False
		old_data = cls.load_old_data_in_list(curr_database, table_name, table_dict)
		table_dict[field_name].insert(-1, index_name)
		data_col = table_dict[field_name][-1]
		b_plus_tree = B_Plus_Tree(3)
		for i,x in enumerate(old_data):
			b_plus_tree.insert([x[data_col], i])
		b_plus_tree.save(db_path + '\\' + curr_database + '\\' + index_name)	# 以索引名命铭文件


	@classmethod
	def drop_index(cls, curr_database, table_name, field_name, table_dict):
		if field_name not in table_dict:
			print(field_name, '不存在')
			return False
		index_name = '_'+table_name+'_'+field_name+'_index'
		if index_name not in table_dict[field_name]:
			print(field_name, '无索引')
			return False

		os.remove(db_path + '\\' + curr_database + '\\'+ index_name +'.index')
		table_dict[field_name].remove(index_name)


	# 把文件中的数据读入到old_data二维表 并对其规范化
	@classmethod
	def load_old_data_in_list(cls, curr_database, table_name, table_dict):
		with open(db_path + '\\' + curr_database + '\\' + table_name + '.db', 'r') as f:
			old_data = f.read().strip().replace('\n','').split(';')
			old_data = [item.replace('\'','') for item in old_data]
			old_data.pop()
			old_data = Valid.form_table_data(old_data, table_dict)	# 对读取出来的字符串列表进行规范化处理 组成一个二维列表
		return old_data


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


	@classmethod
	def form_value(cls, table_dict, field_name, value):
		for judge in table_dict[field_name]:
			if type(judge) is not str:
				continue
			elif 'int' in judge:
				value = int(value)
				break
			elif 'float' in judge:
				value = float(value)
				break
			elif 'char' in judge:
				value = value.replace('\'', '')
				break
		return value


	@classmethod
	def modify_B_Plus_Tree(cls, curr_database, table_name, items, table_dict):
		'''
		调整B+树
		items:	有B+树索引的字段
		'''
		new_data = cls.load_old_data_in_list(curr_database, table_name, table_dict)
		for item in items:
			index_name = index_name = '_'+table_name+'_'+item+'_index'
			tree = B_Plus_Tree(3)
			for i,value in enumerate(new_data):
				tree.insert([value[ table_dict[item][-1] ], i])
			tree.save(db_path + '\\' + curr_database + '\\' + index_name)
			tree.show()