from threading import Condition
# 条件变量(最复杂的同步锁) 用于复杂的线程间同步
import threading

class XiaoAi(threading.Thread):
	def __init__(self, cond):
		super().__init__(name="小爱")
		self.cond = cond

	def run(self):
		with self.cond:
			self.cond.wait()
			print("{}:在".format(self.name))
			self.cond.notify()

			self.cond.wait()
			print("{}:好啊".format(self.name))
			self.cond.notify()

			self.cond.wait()
			print("{}:岂因福祸避趋之".format(self.name))


class TianMao(threading.Thread):
	def __init__(self, cond):
		super().__init__(name="天猫精灵")
		self.cond = cond

	def run(self):
		with self.cond:
			print("{}:小爱同学".format(self.name))
			self.cond.notify()

			self.cond.wait()
			print("{}:我们来念诗吧".format(self.name))
			self.cond.notify()

			self.cond.wait()
			print("{}:苟利国家生死以".format(self.name))
			self.cond.notify()


if __name__ == '__main__':
	cond = Condition()
	xiaoai = XiaoAi(cond)
	tianmao = TianMao(cond)

	# 如果使用lock来完成协调读诗 可能会导致小爱还没start 天猫精灵就已经不断地申请，释放锁以完成所有操作了
	xiaoai.start()	# 要先启动小爱	若先启动天猫，在第一次notify之后 小爱还没开始 所以会两者都一直处于wait 死锁
	tianmao.start()