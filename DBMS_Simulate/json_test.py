import json
from werkzeug.security import generate_password_hash, check_password_hash

user = {
	'root':{
			'password':generate_password_hash('123'),
			'permissions':'w-r-u'
	},
}


# json_str = json.dumps(user)
# print(json_str)


with open('test.json', 'r') as f:
	data = json.load(f)
print(data)
for k,v in data.items():
	print(k, ' ', v)

# json的文件相关
with open('user.json', 'w') as f:
	json.dump(user, f)


# with open('user.json', 'r') as f:
# 	data = json.load(f)


# print(data['root'])
# print(data['root']['password'])
# print(check_password_hash(data.get('root').get('password'), '123456'))
# print(data.get('root').get('permissions'))


