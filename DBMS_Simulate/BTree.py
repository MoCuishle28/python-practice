'''
B+ 数
'''
import json


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
		self.fill_factory = self.rank//2	# 填充因子 (大于时能够借用, 小于时需要合并)


	def search_by_node(self, field):
		'''
		return:		list -> [index1, index2, ...]
		'''
		curr_node = self.root
		ret = []
		while not curr_node.is_leaf():
			go = 0
			for v in curr_node.value:
				if v > field:
					break
				go += 1
			curr_node = curr_node.point[go]
		if field in curr_node.value:
			index = curr_node.value.index(field)
			ret = curr_node.index[curr_node.value[index]]
		return ret.copy()


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


	def delete(self, element):
		if len(element) != 2 or element[0] not in self.link_index or element[1] not in self.link_index.get(element[0],[]):
			return False
		field, index = element
		curr_node = self.root
		node_stack = []
		replace_node = None 	# 需要被替代key的节点
		while not curr_node.is_leaf():
			node_stack.append(curr_node)
			go = 0
			for v in curr_node.value:
				if v > field:
					break
				elif v == field:
					replace_node = curr_node
				go += 1
			curr_node = curr_node.point[go]

		if len(curr_node.index[field]) > 1:		# key对应多个index
			curr_node.index[field].remove(index)
			self.link_index[field].remove(index)
		else:
			curr_node.value.remove(field)
			del curr_node.index[field]
			self.link_value.remove(field)
			del self.link_index[field]

		if len(curr_node.value) >= self.fill_factory:	# (1).删除后还满足填充因子(有可能有多条记录 只删了一条)
			if field not in self.link_index and replace_node and field in replace_node.value:	# 已经彻底删除了
				replace_node.value[replace_node.value.index(field)] = curr_node.value[0]
			return True
		elif node_stack:					# 删除后不满足填充率 并且有父节点
			pre_node = node_stack.pop()		# 父节点
			bro_node = None
			for i,point in enumerate(pre_node.point):	# 找到兄弟节点
				if point == curr_node:
					if i-1 >= 0 and len(pre_node.point[i].value) > self.fill_factory:
						bro_node = pre_node.point[i-1]
					elif i+1 < len(pre_node.point) and len(pre_node.point[i+1].value) > self.fill_factory:
						bro_node = pre_node.point[i+1]
					else:
						bro_node = pre_node.point[i-1] if i-1 >= 0 else pre_node.point[i+1]
					break

			if len(bro_node.value) > self.fill_factory:	# (2).如果兄弟节点有富足
				if pre_node.point.index(bro_node) < pre_node.point.index(curr_node):	# 如果兄弟是左节点
					# 借左边最大的key 及其对应行号
					borrow_key = bro_node.value.pop()
					if bro_node.is_leaf():
						borrow_index = bro_node.index[borrow_key]
						del bro_node.index[borrow_key]
					curr_node.value.insert(0, borrow_key)
					curr_node.index[borrow_key] = borrow_index
					pre_node.value[pre_node.point.index(curr_node) - 1] = borrow_key	# 替换父节点的key(bro and curr 之间的)
				elif pre_node.point.index(bro_node) > pre_node.point.index(curr_node):	# 如果兄弟是右节点
					# 借右边最小的key 及其对应行号
					borrow_key = bro_node.value.pop(0)
					if bro_node.is_leaf():
						borrow_index = bro_node.index[borrow_key]
						del bro_node.index[borrow_key]
					curr_node.value.append(borrow_key)
					curr_node.index[borrow_key] = borrow_index
					pre_node.value[pre_node.point.index(curr_node)] = bro_node.value[0]
				if replace_node and replace_node != pre_node and field in replace_node.value:
					replace_node.value[replace_node.value.index(field)] = curr_node.value[0]	# 修改上面索引节点中被删除的key
			else:											# (3).兄弟节点没有富足
				# 合并兄弟节点和当前节点
				for key in bro_node.value:
					curr_node.value.append(key)
					curr_node.index[key] = bro_node.index[key]
				curr_node.value.sort()	# 调整为升序的
				# 删除父节点的key(bro and curr 之间)
				if pre_node.point.index(bro_node) < pre_node.point.index(curr_node):	# 如果兄弟是左节点
					pre_node.value.pop(pre_node.point.index(curr_node)-1)
				else:	# 否则兄弟是右节点
					pre_node.value.pop(pre_node.point.index(curr_node))
				pre_node.point.remove(bro_node)		# 合并完毕
				if replace_node and field in replace_node.value:	# 修改上面索引节点中被删除的key
					replace_node.value[replace_node.value.index(field)] = curr_node.value[0]

				if pre_node == self.root and pre_node.value == []:
					self.root = curr_node
					return True

				curr_node = pre_node
				if len(curr_node.value) >= self.fill_factory:	# (4).若索引节点满足填充因子
					return True
				elif node_stack:		# 索引不满足填充因子 且还有父节点
					pre_node = node_stack.pop()
					bro_node = None
					for i,point in enumerate(pre_node.point):	# 找到兄弟节点
						if point == curr_node:
							if i-1 >= 0 and len(pre_node.point[i].value) > self.fill_factory:
								bro_node = pre_node.point[i-1]
							elif i+1 < len(pre_node.point) and len(pre_node.point[i+1].value) > self.fill_factory:
								bro_node = pre_node.point[i+1]
							else:
								bro_node = pre_node.point[i-1] if i-1 >= 0 else pre_node.point[i+1]
							break

					if len(bro_node.value) > self.fill_factory:		# (5).如果兄弟节点有富足
						# 将兄弟节点的子树移动到当前节点 且兄弟节点的key借一个给父节点
						if pre_node.point.index(bro_node) < pre_node.point.index(curr_node):	# 如果兄弟是左节点
							curr_node.point.insert(0, bro_node.point.pop())
							curr_node.value.insert(0, pre_node.value.pop())		# 父节点key 下移
							pre_node.value.insert(pre_node.point.index(bro_node), bro_node.value.pop())
						else:																	# 兄弟节点是右节点
							curr_node.point.append(bro_node.point.pop(0))
							curr_node.value.append(pre_node.value.pop(0))	# 父节点key 下移
							pre_node.value.insert(pre_node.point.index(curr_node), bro_node.value.pop(0))
					else:		# (6).兄弟节点不满足填充因子
						# 当前节点和兄弟节点以及父节点向下移动一个key组成新节点
						# 如果父节点有富足 应该是父节点落下一个key 而不是直接和父节点合并
						if len(pre_node.value) > self.fill_factory:
							if pre_node.point.index(bro_node) < pre_node.point.index(curr_node):	# 如果兄弟是左节点
								new_key = pre_node.value.pop(pre_node.point.index(bro_node))
								bro_node.value.append(new_key)
								for point in curr_node.point:
									bro_node.point.append(point)
								for key in curr_node.value:
									bro_node.value.append(key)
								pre_node.point.remove(curr_node)
							else:																	# 兄弟节点是右节点
								new_key = pre_node.value.pop(pre_node.point.index(curr_node))
								bro_node.value.insert(0, new_key)
								for point in curr_node.point[::-1]:
									bro_node.point.insert(0, point)
								for key in curr_node.value[::-1]:
									bro_node.value.insert(0, key)
								pre_node.point.remove(curr_node)
						else:
							if pre_node.point.index(bro_node) < pre_node.point.index(curr_node):	# 如果兄弟是左节点
								# curr_node与父节点合并
								for key in curr_node.value:
									pre_node.value.append(key)
								pre_node.point.remove(curr_node)
								for node in curr_node.point:
									pre_node.point.append(node)
								# 兄弟节点与父节点合并
								for key in bro_node.value[::-1]:
									pre_node.value.insert(0, key)
								pre_node.point.remove(bro_node)
								for node in bro_node.point[::-1]:
									pre_node.point.insert(0, node)
							else:																	# 兄弟节点是右节点
								# curr_node与父节点合并
								for key in curr_node.value[::-1]:
									pre_node.value.insert(0, key)
								pre_node.point.remove(curr_node)
								for node in curr_node.point[::-1]:
									pre_node.point.insert(0, node)
								# 兄弟节点与父节点合并
								for key in bro_node.value:
									pre_node.value.insert(0, key)
								pre_node.point.remove(bro_node)
								for node in bro_node.point:
									pre_node.point.append(node)
				else:	# 索引不满足填充因子 且没有父节点(即已经是root节点)
					pre_node = curr_node
		return True


	def search_by_dict(self, filed):
		return self.link_index.get(filed, []).copy()


	def save(self, path):
		with open(path + '.index', 'w') as f:
			json.dump(self.link_index, f)
		return True


	def load(self, path):
		with open(path+'.index', 'r') as f:
			d = json.load(f)
		for k,v in d.items():
			key = int(k) if k.isnumeric() else k
			for index in v:
				self.insert([key,index])
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
		print(self.link_index)


