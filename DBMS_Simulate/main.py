import os
import json
import getpass
from werkzeug.security import generate_password_hash, check_password_hash
from sql_function import SQL_Func
from config import db_path, dict_path


with open(dict_path+'\\sql_os.dict', 'r') as f:
	sql_os = f.read()
sql_os_set = set(sql_os.split())	# 操作语句集合
sql_func = {}						# 操作语句与对应的函数
for sql in sql_os_set:
	sql_func[sql] = getattr(SQL_Func, sql, None)


# 输入密码
with open(dict_path+'\\user.json', 'r') as f:
	data = json.load(f)
	password = data.get('root').get('password')
	psw = getpass.getpass('password:')
	if not check_password_hash(password, psw):
		print('密码错误!')
		exit()


Keep = True
command = ''
command_str = ''

while Keep:
	command += ' ' + input(SQL_Func.curr_database + '>')
	command = command.strip()

	if command[-1] == ';':
		command = command.replace(';','')
		command_str = command
	else:
		print('-->', end='')
		continue

	if command.split()[0] not in sql_os_set:
		print('not exist this sql.')
		command = ''
		continue
	else:
		func = sql_func.get(command.split()[0])
		print(func(command_str)) 	# 调用相关的处理函数
		command = ''