import matplotlib.pyplot as plt
import numpy as np

X = [0.10,0.20,0.30,0.40,0.50,0.60,0.70,0.80,0.90,1.00]
Y =	[0.904837,0.818731,0.740818,0.670320,0.606531,0.548812,0.496585,0.449329,0.406570,0.367879]
M = [-0.904837,-0.818731,-0.740818,-0.670320,-0.606531,-0.548812,-0.496585,-0.449329,-0.406570,-0.367879]

def Lj_PI(j):
    res = 0
    for k in range(len(X)):
        if (k == j): continue
        res += (1/(X[j]-X[k]))
    return res

def Lj(x,j):
    """x是变量,k是第k个的索引"""
    res = 1
    for i in range(len(X)):
        if i == j: continue
        else:
            res = res*( (x-X[i]) / (X[j]-X[i]) )
    return res

# def Alpha(x,j):
#     return (1 - 2*(x-X[j])*Lj_PI(j) * ( Lj(x,j)*Lj(x,j) ) )
#
# def Beta(x,j):
#     return (x-X[j])*( Lj(x,j)*Lj(x,j) )

Alpha = lambda x,j: ((1 - 2*(x-X[j])*Lj_PI(j)) * ( Lj(x,j)*Lj(x,j) ) )
Beta = lambda x,j: (x-X[j])*( Lj(x,j)*Lj(x,j) )

def Hermite(x):
    res = 0
    for j in range(len(X)):
        res = res + (Y[j]*Alpha(x,j) + M[j]*Beta(x,j))
    return res

lx = np.linspace(0.1,1,100)
lx = list(lx)
# print(lx)
y = []
for x in lx:
    y.append(Hermite(x))
# print(y)
x0 = 0.55
y0 = Hermite(x0)
print("y0 = %s"%y0)
plt.figure(num=1,figsize=(8,5))
hermite, = plt.plot(lx,y)

plt.scatter(x0,y0,s=50,color='black')

plt.xlabel("I am X")
plt.ylabel("I am Y")
# gca = 'get current axis'
ax = plt.gca()
# spines脊梁,即图的四条框(none即没有)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 打印出线条的名字hermite插值多项式
plt.legend(handles=[hermite],labels = [r'$Hermite\ Interpolation\ Polynomial$'], loc='best')

# xy=是坐标,xycoords='data'以data的值为基准,xytext...
plt.annotate(r'$H(%s)=%s$'%(x0,round(y0,3)),xy=(x0,y0),xycoords='data',xytext=(+20,+20),textcoords='offset points'
             ,fontsize=15,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'))

for i in range(len(X)):   #画点
    plt.scatter(X[i],Y[i],s = 50,color='r')

plt.show()