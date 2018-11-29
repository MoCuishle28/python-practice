import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
from sklearn.decomposition import PCA


SZ=20
bin_n = 16 # Number of bins
affine_flags = cv.WARP_INVERSE_MAP|cv.INTER_LINEAR


# 使用二阶矩矫正图像
def deskew(img):
    m = cv.moments(img)
    if abs(m['mu02']) < 1e-2:
        return img.copy()
    skew = m['mu11']/m['mu02']
    M = np.float32([[1, skew, -0.5*SZ*skew], [0, 1, 0]])
    # 图像的平移，参数:输入图像、变换矩阵、变换后的大小
    img = cv.warpAffine(img, M, (SZ, SZ), flags=affine_flags)
    return img


def hog(img):
    '''先用sobel提取轮廓信息 再做轮廓信息的统计直方图'''
    # 计算图像的 X 方向和 Y 方向的 Sobel 导数(梯度滤波器)
    gx = cv.Sobel(img, cv.CV_32F, 1, 0)
    gy = cv.Sobel(img, cv.CV_32F, 0, 1)
    mag, ang = cv.cartToPolar(gx, gy)       # 笛卡尔坐标转换为极坐标, → magnitude, angl
    bins = np.int32(bin_n*ang/(2*np.pi))
    bin_cells = bins[:10,:10], bins[10:,:10], bins[:10,10:], bins[10:,10:]
    mag_cells = mag[:10,:10], mag[10:,:10], mag[:10,10:], mag[10:,10:]

    hists = [np.bincount(b.ravel(), m.ravel(), bin_n) for b, m in zip(bin_cells, mag_cells)]
    hist = np.hstack(hists)     # hist 是64位的向量
    return hist


img = cv.imread('digits.png',0)

if img is None:
    raise Exception("we need the digits.png image from samples/data here !")


cells = [np.hsplit(row,100) for row in np.vsplit(img,50)]	# 横轴切成50份 -> 每份纵轴切成100份

# 二分训练集和测试集
train_cells = [ i[:50] for i in cells ]
test_cells = [ i[50:] for i in cells]

deskewed = [list(map(deskew, row)) for row in train_cells]	# 对训练集每个样例做抗扭曲处理
hogdata = [list(map(hog, row)) for row in deskewed]			# 提取特征值

trainData = np.float32(hogdata).reshape(-1,64)

# 显示特征值
print(trainData[0].shape)
print(trainData[0])

pca = PCA(n_components=2, svd_solver='arpack')
test_pca = trainData
pca_mat = pca.fit_transform(test_pca)
np.savetxt("trainMat.txt", pca_mat)

pca_3d = PCA(n_components=3, svd_solver='arpack')
test_pca_3d = trainData
pca_mat = pca_3d.fit_transform(test_pca_3d)
np.savetxt("trainMat_3D.txt", pca_mat)

responses = np.repeat(np.arange(10),250)[:,np.newaxis]

np.savetxt("labels.txt", responses)


svm = cv.ml.SVM_create()
svm.setKernel(cv.ml.SVM_LINEAR)
svm.setType(cv.ml.SVM_C_SVC)
svm.setC(2.67)
svm.setGamma(5.383)
svm.train(trainData, cv.ml.ROW_SAMPLE, responses)
svm.save('svm_data.dat')

# 预处理测试数据集
deskewed = [list(map(deskew,row)) for row in test_cells]
hogdata = [list(map(hog,row)) for row in deskewed]

testData = np.float32(hogdata).reshape(-1,bin_n*4)

result = svm.predict(testData)[1]
mask = result==responses
correct = np.count_nonzero(mask)

print(correct*100.0/result.size)