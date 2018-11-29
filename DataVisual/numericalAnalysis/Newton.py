import matplotlib.pyplot as plt
import numpy as np

lx = [0,10,20,30,40,50,60,70,80,90,100,110,120]
ly = [5,1,7.5,3,4.5,8.8,15.5,6.5,-5,-10,-2,4.5,7]
# 以下为牛顿插值多项式
print("--------------------------------------Newton-----------------------------------------")
def f(list_x,list_y):
    if len(list_x) == 2:
        return (list_y[0] - list_y[-1]) / (list_x[0] - list_x[-1])
    return   ( f(list_x[1:],list_y[1:]) - f(list_x[0:-1],list_y[0:-1]) ) / (list_x[-1] - list_x[0])

def Newton(x):
    res = ly[0]
    cnt = 2
    for i in range(len(lx)):
        t = 1
        if i == 0: continue
        for j in range(i):
            t = t * (x - lx[j])
        res = res + (t* f(lx[0:cnt],ly[0:cnt]) )
        cnt += 1
    return res

f_sub = lambda list_x,list_y:  ( (list_y[0] - list_y[-1]) ) / ( (list_x[0] - list_x[-1]) )
Newton_sub = lambda x,sub_x,sub_y: sub_y[0] + (f_sub(sub_x,sub_y)*(x - sub_x[0]))

x0 = 65
y0 = Newton(x0)
Y = []
X = np.linspace(0,120,120)
X = list(X)

for tx in X:
    Y.append(Newton(tx))

sub_Y = []
cntS = 0
cntE = 2
cnt = 1
for i in range(len(X)):
    if cnt%10 == 0 and cnt != 120:
        cntS += 1
        cntE += 1
    sub_Y.append(Newton_sub(X[i],lx[cntS:cntE],ly[cntS:cntE]))
    cnt += 1

plt.figure(figsize=(8,5))
newton0, = plt.plot(X,Y)
newton1, = plt.plot(X,sub_Y,color="black",linestyle="--")

print(Y)
print(sub_Y)
print("牛顿插值多项式结果:X=65","Y=%s"%y0)
y1 = Newton_sub(x0,lx[6:8],ly[6:8])
print("牛顿分段插值多项式结果:X=65","Y=%s"%y1)

plt.scatter(x0,y0,s=50,color='blue')
plt.scatter(x0,y1,s=50,color='black')

plt.xlabel("I am X")
plt.ylabel("I am Y")
# gca = 'get current axis'
ax = plt.gca()
# spines脊梁,即图的四条框(none即没有)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 打印出线条的名字Newton插值多项式
plt.legend(handles=[newton0,newton1],labels = [r'$Newton\ Interpolation\ Polynomial$',
                                               r'$Newton\ Interpolation\ Segmentation\ Polynomial$'], loc='best')
# xy=是坐标,xycoords='data'以data的值为基准,xytext...
plt.annotate(r'$Ln(%s)=%s$'%(x0,round(y0,3)),xy=(x0,y0),xycoords='data',xytext=(20,20),textcoords='offset points'
             ,fontsize=15,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.5'))
plt.annotate(r'$Ln(%s)=%s$'%(x0,round(y1,3)),xy=(x0,y1),xycoords='data',xytext=(-30,-60),textcoords='offset points'
             ,fontsize=15,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.3'))

for i in range(len(lx)):                    #画点
    plt.scatter(lx[i],ly[i],s = 50,color='r')

plt.show()