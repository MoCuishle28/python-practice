'''
B+ 数
'''


class Node(object):
	'''节点'''
	def __init__(self, rank):
		self.rank = rank	# 秩 (每个节点包含值的个数)
		self.value = []		# 值域	每个元素为 field
		self.index = {}		# 用于找到field对应的index    key:value -> field:[index1, index2, ...]
		self.point = []		# 指针域


	def is_leaf(self):
		return self.point == []


	def is_full(self):
		return len(self.value) >= self.rank


	def insert_element(self, element):
		'''插入当前节点'''
		if type(element) is not list or len(element) != 2:
			return False
		field, index = element
		tar_i = 0
		for v in self.value:
			if v > field:
				break
			elif v == field:
				tar_i = -1
				break
			tar_i += 1

		if tar_i == -1:	# 原来已经有
			self.index[field].append(index)
		else:
			self.value.insert(tar_i, field)
			self.index[field] = [index]
		return True


class B_Plus_Tree(object):

	def __init__(self, rank):
		self.rank = rank
		self.root = Node(rank)
		self.link_value = []	# 线性存储索引
		self.link_index = {} 


	def _split_node(self, node_stack, curr_node):
		'''
		node_stack:		节点栈, 找到当前节点所走过的节点
		curr_node:		当前节点
		'''
		if node_stack == [] and curr_node.is_leaf() and curr_node == self.root:
			curr_node_len = len(curr_node.value)
			left_list, right_list = curr_node.value[:curr_node_len//2], curr_node.value[curr_node_len//2:]	# 拆分
			middle_value = curr_node.value[curr_node_len//2]
			curr_node.value.clear()
			curr_node.value.append(middle_value)

			left_node = Node(self.rank)
			right_node = Node(self.rank)
			left_node.value = left_list
			right_node.value = right_list

			for v in left_node.value:
				left_node.index[v] = curr_node.index[v]
			for v in right_node.value:
				right_node.index[v] = curr_node.index[v]
			curr_node.index.clear()
			curr_node.point.append(left_node)
			curr_node.point.append(right_node)
		elif node_stack != [] and curr_node.is_leaf():
			left_node = Node(self.rank)
			right_node = Node(self.rank)
			curr_node_len = len(curr_node.value)
			left_node.value, right_node.value = curr_node.value[:curr_node_len//2], curr_node.value[curr_node_len//2:]	# 拆分
			middle_value = curr_node.value[curr_node_len//2]

			# 设置dict
			for v in left_node.value:
				left_node.index[v] = curr_node.index[v]
			for v in right_node.value:
				right_node.index[v] = curr_node.index[v]

			pre_node = node_stack.pop()
			for i,point in enumerate(pre_node.point):
				if point == curr_node:
					pre_node.value.insert(i, middle_value)
					pre_node.point[i] = left_node
					pre_node.point.insert(i+1, right_node)
					break
			if pre_node.is_full():
				self._split_node(node_stack, pre_node)
		elif node_stack == [] and not curr_node.is_leaf() and curr_node == self.root:
			left_node = Node(self.rank)
			right_node = Node(self.rank)
			curr_node_len = len(curr_node.value)
			left_node.value, right_node.value = curr_node.value[:curr_node_len//2], curr_node.value[curr_node_len//2+1:]
			middle_value = curr_node.value[curr_node_len//2]
			for i,point in enumerate(curr_node.point):
				if i <= curr_node_len//2:	# 左半部分给	left_node
					left_node.point.append(point)
				else:						# 右半部分给	right_node
					right_node.point.append(point)
			curr_node.value.clear()
			curr_node.point.clear()
			curr_node.value.append(middle_value)
			curr_node.point.append(left_node)
			curr_node.point.append(right_node)
		elif node_stack and not curr_node.is_leaf() and curr_node != self.root:
			left_node = Node(self.rank)
			right_node = Node(self.rank)
			curr_node_len = len(curr_node.value)
			left_node.value, right_node.value = curr_node.value[:curr_node_len//2], curr_node.value[curr_node_len//2+1:]
			middle_value = curr_node.value[curr_node_len//2]
			for i,point in enumerate(curr_node.point):
				if i <= curr_node_len//2:		# 左半部分给	left_node
					left_node.point.append(point)
				else:							# 右半部分给	right_node
					right_node.point.append(point)

			pre_node = node_stack.pop()
			for i,point in enumerate(pre_node.point):
				if point == curr_node:
					pre_node.value.insert(i, middle_value)
					pre_node.point[i] = left_node
					pre_node.point.insert(i+1, right_node)
					break
			if pre_node.is_full():
				self._split_node(node_stack, pre_node)


	def insert(self, element):
		'''
		element:	每个元素为一个list [field, index]
		'''
		if type(element) is not list or len(element) != 2:
			return False
		field, index = element
		node_stack = []
		curr_node = self.root

		if curr_node.is_leaf():
			curr_node.insert_element(element)
		else:
			while not curr_node.is_leaf():
				go = 0
				for f in curr_node.value:
					if f > field:
						break
					go += 1

				node_stack.append(curr_node)	# 入栈
				curr_node = curr_node.point[go]
			curr_node.insert_element(element)

		if curr_node.is_full():
			self._split_node(node_stack, curr_node)

		go = 0
		for x in self.link_value:
			if x > field:
				break
			elif x == field:
				go = -1
				break
			go += 1
		if go == -1:
			self.link_index[field].append(index)
		else:
			self.link_value.insert(go, field)
			self.link_index[field] = [index]
		return True


	def show(self):
		queue = [self.root]
		while queue:
			curr_node = queue.pop(0)
			if curr_node.is_leaf():
				print(curr_node.index)
			else:
				print(curr_node.value)
			for point in curr_node.point:
				queue.append(point)
		print(self.link_value)


if __name__ == '__main__':
	# 测试
	b_plus_tree = B_Plus_Tree(3)
	b_plus_tree.insert([3,0])
	b_plus_tree.insert([8,1])
	b_plus_tree.insert([12,2])
	b_plus_tree.insert([1,4])
	b_plus_tree.insert([16,3])
	b_plus_tree.insert([8,5])
	b_plus_tree.insert([22,6])
	b_plus_tree.insert([28,7])
	b_plus_tree.insert([30,8])
	b_plus_tree.show()

	b_plus_tree = B_Plus_Tree(3)
	index = 0
	while True:
		field = int(input('>'))
		b_plus_tree.insert([field, index])
		b_plus_tree.show()
		index += 1