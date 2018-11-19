from numpy import *
import operator
from os import listdir
from PIL import Image
import matplotlib.pylab as plt
import matplotlib.image as mpimg # mpimg 用于读取图片
import numpy as np

# Test code
# def createDataSet():
#     group = array([[1.0,1.1],[1.0,1.0],[0,0],[0,0.1]])
#     labels = ['A','A','B','B']
#     return group,labels

def imgToVector(fileName):
    # create a vector (every elements is zero)1行1024列
    retVect = zeros((1,1024))
    with open(fileName) as f:
        for i in range(32):
            lineStr = f.readline()
            # 将前32字转换为int存入向量
            for j in range(32):
                retVect[0,32*i+j] = int(lineStr[j])
    return retVect

def classify(inVector, dataSet, labels, k):
    """
    :param inVector: 用于分类的输入向量
    :param dataSet: 输入的训练样本集
    :param labels:  样本数据的类标签向量
    :param k: 用于选择最近邻居的数目
    :return: 返回频次最高的类别
    """
    # 样本数据(第一维[0])的数量
    dataSetSize = dataSet.shape[0]

    # 以下为求欧氏距离的语句,distances是求出的欧氏距离
    # 矩阵运算,计算测试数据与每个样本数据对应数据(每个元素)的差值
    # title(a,(num1,num2))向量a在列方向上重复num1次,行方向上重复num2次
    diffMat = tile(inVector, (dataSetSize, 1)) - dataSet
    # 上一结果的平方
    sqDiffMat = diffMat**2
    # axis=1是压缩列,即将每一行的元素相加,将矩阵压缩为一列
    sqDist = sqDiffMat.sum(axis=1)
    # 取平方根,得到距离向量
    distances = sqDist**0.5

    # 按照距离值从小到大排列数组的索引(返回的是排列前的数组的索引在排列后的位置)
    sortedDistIndex = distances.argsort()
    classCount = {}

    # 依次取出最近的样本数据
    for i in range(k):
        # 记录该样本数据所属类别
        voteLabel = labels[sortedDistIndex[i]]
        # voteLabel位置上加1
        classCount[voteLabel] = classCount.get(voteLabel,0)+1

    # 对类别出现频率进行排序,从低到高(operator.itemgetter(1)表示对第二个域进行排序)(reverse=True降序)
    sortedClassCount = sorted(classCount.items(),key=operator.itemgetter(1),reverse=True)
    # 返回频次最高([0])的类别([0][0])
    return sortedClassCount[0][0]

# 测试训练分类结果
def handWritingClassTest():
    # 训练样本数据的类标签列表
    hwLabels = []
    # 训练样本数据文件列表
    trainingFileList = listdir('digits/trainingDigits')
    m = len(trainingFileList)
    # 初始化训练样本数据矩阵
    trainingMat = zeros((m,1024))

    # 依次读取所有训练样本数据到数据矩阵中
    for i in range(m):
        # 以下为提取文件名字中的数字的语句
        fileName = trainingFileList[i]
        fileStr = fileName.split('.')[0]
        # '_'前的数字为正确答案
        classNum = int(fileStr.split('_')[0])
        hwLabels.append(classNum)
        # 将样本数据存入矩阵
        trainingMat[i,:] = imgToVector('digits/trainingDigits/%s'%fileName)

    # 循环读取测试数据
    testFileList = listdir('digits/testDigits')
    # 初始化错误数
    errorCount = 0
    testSize = len(testFileList)

    # 循环测试每个测试数据文件
    for i in range(testSize):
        fileName = testFileList[i]
        fileStr = fileName.split('.')[0]
        classNum = int(fileStr.split('_')[0])
        # 提取数据向量
        testVector = imgToVector('digits/testDigits/%s'%fileName)
        # 对数据文件进行分类
        classifierResult = classify(testVector, trainingMat, hwLabels, 3)
        # 打印分类结果
        print("分类器分类结果为: %d, 实际结果为: %d"%(classifierResult, classNum))
        # 判断结果是否准确
        if (classifierResult != classNum):
            errorCount += 1.0
    print("-------------额外测试-------------------------------")
    t = 0
    for i in range(10):
        img = mpimg.imread(str(i)+'.png')
        plt.imshow(img) # 读取和代码处于同一目录下的 img.png
        # 此时 img 就已经是一个 np.array 了，可以对它进行任意处理
        plt.axis('off')
        plt.show()
        testVector = imgToVector(str(i)+'.txt')
        classifierResult = classify(testVector, trainingMat, hwLabels, 3)
        if classifierResult != i:
            t += 1
        print("分类器分类结果为: %d, 实际结果为: %d" % (classifierResult, i))
    print("-------------额外测试-------------------------------")
    print("额外测试错误数为:%d"%t)
    print("总错误数为:%f"%errorCount)
    print("总错误率为:%f"%(errorCount/float(testSize)))


