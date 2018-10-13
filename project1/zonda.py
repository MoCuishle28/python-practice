from app import create_app

app = create_app()

if __name__ == '__main__':
	# 生产环境下 nginx + uwsgi 有uwsgi加载flask模块执行
	# 若无 if __name__ == '__main__'...

	# host = '0.0.0.0' 表示可以接受外网访问
	# debug = True 可以不用重新编译代码 可以在网页上看到详细错误信息 但是上线前要写一个配置文件config
	# threaded=True 开启多线程模式
	app.run(host='0.0.0.0', debug=app.config['DEBUG'], threaded=True)