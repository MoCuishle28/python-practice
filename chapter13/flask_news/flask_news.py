from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://test:123456@localhost:3306/mydatabase?charset=utf8'
db = SQLAlchemy(app)


class News(db.Model):
	__tablename__ = 'news'
	ID = db.Column('id', db.Integer, primary_key=True)
	title = db.Column(db.String(200), nullable=False)
	content = db.Column(db.String(2000), nullable=False)
	types = db.Column(db.String(10), nullable=False)
	image = db.Column(db.String(300))
	author = db.Column(db.String(20))
	view_count = db.Column(db.Integer, default=0)			     # 浏览次数
	created_at = db.Column(db.DateTime)
	is_valid = db.Column(db.Boolean, default=True)

	def __repr(self):	# 打印的内容 类似__str__
		return '<News %r>'%self.title


@app.route('/')
def index():
	'''首页'''
	return render_template('index.html')


@app.route('/cat/<name>/')
def cat(name):
	'''类别'''
	# 查询类别为name的新闻
	news_list = News.query.filter(News.types == name)
	return render_template('cat.html', name=name, news_list=news_list)


@app.route('/detail/<int:pk>/')
def detail(pk):
	'''新闻详情'''
	new_obj = News.query.get(pk)
	return render_template('detail.html', pk=pk, new_obj=new_obj)

if __name__ == '__main__':
	app.run(debug=True)