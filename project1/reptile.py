"""
写个爬虫 从豆瓣爬去图书信息
"""
import requests
from bs4 import BeautifulSoup
import time
import MySQLdb


class Book(object):
	def __init__(self, title, author, publisher, isbn, summary, image):
		# self.id = _id
		self.title = title
		self.author = author
		self.publisher = publisher
		self.isbn = isbn
		self.summary = summary
		self.image = image

	def insert(self, conn):
		# 插入数据库操作
		try:
			sql = """insert into `book` (`title`, `author`, `publisher`, `isbn`, `summary`, `image`)
					 values (%s, %s, %s, %s, %s, %s);"""
			cursor = conn.cursor()
			cursor.execute(sql, 
				(self.title, self.author, self.publisher, self.isbn, self.summary, self.image, ))
			conn.commit()
		except Exception as e:
			print(e, self.title)
			conn.rollback()	# 一条sql失败 则全部都不会提交


	def __str__(self):
		return self.title + ' ' + self.author + ' '+ self.isbn + '...'



def getHTML(url, code='utf-8'):
	try:
		r = requests.get(url,timeout = 30)
		r.raise_for_status()
		r.encoding = code
		return r.text
	except:
		return ""


def getBookList(url, bookList):
	html = getHTML(url)
	soup = BeautifulSoup(html, "html.parser")
	items = soup.find_all('div', 'info')
	li = soup.find_all('li', 'subject-item')
	for item in li:
		img = item.find('img')
		a = item.find_all('a')				# 包含isbn 和 title的a标签
		pub = item.find('div', 'pub')		# 包含出版社的标签
		p = item.find('p')					# 包含简介的标签简介
		try:
			title = a[1]['title']			# 提取title

			s = pub.string.strip()
			arr_s = s.split('/')
			author = ''
			publisher = '未知'
			for i in arr_s:
				if '出版' in i:
					publisher = i			# 出版社
					break
				else:
					author += ' '+i 		# 作者

			link = a[0].attrs['href']
			summary = p.string				# 内容摘要
			isbn = link.split('/')[-2]		# 提取isbn
			img = img.attrs['src']			# 提取图片url
			# 放入链表
			book = Book(title, author, publisher, isbn, summary, img)
			bookList.append(book)
		except:
			continue


def main():
	url = "https://book.douban.com/tag/小说?start={}&type=T"
	start = 0
	bookList = []

	while start<=60:
		getBookList(url.format(start), bookList)
		start += 20
		time.sleep(0.5)	# 休眠一下 不频繁访问
	print(len(bookList))

	# 已经完成
	# # 先要连接数据库
	# try:
	# 	conn = MySQLdb.connect(
	# 				host='127.0.0.1',
	# 				port=3306,
	# 				user='test',
	# 				passwd='123456',
	# 				db='zonda',
	# 				charset='utf8'
	# 			)
	# except MySQLdb.Error as e:
	# 		print('Error: %s' % e)
	# # 插入MySQL数据库
	# for book in bookList:
	# 	book.insert(conn)
	# conn.close()


if __name__ == '__main__':
	main()