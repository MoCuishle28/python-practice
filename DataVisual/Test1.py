import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-3,3,50)
y = 2*x + 1

# Test
def fx():
    y = 2 * x + 1
    return y
print(y)
print("==========================================")
print(list(y))
plt.figure(num=1,figsize=(8,5))
# plt.plot(x,y)
plt.plot(x,fx()) #以函数形式传入也可以
# plt.plot(list(y)) #直接一组列表也可以

ax = plt.gca()
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0))
ax.spines['left'].set_position(('data',0))

x0 = 1
y0 = 2*x0 + 1
# scatter画出点
plt.scatter(x0,y0,s=50,color='b')
# 画出从[x0->x0,y0->0]的线,其中k--表示黑色虚线,lw是线宽
plt.plot([x0,x0],[y0,0],'k--',lw = 2.5)

# method 1:
# xy=是坐标,xycoords='data'以data的值为基准,xytext...
plt.annotate(r'$2x+1=%s$'%y0,xy=(x0,y0),xycoords='data',xytext=(+30,-30),textcoords='offset points'
             ,fontsize=16,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'))

# method 2:
# (-3.7,3)表示位置,
plt.text(-3.7,3,r'$This\ is\ the\ some\ text.\ \mu \sigma_i \alpha_t$',
         fontdict = {'size':16,'color':'r'})

plt.show()