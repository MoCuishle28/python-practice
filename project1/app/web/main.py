from flask import render_template, request, url_for, session, redirect, flash
from . import web
from app.models.book import Book
from app.models.user import User
from app.models.gift import Gift
from app.models.wish import Wish
from app.models.drift import Drift
from werkzeug.security import generate_password_hash, check_password_hash


@web.route('/')
def index():
	username = ''
	bookList = Book.find_all()
	# 测试一下带条件的
	# book = Book.find_all(title='解忧杂货店', id='79', isbn='25862578')
	# print(book)
	if session.get('username'):
		username = session.get('username')
	return render_template('index.html', bookList=bookList[:38], username=username)


@web.route('/register', methods=['GET','POST'])
def register():
	msg = ''
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')
		password = generate_password_hash(password)		# hash加密
		nickname = request.form.get('nickname')
		address = request.form.get('address')
		phone = request.form.get('phone')
		email = request.form.get('email')

		if User.valid_user(username):
			msg = "该账号已经存在"
			return render_template('register.html', msg = msg)
		if User.valid_nickname(nickname):
			msg = '该昵称已经存在'
			return render_template('register.html', msg = msg)
		new_user = User(username, password, nickname, address, phone, email)
		new_user.insert()
		return redirect(url_for('web.login'))
	return render_template('register.html')


@web.route('/login', methods=['GET', 'POST'])
def login():
	msg = ''
	if request.method == 'POST':
		form = request.form
		username = form.get('username')
		password = form.get('password')
		ret = User.valid_user(username)
		if ret and User.check_password(username, password):
			# 操作session 浏览器与服务器的一次会话
			session['username'] = username
			# session permanent 持久化置为True则session课保存31天.
			# session.permanent = True
			return redirect(url_for('web.index'))	
		msg = '登录失败!'
	return render_template('login.html', msg = msg)


@web.route('/detil/<book_id>', methods=['POST', 'GET'])
def detil(book_id):
	message = ''
	book = Book.find_all(id=book_id)	# 返回一个列表 每个元素是字典
	if book:
		# 拿到相关用户id nickname
		giftList = Gift.get_giftInfo(book_id)
		wishList = Wish.get_wishInfo(book_id)
	book = book[0]
	username = session.get('username')

	if request.method=='POST':
		# 要把这本书作为礼物
		user = User.find_oneID_by_username(username)
		user_id = user[0]

		if 'give_book' in request.form:
			if not is_your_gitf(giftList, user_id):
				# 如果该用户已经把这书添加到礼物 则返回已经添加
				message = '已经添加过了'
				return render_template('detil.html', book=book, username=username, giftList=giftList, wishList=wishList, message=message)

			# 要添加到礼物 则该书本不能是这个用户的未完成心愿
			for wish in wishList:
				if wish.get('user_id') == user_id:
					# 已经是未完成心愿
					message = '此书是你未完成的心愿'
					return render_template('detil.html', book=book, username=username, giftList=giftList, wishList=wishList, message=message)
			# 没添加过则添加该数据到数据库的gift表中
			new_gift = Gift(book_id, user_id, 0)
			new_gift.insert()	# 插入数据
			message = '成功添加到赠送礼物'

		# 要把这本书添加到心愿
		elif 'wish_book' in request.form:
			if not is_your_wish(wishList, user_id):
				# 如果该用户已经把这本书添加到心愿 则返回已经添加
				message = '已经添加过了'
				return render_template('detil.html', book=book, username=username, giftList=giftList, wishList=wishList, message=message)
			if not is_your_gitf(giftList, user_id):
				# 不能是未送出的礼物
				message = '此书是你未送出的礼物'
				return render_template('detil.html', book=book, username=username, giftList=giftList, wishList=wishList, message=message)				
			new_wish = Wish(book_id, user_id, 0)
			new_wish.insert()
			message = '成功添加到你的心愿'

	return render_template('detil.html', book=book, username=username, giftList=giftList, wishList=wishList, message=message)


def is_your_gitf(giftList, user_id):
	for gift in giftList:
		if gift.get('user_id') == user_id:
			print('False')
			return False
	return True


def is_your_wish(wishList, user_id):
	for wish in wishList:
		if wish.get('user_id') == user_id:
			return False
	return True


@web.route('/giftList')
def giftList():
	username = session.get('username')
	if not username:
		return redirect(url_for('web.login'))
	giftList = Gift.get_user_gift_by_username(username)		# 字典
	return render_template('giftList.html', username=username, myList=giftList)


