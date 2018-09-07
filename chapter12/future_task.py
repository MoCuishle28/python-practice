# Future 结果容器 

# Task 是future的子类 是协程与future的桥梁	用于解决协程 线程 的不一致
# 1.激活协程
# 2.在协程返回抛出StopIteration异常时 接收返回值并处理异常