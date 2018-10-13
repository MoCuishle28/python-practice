from flask import render_template, request, url_for, session, redirect
from . import web
from app.models.book import Book
from app.models.user import User


@web.route('/')
def index():
	bookList = Book.find_all()
	# 测试一下带条件的
	# book = Book.find_all(title='解忧杂货店', id='79', isbn='25862578')
	# print(book)
	return render_template('index.html', bookList=bookList[:38])


@web.route('/register', methods=['GET','POST'])
def register():
	return render_template('register.html')


@web.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		form = request.form
		username = form.get('username')
		password = form.get('password')
		ret = User.valid_user(username)
		if ret and ret[1] == password:
			return redirect(url_for('web.index'))	
		msg = '登录失败!'
		# 操作session
		# session[username] = username
    	# session permanent 持久化置为True则session课保存31天.
	    # session.permanent = True
	return render_template('login.html', msg = msg)


@web.route('/detil')
def detil():
	pass