import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA
from mpl_toolkits.mplot3d import Axes3D  # 空间三维画图


trainMat = np.loadtxt("trainMat_3D.txt")
labels = np.loadtxt("labels.txt")
print(trainMat)
print(labels)


fig = plt.figure()
treeD_ax = Axes3D(fig)

labels = labels[::10]

f0 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='red',marker='x',lw = 1)
f1 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='blue',marker='.',lw = 1)
f2 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='yellow',marker=',',lw = 1)
f3 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='pink',marker='v',lw = 1)
f4 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='green',marker='^',lw = 1)
f5 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='black',marker='+',lw = 1)
f6 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='brown',marker='d',lw = 1)
f7 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='purple',marker='*',lw = 1)
f8 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='orange',marker='s',lw = 1)
f9 = lambda x: treeD_ax.scatter(x[0], x[1], x[2], s=15, color='indigo',marker='o',lw = 1)

scatter_dict = {0:f0, 1:f1, 2:f2, 3:f3, 4:f4, 5:f5, 6:f6, 7:f7, 8:f8, 9:f9}

for i,x in enumerate(trainMat[::10]):
	scatter_dict[labels[i]](x)

plt.show()