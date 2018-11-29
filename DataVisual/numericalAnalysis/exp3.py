import numpy as np
import matplotlib.pyplot as plt
import math
from matplotlib.patches import Polygon

I = -12.0703463164
a,b = 0,math.pi
h = b - a
n = 1

f = lambda x: math.exp(x) * math.cos(x)
T2n = lambda tn,hn: 0.5*(tn+hn)

def Hn(h):
    res = 0
    for i in range(1,n+1):
        res = res + f(a + ((2*i-1)*h)/2 )
    return res*h

def Sigma(n):
    res = 0
    for k in range(1,n):
        res = res + f(a+k*h)
    return 2*res

Tn = (h/2) * (f(a)  + f(b))
while True:
    temp = T2n(Tn,Hn(h))
    print(temp,Tn,abs(temp - Tn),n)
    n = 2*n
    h = h/2
    if abs(temp - Tn) <  0.000001:
        break
    Tn = temp

print(temp,Tn,abs(temp - Tn),n)
print("---------------END------------------")
print(n/2)
print(Tn)

x = np.linspace(0,math.pi,200)
x = list(x)
y = []
for i in x:
    y.append(f(i))

fig,ax=plt.subplots(figsize=(8,5))
plt.plot(x,y,'r',linewidth=2)
# gca = 'get current axis'
# ax = plt.gca()

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

plt.xlim(xmin = 0)
# 表示积分的区域
verts=[(a,0)]+list(zip(x,y))+[(b,0)]
# 表示使用Polygon函数填充积分区域的面积,表面颜色是0.7,边沿颜色是0.5
poly=Polygon(verts,facecolor='0.7',edgecolor='0.5')
# 表示将填充的面积添加到图表中
ax.add_patch(poly)
# 表示在(0.5*(a+b),1)的位置给图表添加一个积分公式,字体是20,积分上下限为a~b,函数是f(x),而horizontalalignment='center'表示水平居中对齐
plt.text(2,20,r"$\int_a^b f(x)\mathrm{d}x$", horizontalalignment='center',fontsize=20)

# 分别表示给X轴和Y轴添加标签
plt.figtext(0.9,0.075,'$x$')
plt.figtext(0.075,0.9,'$f(x)$')
# 表示X轴刻度的位置
ax.set_xticks((a,b))
# 表示X轴刻度位置放置的标签内容
ax.set_xticklabels(('','$b$'))
# 表示Y轴刻度的位置
# ax.set_yticks([f(a),f(b)])
# 表示X轴刻度的位置
ax.set_xticks([a,b])
# 表示Y轴刻度位置放置的标签内容
# ax.set_yticklabels(('$f(a)$','$f(b)$'))
# 表示给图表添加网格
# plt.grid(True)

plt.show()
