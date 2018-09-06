# 通过队列进行线程之间的通信
from queue import Queue # Queue是线程安全的
import time
import threading

def get_detail_html(queue):	# 爬取详情页
	while True:
		url = queue.get()	# 从队尾get一个url 这是一个阻塞的方法 若队列为空 会一直阻塞在这里
		print('get_detail_html started')
		time.sleep(2)
		print('get_detail_html end')

# 爬取到文章的url后 要交给详情页爬取函数爬取详情 所以用到线程间的通信
def get_detail_url(url, queue):	# 爬取列表页
	while True:
		print('get_detail_url started')
		time.sleep(1)
		for i in range(20):	# 假设爬取20个文章url
			queue.put("http://projectsedu.com/{id}".format(id=i))	# 队列满时也会阻塞在这里
		print('get_detail_url end')

if __name__ == '__main__':
	detail_url_queue = Queue(maxsize=1000)
	t1 = threading.Thread(target=get_detail_url, args=("", detail_url_queue))
	for i in range(10):
		t2 = threading.Thread(target=get_detail_html, args=(detail_url_queue))
		t2.start()

	start_time = time.time()
	t1.start()

	print('last time:{}'.format(time.time() - start_time))