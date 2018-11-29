import matplotlib.pyplot as plt
import numpy as np

# 生成-1到1的50个点
x = np.linspace(-1,1,50)
print(x)
y = 2*x + 1
z = x**2

# plt.plot(x,y)
# plt.show()
# plt.plot(x,z)
# plt.show()

"""每个figure对应一张图片"""
# num:标号,figsize:窗口大小
# plt.figure(num=0,figsize=(3,5))
# plt.plot(x,y)
# plt.figure(num=1,figsize=(6,6))
# plt.plot(x,z)
# 再创建一个figure,放两条线
plt.figure()
l1, = plt.plot(x,z,label = 'a')# 返回时要加,
l2, = plt.plot(x,y,color='red',linewidth=1.0,linestyle='--',label = 'b')

# 打印出线条l1,l2的名字'aaa'和'bbb'
plt.legend(handles = [l1,l2],labels = ['aaa','bbb'],loc = 'best')
# 控制坐标轴范围
plt.xlim((-1,2))
plt.ylim((-2,3))
# 坐标轴标签
plt.xlabel("I am X")

new_ticks = np.linspace(-1,2,5)
print("------------------------------------------------------------")
print(new_ticks)
# 改变了x轴的间隔大小
plt.xticks(new_ticks)
# 在y轴指定位置上加上描述(加r'$...$'可让字体好看)(\加上alpha可得到数学符号α)
plt.yticks([-2,-1.8,-1,1.22,3],[r'$very\ bad$',r'$bad\ \alpha$','normal','good','very good'])

# gca = 'get current axis'
ax = plt.gca()
# spines脊梁,即图的四条框(none即没有)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 设置x,y为那两条边框(这里x为下边框)
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
# x轴data(值)0时为原点
ax.spines['bottom'].set_position(('data',0))
# y轴data(值)0时为原点
ax.spines['left'].set_position(('data',0))
plt.show()
