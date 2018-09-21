from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Boolean

# root 用户  后面是密码  mydatabase是数据库名称
engine = create_engine('mysql://test:123456@localhost:3306/mydatabase?charset=utf8')
Base = declarative_base()

class News(Base):
	__tablename__ = 'news_test'
	ID = Column('id', Integer, primary_key=True)
	title =  Column(String(200), nullable=False)
	content = Column(String(2000), nullable=False)
	types = Column(String(10), nullable=False)
	image = Column(String(300))
	author = Column(String(20))
	view_count = Column(Integer, default=0)			     # 浏览次数
	created_at =  Column(DateTime)
	is_valid = Column(Boolean, default=True)

