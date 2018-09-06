# 线程间的通信
import time
import threading

# from . import variables	# cannot import?
# detail_url_list = []	# 将全局变量放入variables.py里

def get_detail_html(detail_url_list):	# 爬取详情页
	while True:
		print('get_detail_html started')
		if detail_url_list:
			url = detail_url_list.pop()	# 从尾部pop一个url
		time.sleep(2)
		print('get_detail_html end')

def get_detail_url(url, detail_url_list):	# 爬取列表页
	# 爬取到文章的url后 要交给详情页爬取函数爬取详情 所以用到线程间的通信
	while True:
		print('get_detail_url started')
		time.sleep(4)
		for i in range(20):	# 假设爬取20个文章url
			detail_url_list.append("http://projectsedu.com/{id}".format(id=i))
		print('get_detail_url end')

if __name__ == '__main__':
	t1 = threading.Thread(target=get_detail_url, args=("", detail_url_list))
	for i in range(10):
		t2 = threading.Thread(target=get_detail_html, args=(detail_url_list))
		t2.start()

	start_time = time.time()
	t1.start()

	print('last time:{}'.format(time.time() - start_time))
