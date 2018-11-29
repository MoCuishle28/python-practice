import matplotlib.pyplot as plt
import numpy as np

# Lagrange插值多项式,画出Ln

lx = [0,10,20,30,40,50,60,70,80,90,100,110,120]
ly = [5,1,7.5,3,4.5,8.8,15.5,6.5,-5,-10,-2,4.5,7]

def LK(x,k):
    """x是变量,k是第k个的索引"""
    res = 1
    for j in range(len(lx)):
        if j == k: continue
        else:
            res = res*( (x-lx[j]) / (lx[k]-lx[j]) )
    return res

def LN(x):
    res = 0
    for k in range(len(ly)):
        res = res+( ly[k] * LK(x,k) )
    return res

# 测试Lagrange插值多项式的函数
def Fx():
    res = []
    for x in lx:
        res.append(LN(x))
    return res

plt.figure(figsize=(8,5),num=0)

x0 = 65
y0 = LN(x0)
print("X=65","Y=%s"%y0)

Y = []
X = np.linspace(0,120,120)
X = list(X)
for i in X:
    Y.append(LN(i))

# print("X:",X)
# print("Y:",Fx())
# print("Lagrange插值多项式计算结果:",Y)

# 画图并返回曲线名字
Lagrange0, = plt.plot(X,Y)
for i in range(len(lx)):                    #画点
    plt.scatter(lx[i],ly[i],s = 50,color='r')
plt.scatter(x0,y0,s=50,color='black')
plt.xlabel("I am X")
plt.ylabel("I am Y")
# gca = 'get current axis'
ax = plt.gca()
# spines脊梁,即图的四条框(none即没有)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 打印出线条的名字Lagrange插值多项式
# plt.legend(handles=[Lagrange0],labels = [r'$Lagrange\ Interpolation\ Polynomial$'], loc='best')
# 放下面一起画出以上提示框

# xy=是坐标,xycoords='data'以data的值为基准,xytext...
plt.annotate(r'$Ln(%s)=%s$'%(x0,round(y0,3)),xy=(x0,y0),xycoords='data',xytext=(+20,+20),textcoords='offset points'
             ,fontsize=15,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.5'))

####################################################################################################
# 分段插值
def LK_sub(x,k,index_a,index_b):
    """x是变量,k是第k个的索引,index_a和index_b是区间端点索引"""
    res = 1
    for j in index_a,index_b:
        if j == k:
            continue
        else:
            res = res = res * ((x - lx[j]) / (lx[k] - lx[j]))
    return res

def LN_sub(x,index_a,index_b):
    res = 0
    for k in index_a,index_b:
        res = res+( ly[k] * LK_sub(x,k,index_a,index_b) )
    return res

# 分段插值的测试函数
def Fx_sub():
    res = []
    for x in range(len(lx)-1):
        res.append(LN_sub(lx[x],x,x+1))
    res.append(LN_sub(lx[x+1],x,x+1))
    return res

# print("----------------------------------------------------------------")
# print("测试结果:",Fx_sub())
Y_sub = []
X_sub = np.linspace(0,120,120)
X_sub = list(X_sub)
cnt = 0
index_a = 0
index_b = 1

for i in X_sub:
    if cnt == 10:
        cnt = 0
        index_a = index_b
        index_b = index_b+1
    Y_sub.append(LN_sub(i,index_a,index_b))
    cnt = cnt+1

# print("最后结果",Y_sub)
Lagrange1 ,= plt.plot(X_sub,Y_sub,color='black',linestyle='--')
y0 = LN_sub(x0,6,7)
print("分段插值结果:X=65","Y=%s"%y0)
plt.scatter(x0,y0,s=50,color='pink')
# 打印出线条的名字Lagrange插值多项式
plt.legend(handles=[Lagrange0,Lagrange1],labels = [r'$Lagrange\ Interpolation\ Polynomial$'
                                                    ,r'$Lagrange\ Segmentation\ Interpolation\ Polynomial$'], loc='best')
# xy=是坐标,xycoords='data'以data的值为基准,xytext...
plt.annotate(r'$Ln(%s)=%s$'%(x0,y0),xy=(x0,y0),xycoords='data',xytext=(-60,-50),textcoords='offset points'
             ,fontsize=15,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.5'))


# 以下为牛顿插值多项式
# print("--------------------------------------Newton-----------------------------------------")
# def f(list_x,list_y):
#     if len(list_x) == 2:
#         return (list_y[0] - list_y[-1]) / (list_x[0] - list_x[-1])
#     return   ( f(list_x[1:],list_y[1:]) - f(list_x[0:-1],list_y[0:-1]) ) / (list_x[-1] - list_x[0])
#
# def Newton(x):
#     res = ly[0]
#     cnt = 2
#     for i in range(len(lx)):
#         t = 1
#         if i == 0: continue
#         for j in range(i):
#             t = t * (x - lx[j])
#         res = res + (t* f(lx[0:cnt],ly[0:cnt]) )
#         cnt += 1
#     return res
#
# def Newton_sub(x,sub_x):
#     res = ly[0]
#     cnt = 2
#     for i in range(len(lx)):
#         t = 1
#         if i == 0: continue
#         for j in range(i):
#             t = t * (x - lx[j])
#         res = res + (t * f(lx[0:cnt], ly[0:cnt]))
#         cnt += 1
#     return res
#
# y0 = Newton(x0)
# Y = []
# for tx in X:
#     Y.append(Newton(tx))

# sub_Y = []
# for i in range(len(X)):
#     if i == len(X):
#         sub_Y.append(Newton_sub(X[i],lx[i-1:]))
#     sub_Y.append(Newton_sub(X[i],lx[i:i+2]))

# plt.figure(figsize=(8,5),num=1)
# newton0, = plt.plot(X,Y)
# print("牛顿插值多项式结果:X=65","Y=%s"%y0)
#
# plt.scatter(x0,y0,s=50,color='yellow')
# plt.xlabel("I am X")
# plt.ylabel("I am Y")
# # gca = 'get current axis'
# ax = plt.gca()
# # spines脊梁,即图的四条框(none即没有)
# ax.spines['right'].set_color('none')
# ax.spines['top'].set_color('none')
# # 打印出线条的名字Newton插值多项式
# plt.legend(handles=[newton0],labels = [r'$Newton\ Interpolation\ Polynomial$'], loc='best')
# # xy=是坐标,xycoords='data'以data的值为基准,xytext...
# plt.annotate(r'$Ln(%s)=%s$'%(x0,round(y0,3)),xy=(x0,y0),xycoords='data',xytext=(20,20),textcoords='offset points'
#              ,fontsize=15,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.5'))
#
# for i in range(len(lx)):                    #画点
#     plt.scatter(lx[i],ly[i],s = 50,color='r')

plt.show()