import os
import json
import getpass


from werkzeug.security import generate_password_hash, check_password_hash
from sql_function import SQL_Func
from config import db_path, dict_path
from valid import Valid


with open(dict_path+'\\sql_os.dict', 'r') as f:
	sql_os = f.read()
sql_os_set = set(sql_os.split())	# 操作语句集合
sql_func = {}						# 操作语句与对应的函数
for sql in sql_os_set:
	sql_func[sql] = getattr(SQL_Func, sql, None)


username = input('username:')
psw = getpass.getpass('password:')
# 输入密码
with open(dict_path+'\\user.json', 'r') as f:
	data = json.load(f)
	password = data.get(username).get('password') if username in data else ''
	if not check_password_hash(password, psw):
		print('密码错误!')
		exit()


general_oper = {'show', 'describe', 'cls', 'exit'}
oper_dict = {'r':['select'], 'w':['insert'], 'u':['update', 'delete', 'alter']}

permission_list = data.get(username).get('permissions').split(';')

# 当前用户能用的数据表及其对应的数据库 -> table_name:db_name
user_can_use = {}
can_use_db = set()

for can in permission_list:
	can_list = can.split('-')
	db_name, table_name, can_oper = can_list[0], can_list[1], can_list[2]
	user_can_use[table_name] = [db_name]
	can_use_db.add(db_name)
	oper_list = can_oper.split(',')
	for oper in oper_list:
		for op in oper_dict[oper]:
			user_can_use[table_name].append(op)	# 把能进行的操作加入


Keep = True
command = ''
command_str = ''

while Keep:
	command += ' ' + input(SQL_Func.curr_database + '> ')
	command = command.strip()

	if command and command[-1] == ';':
		command = command.replace(';','')
		command_str = command
		if not command:
			continue
	else:
		print('--> ', end='')
		continue

	if command.split()[0] not in sql_os_set:
		print(command.split()[0], 'not exist this sql.')
		command = ''
		continue
	else:
		command_str = command_str.strip()
		command_list = command.split()

		if username != 'root' and command_list[0] not in general_oper and not Valid.valid_oper(user_can_use, can_use_db, command_str, SQL_Func.curr_database, SQL_Func.tables_set):
			print('你没有', command_list[0], '操作的权限')
		else:
			func = sql_func.get(command_list[0])
			print(func(command_str)) 	# 调用相关的处理函数
		command = ''