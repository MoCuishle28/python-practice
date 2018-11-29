import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


trainMat = np.loadtxt("trainMat.txt")
labels = np.loadtxt("labels.txt")
print(trainMat)
print(labels)


plt.figure()


ax = plt.gca()

ax.spines['right'].set_color('none')
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')
ax.yaxis.set_ticks_position('left')
ax.spines['bottom'].set_position(('data',0))
ax.spines['left'].set_position(('data',0))

for i,x in enumerate(trainMat):
	if labels[i] == 0:
		ax.scatter(x[0], x[1], s=15, color='red',marker='x',lw = 1)
	elif labels[i] == 1:
		ax.scatter(x[0], x[1], s=15, color='blue',marker='x',lw = 1)
	elif labels[i] == 2:
		ax.scatter(x[0], x[1], s=15, color='yellow',marker='x',lw = 1)
	elif labels[i] == 3:
		ax.scatter(x[0], x[1], s=15, color='pink',marker='x',lw = 1)
	elif labels[i] == 4:
		ax.scatter(x[0], x[1], s=15, color='green',marker='x',lw = 1)
	elif labels[i] == 5:
		ax.scatter(x[0], x[1], s=15, color='black',marker='x',lw = 1)	

plt.show()