@web.route('/wishList')
def wishList():
	username = session.get('username')
	if not username:
		return redirect(url_for('web.login'))
	wishList = Wish.get_user_wish_by_username(username)		# 字典
	return render_template('wishList.html', username=username, myList=wishList)


@web.route('/driftList')
def driftList():
	username = session.get('username')
	if not username:
		return redirect(url_for('web.login'))
	user_id = User.find_oneID_by_username(username)[0]
	giver_list = Drift.get_giver_drift(user_id)
	recipient_list = Drift.get_recipient_id_drift(user_id)
	return render_template('driftList.html', username=username, giver_list=giver_list, recipient_list=recipient_list)


@web.route('/ok', methods=['POST','GET'])
def ok():
	# 在drift list 下同意请求
	if request.method=='POST':
		username = session.get('username')
		if not username:
			return redirect('web.login')
		uid = User.find_oneID_by_username(username)[0]	# 找到送礼人id
		if 'ok' in request.form:
			print(request.form)
			if Drift.update(request.form.get('drift_id'), 'status', '待寄出'):
				print(Gift.update(uid, 'launched', '1', request.form.get('book_id')))
		else:
			drift_id = request.form.get('drift_id')
			drift = Drift.find_drift_by_ID(drift_id)
			rec_id = drift.get('recipient_id')
			Wish.update('launched', '0', 'user_id', rec_id, drift.get('book_id'))
			Drift.update(drift_id, 'status', '已拒绝')
	return redirect(url_for('web.driftList'))


@web.route('/requestBook', methods=['POST','GET'])
def requestBook():
	# 请求书籍
	print('========================REQUEST======================')
	print(request.form)
	username = session.get('username')
	if not username:
		return redirect(url_for('web.login'))
	user = User.find_user_by_username(username)[0]	# 接收者
	drift = Drift(request.form.get('giver_id'), user.get('id'), request.form.get('book_id'), user.get('address'), '待处理')
	if Drift.valid_drift(request.form.get('giver_id'), user.get('id'), request.form.get('book_id')):
		return redirect(url_for('web.index'))
	elif drift.insert():
		if not Wish.valid_wish_exists(drift.book_id, drift.recipient_id):
			# 如果还没有wish
			wish = Wish(drift.book_id, drift.recipient_id, 0)
			print(wish.insert())
		print(Wish.update('launched', 1, 'user_id', user.get('id'), request.form.get('book_id')))
	return redirect(url_for('web.driftList'))


@web.route('/giveBook', methods=['POST','GET'])
def giveBook():
	# 赠予书籍
	print('========================GIVE======================')
	print(request.form)
	username = session.get('username')
	if not username:
		return redirect(url_for('web.login'))
	user = User.find_user_by_username(username)[0]	# 赠送者
	drift = Drift(user.get('id'), request.form.get('rec_id'), request.form.get('book_id'), user.get('address'), '待签收')
	if Drift.valid_drift(user.get('id'), request.form.get('rec_id'), request.form.get('book_id')):
		return redirect(url_for('web.index'))
	elif drift.insert():
		if not Gift.valid_gift_exists(drift.book_id, drift.giver_id):
			# 插入
			gift = Gift(drift.book_id, drift.giver_id, 0)
			print(gift.insert())
		print(Wish.update('launched', 1, 'user_id', request.form.get('rec_id'), request.form.get('book_id')))
		print(Gift.update(user.get('id'), 'launched', '1', request.form.get('book_id')))
	return redirect(url_for('web.driftList'))


@web.route('/del_gift/<isbn>')
def del_gift(isbn):
	username = session.get("username")
	if not username:
		redirect(url_for('web.login'))
	retDel = Gift.delete_by_ISBN(isbn)
	return redirect(url_for('web.giftList'))


@web.route('/del_wish/<isbn>')
def del_wish(isbn):
	username = session.get("username")
	if not username:
		redirect(url_for('web.login'))
	retDel = Wish.delete_by_ISBN(isbn)
	return redirect(url_for('web.wishList'))


@web.route('/personal')
def personal():
	username = session.get('username')
	if not username:
		return redirect(url_for('web.login'))
	user = User.find_user_by_username(username)[0]
	# print(user)
	return render_template('personal.html', username=username, user=user)


@web.route('/changeInfo', methods=['POST', 'GET'])
def changeInfo():
	user = User(request.form.get('username'), request.form.get('password'), request.form.get('nickname'), 
		request.form.get('address'), request.form.get('phone'), request.form.get('email'))
	print(user.update())
	return redirect(url_for('web.index'))


@web.route('/exit')
def exit():
	# 退出
	session['username'] = None
	return redirect(url_for('web.index'))