if __name__ == '__main__':
	# 测试
	b_plus_tree = B_Plus_Tree(3)
	b_plus_tree.insert([3,0])
	b_plus_tree.insert([8,1])
	b_plus_tree.insert([12,2])
	b_plus_tree.insert([1,4])
	b_plus_tree.insert([16,3])
	# b_plus_tree.insert([8,5])
	b_plus_tree.insert([22,6])
	b_plus_tree.insert([28,7])
	b_plus_tree.insert([30,8])
	b_plus_tree.show()

	print('---删除测试---')
	delete_element = [22, 6]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()
	print('---朴实的分割线---')
	delete_element = [8, 1]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()

	print('---朴实的分割线---')
	delete_element = [12, 2]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()

	print('---朴实的分割线---')
	delete_element = [28, 7]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()

	print('---朴实的分割线---')
	delete_element = [16, 3]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()

	print('====================================')

	print('---朴实的分割线---')
	delete_element = [3, 0]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()

	print('---朴实的分割线---')
	delete_element = [30, 8]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()

	print('---朴实的分割线---')
	delete_element = [1, 4]
	print('delete', delete_element ,b_plus_tree.delete(delete_element))
	b_plus_tree.show()

	print('---朴实的分割线---')
	print('search_by_node:',8, b_plus_tree.search_by_node(8))
	print(28, b_plus_tree.search_by_node(28))
	print(3, b_plus_tree.search_by_node(3))

	print('---朴实的分割线---')
	# print(b_plus_tree.save('test_json'))
	# tmp = B_Plus_Tree(3)
	# tmp.load('test_json')
	# tmp.show()

	b_plus_tree = B_Plus_Tree(3)
	i = 0
	while True:
		field = input('>')
		oper, field = field.split()
		if oper == 'in':
			field = int(field)
			b_plus_tree.insert([field, i])
			i+=1
		elif oper == 'del':
			field = int(field)
			index = b_plus_tree.search_by_dict(field)
			if index:
				print('del:',field, index)
				print(b_plus_tree.delete([field, index.pop(0)]))
			else:
				print('don\'t')
		elif oper == 'exit':
			break
		b_plus_tree.show()