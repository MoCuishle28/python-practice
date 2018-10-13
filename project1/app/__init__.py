from flask import Flask
from app.models.base import pool


def create_app():
	app = Flask(__name__)
	app.config.from_object('app.secure')
	register_blueprint(app)	# 注册蓝图
	# # 启动连接池
	print('连接池:',pool)
	return app

# 注册蓝图对象到核心对象app上
def register_blueprint(app):
	from app.web import web
	app.register_blueprint(web)