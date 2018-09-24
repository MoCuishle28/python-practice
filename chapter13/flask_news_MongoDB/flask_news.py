from flask import Flask, render_template
from flask_mongoengine import MongoEngine, first_or_404
from datetime import datetime


app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'learn',
    'host': '127.0.0.1',
    'port': 27017
}
db = MongoEngine(app)


NEWS_TYPES = (
	('推荐','推荐'),
	('本地','本地')
)


class News(db.Document):
	ID = db.Column('id', db.Integer, primary_key=True)
	title = db.StringField(required=True, max_length=200)
	content = db.StringField(required=True, choices=NEWS_TYPES)
	news_type = db.StringField(required=True)
	img_url = db.StringField()
 	is_valid = db.BooleanField(default=True)
 	created_at = db.DateTimeField(default=datetime.now())
 	updated_at = db.DateTimeField(default=datetime.now())	# 最后编辑时间
	# 还可以扩展 比如加上评论

	meta = {
		'collection':'news',
		'ordering':['-created_at']
	}

	def __repr(self):	# 打印的内容 类似__str__
		return '<News %r>'%self.title


@app.route('/')
def index():
	'''首页'''
	news_list = News.objects.all()
	return render_template('index.html', news_list=news_list)


@app.route('/cat/<name>/')
def cat(name):
	'''类别'''
	# 查询类别为name的新闻
	news_list = News.objects.filter(is_valid=True, news_type=name)
	return render_template('cat.html', name=name, news_list=news_list)


@app.route('/detail/<pk>/')
def detail(pk):
	'''新闻详情'''
	new_obj = News.objects.first_or_404(pk=pk)
	return render_template('detail.html', pk=pk, new_obj=new_obj)

if __name__ == '__main__':
	app.run(debug=True)