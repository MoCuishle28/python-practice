'''
B+ 数
'''


class Leaf(object):
	'''叶节点'''
	def __init__(self, rank):
		self.rank = rank
		self.block_index = []	# 盘块(每个元素为 [field, index1, index2] 列表 )
	

	def isFull(self):
		return len(self.block_index) >= self.rank


class Index(object):
	'''索引节点'''
	def __init__(self, rank):
		self.rank = rank
		self.index = []		# 索引域
		self.point = [Leaf(rank) for _ in range(rank)]		# 指针域


	def insert(self, element):
		pass


	def isFull(self):
		return len(self.index) >= self.rank


	def have_leaf(self):
		'''
		判断是否有叶节点:
			if 		指针域为Leaf then 有待插入的叶节点
			else 	指针域指向索引节点
		'''
		return True if type(self.point[0]) is Leaf else False


class B_Plus_Tree(object):
			
	def __init__(self, rank):
		self.rank = rank				# 秩(一个叶节点能存的元素个数 + 1)
		self.index_page = Index(rank)	# 索引节点
		self.link = []					# 所有叶节点


	def insert(self, element):
		'''
		element:	is a list with 2 element, 0 is a field and 1 is a index of file
		return:		是否插入成功 (bool)
		'''
		if type(element) is not list or len(element) != 2:
			return False
		field = element[0]
		target_index_page = self.index_page

		if self.index_page.index == []:		# 直接插入
			self.index_page.index.append(field)
			self.index_page.point[0].block_index.append(element)
			return True

		tar_list = []
		if not target_index_page.have_leaf():	# 找到有叶的索引节点
			tar_list, target_index_page = self.search(field)	# 第二个返回值为目标叶节点的前一个索引节点

		if tar_list:
			tar_list.append(element[-1])	# 直接插入
		else:
			goto = 0
			for v in target_index_page.index:
				if v > field:
					break
				goto += 1
			leaf = target_index_page[goto]
			have_inserted = False
			for i,v in enumerate(leaf):
				if v[0] > field:
					leaf.insert(i, element[-1])
					have_inserted = True
					break
			if not have_inserted:
				leaf.append(element[-1])

		# TODO 调整B+树


	def modify_tree(self):
		pass


	def search(self, field):
		'''
		field:		字段名
		return:		目标列表, 目标叶节点前一个索引节点
		'''
		if self.index_page == []:
			return None, None
		curr_index_page = self.index_page

		while not curr_index_page.have_leaf():
			goto = 0
			for v in curr_index_page.index:
				if v > field:
					break
				goto += 1
			curr_index_page = curr_index_page.point[goto]

		goto = 0
		for v in curr_index_page.index:
			if v > field:
				break
			goto += 1

		leaf = curr_index_page.point[goto]
		tar_list = []
		for i,v_list in enumerate(leaf):
			if v_list[0] == field:
				tar_list = v_list
				break

		return tar_list, curr_index_page


	def show(self):
		curr_index_page = self.index_page
		queue = []
		


if __name__ == '__main__':
	# 测试
	b_plus_tree = B_Plus_Tree(3)
	print(b_plus_tree.index_page.have_leaf())	# Test