def pictureTo01(filename):
    """
    将图片转化为32*32像素的文件，用0 1表示
    :param filename: 图片路径
    :return: 生成的01字符txt文件
    """
    # 打开图片
    # 模式“RGBA”:
    # 模式“RGBA”为32位彩色图像，
    # 它的每个像素用32个bit表示，其中24bit表示红色、绿色和蓝色三个通道，
    # 另外8bit表示alpha通道，即透明通道。
    img = Image.open(filename).convert('RGBA')
    # 得到图片的像素值
    pixel_data = img.load()
    # 将其降噪并转化为黑白两色
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if pixel_data[x, y][0] < 90:
                pixel_data[x, y] = (0, 0, 0, 255)

            if pixel_data[x, y][1] < 136:
                pixel_data[x, y] = (0, 0, 0, 255)

            if pixel_data[x, y][2] > 0:
                pixel_data[x, y] = (255, 255, 255, 255)

    # for y in range(img.size[1]):
    #     for x in range(img.size[0]):
    #         if pixel_data[x, y][0] < 90:
    #             pixel_data[x, y] = (0, 0, 0, 255)
    #
    # for y in range(img.size[1]):
    #     for x in range(img.size[0]):
    #         if pixel_data[x, y][1] < 136:
    #             pixel_data[x, y] = (0, 0, 0, 255)
    #
    # for y in range(img.size[1]):
    #     for x in range(img.size[0]):
    #         if pixel_data[x, y][2] > 0:
    #             pixel_data[x, y] = (255, 255, 255, 255)

    # 设置为32*32的大小
    img = img.resize((32, 32), Image.LANCZOS)
    # 得到像素数组，为(32,32,4)
    array = plt.array(img)
    # 按照公式将其转为01, 公式： 0.299 * R + 0.587 * G + 0.114 * B
    gray_array = np.zeros((32, 32))
    # 行数
    for x in range(array.shape[0]):
        # 列数
        for y in range(array.shape[1]):
            # 计算灰度，若为255则白色，数值越小越接近黑色
            gary = 0.299 * array[x][y][0] + 0.587 * array[x][y][1] + 0.114 * array[x][y][2]
            # 设置一个阙值，记为0
            if gary == 255:
                gray_array[x][y] = 0
            else:
                # 否则认为是黑色，记为1
                gray_array[x][y] = 1

    # 得到对应名称的txt文件
    name01 = filename.split('.')[0]
    name01 = name01 + '.txt'
    # 保存到文件中
    np.savetxt(name01, gray_array, fmt='%d', delimiter='')


if __name__ == "__main__":
    # #test code 第一行的0,1字符
    # testVector = imgToVector("digits/testDigits/0_1.txt")
    # print(testVector[0,0:31])
    # # 测试分类器(应输出B)
    # group,labels = createDataSet()
    # print(classify0([0,0],group,labels,3))

    # 测试将png图转换为01字符文件
    # for i in range(10):
    #     pictureTo01(str(i)+".png")
    handWritingClassTest()