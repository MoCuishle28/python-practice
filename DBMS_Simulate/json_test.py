import json
from werkzeug.security import generate_password_hash, check_password_hash

user = {
	'root':{
			'password':generate_password_hash('123456'),
			'permissions':'w-r-u'
	},

	'user1':{
			'password':generate_password_hash('123456'),
			'permissions':'r'
	}
}


json_str = json.dumps(user)
print(json_str)


# json的文件相关
# with open('user.json', 'w') as f:
# 	json.dump(user, f)


# with open('user.json', 'r') as f:
# 	data = json.load(f)


# print(data['root'])
# print(data['root']['password'])
# print(check_password_hash(data.get('root').get('password'), '123456'))
# print(data.get('root').get('permissions'))


