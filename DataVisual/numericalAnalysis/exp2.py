import numpy as np
import matplotlib.pyplot as plt

X = [0,10,20,30,40,50,60,70,80,90]
Y = [68,67.1,66.4,65.6,64.6,61.8,61.0,60.8,60.4,60]

def x_Quadratic_Sum():
    res = 0
    for xi in X:
        res = res + xi*xi
    return res

# x or y sum
def sum(ls):
    res = 0
    for i in ls:
        res = res + i
    return res

def x_Multiply_y_Sum():
    res = 0
    for i in range(len(X)):
        res = res + (X[i]*Y[i])
    return res

def x_Sum_Quadratic():
    res = 0
    for xi in X:
        res = res + xi
    return res*res

m = len(X)-1
b = ( (x_Quadratic_Sum() * sum(Y)) - (sum(X) * x_Multiply_y_Sum()) ) / ( ( (m+1)*x_Quadratic_Sum() ) - x_Sum_Quadratic() )
a = ( ( (m+1)*x_Multiply_y_Sum() ) - sum(X)*sum(Y) ) / ( ( (m+1)*x_Quadratic_Sum() ) - x_Sum_Quadratic() )

# check = []
# for xi in X:
#     check.append(a*xi+b)
# print(check)
lx = np.linspace(0,90,900)
lx = list(lx)
ly = []
for xi in lx:
    ly.append(a*xi+b)
# print(ly)
x0 = 55
y0 = a*x0+b
print("f(55) = %s"%y0)
plt.figure(num=0,figsize=(8,5))
line,= plt.plot(lx,ly)

plt.scatter(x0,y0,s=50,color='red')
plt.xlabel("I am X")
plt.ylabel("I am Y")
# gca = 'get current axis'
ax = plt.gca()
# spines脊梁,即图的四条框(none即没有)
ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
# 打印出线条的名字hermite插值多项式
plt.legend(handles=[line],labels = [r'$Least\ Squares$'], loc='best')

# xy=是坐标,xycoords='data'以data的值为基准,xytext...
plt.annotate(r'$f(%s)=%s$'%(x0,round(y0,3)),xy=(x0,y0),xycoords='data',xytext=(+20,+20),textcoords='offset points'
             ,fontsize=15,arrowprops=dict(arrowstyle='->',connectionstyle='arc3,rad=.2'))

for i in range(len(X)):   #画点
    plt.scatter(X[i],Y[i],s = 50,color='black')

plt.show()