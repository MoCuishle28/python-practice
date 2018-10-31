学习Python时的实验代码

chapter01： 一切皆是对象

chapter02：	魔法函数

chapter03：	python的类 上下文管理器

chapter04：	序列类型

chapter05：	dict和set

chapter06：	python变量的实际 垃圾回收

chapter07：	元类编程 ORM

chapter08：	生成器

chapter09：	socket

chapter10： 多线程 多进程

chapter11：	同步 异步 并发 select技术 以及yield from

chapter12：	aiohttp	(用到的包 aiohttp, aiomysql, pyquery)

chapter13: 	数据库操作练习 包括MySQL, MongoDB, Redis 
			用到的包: mysqlclient 
					 flask, Flask-SQLAlchemy	文档：	Flask https://dormousehole.readthedocs.io/en/latest/
														Flask-SQLAlchemy http://www.pythondoc.com/flask-sqlalchemy/quickstart.html
					 mongoengine(依赖pymongo)  	文档：	pymongo http://api.mongodb.com/python/current/  
														mongoengine http://docs.mongoengine.org/tutorial.html
					 flask-mongoengine			文档： 	https://flask-mongoengine.readthedocs.io/en/latest/	(依赖 mongoengine)
					 
project1:	数据库应用 写一个赠送图书的网站zonda  
			用到的包: 
				Flask
				requests
				beautifulsoup4					文档(中文): 	https://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/

DBMS_Simulate:	模拟一个DBMS（缺少sql编译系统）
				完成常规的sql操作 如：create, alter, drop, insert, delete, select ...
				完成索引的添加 (add index)

解决包安装失败网址 : http://www.lfd.uci.edu/~gohlke/pythonlibs/