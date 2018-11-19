import numpy as np
import matplotlib.pyplot as plt
import random

def sig(x):
    """
    Sigmoid函数
    :param x: x(mat):feature * w
    :return: sigmoid(x) (mat):Sigmoid值
    """
    return 1.0 / (1 + np.exp(-x))

def load_TestData(file_name, n):
    """
    导入测试数据
    :param file_name:   文件位置
    :param n:           特征值个数
    :return:            测试集特征
    """
    f = open(file_name+'.txt')
    feature_data = []
    for line in f.readlines():
        feature_tmp = []
        lines = line.strip().split('\t')
        if len(lines) != n-1:
            continue
        if random.randint(0,1) > 0.5:
            feature_tmp.append(1)
        else:
            feature_tmp.append(0)
        for x in lines:
            feature_tmp.append(float(x))
        feature_data.append(feature_tmp)
    f.close()
    return np.mat(feature_data)

def predict(data, w):
    """
    对数据进行预测
    :param data:    测试数据集
    :param w:       函数参数（权重）
    :return:        预测结果向量
    """
    h = sig(data * w.T) #取得Sigmoid值
    m = np.shape(h)[0]
    for i in range(m):
        if h[i,0] < 0.5:
            h[i,0] = 0.0
        else:
            h[i,0] = 1.0
    return h

def error_rate(h, label):
    """
    计算当前损失函数值
    :param h:       预测值
    :param label:   实际值
    :return:        错误率
    """
    m = np.shape(h)[0]
    sum_err = 0.0
    for i in range(m):
        if h[i,0] > 0 and ( 1 - h[i,0]) > 0:
            sum_err -= (label[i,0] * np.log(h[i,0]) + (1-label[i,0]) * np.log(1-h[i,0]))
        else:
            sum_err -= 0
    return sum_err / m

def lr_train_bgd(feature, label, maxCycle, alpha):
    """
    利用梯度下降法训练LR模型
    :param feature:     特征
    :param label:       标签
    :param maxCycle:    最大迭代次数
    :param alpha:       学习率
    :return:            权重（参数）
    """
    # 测试数据

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    plt.ion()
    plt.title('Current Classification')
    plt.xlabel('X')
    plt.ylabel('Y')
    aax = plt.gca()
    aax.spines['right'].set_color('none')
    aax.spines['top'].set_color('none')
    aax.xaxis.set_ticks_position('bottom')
    aax.yaxis.set_ticks_position('left')

    n = np.shape(feature)[1] #特征个数
    data = load_TestData("test_data", n)
    w = np.mat(np.ones(n)) #权重初始化
    i = 0
    w = np.transpose(w) #转置
    print(np.shape(feature)[0], np.shape(feature)[1])
    print(np.shape(w)[0],np.shape(w)[1])
    while i < maxCycle:
        i += 1
        h = sig(feature * w) #计算Sigmoid值
        err = label - h #得到一个向量，代表所有训练样本的误差
        # if i % 10 == 0:
        print('\t------------------iter='+str(i), "train error rate="+str(error_rate(h, label)))
        # 目前分类情况

        print('--------------------Current Classification---------------------------')
        print('Current Weights:',w.T)
        try:
            ax.cla()
        except Exception:
            pass
        curr = predict(data, w.T)
        for j in range(len(data)):
            if curr[j, 0] == 0:
                ax.scatter(data[j, 1], data[j, 2], s=15, color='red',marker='x',lw = 1)
            else:
                ax.scatter(data[j, 1], data[j, 2], s=15, color='blue',marker='x', lw = 1)
        plt.pause(0.5)

        w = w + alpha * feature.T * err #权重修正 （feature.T 是为了转置使其能与err相乘）
    print('--------------------Training End---------------------------')
    plt.ioff()
    plt.show()
    plt.close()
    return w

def load_data(file_name):
    """
    :param file_name: 训练样本位置
    :return:          特征，标签
    """
    f = open(file_name)
    feature_data = []
    label_data = []
    for line in f.readlines():
        feature_tmp = []
        label_tmp = []
        lines = line.strip().split('\t')
        feature_tmp.append(1) #偏置项
        for i in range(len(lines) - 1):
            feature_tmp.append(float(lines[i]))
        label_tmp.append(float(lines[-1]))

        feature_data.append(feature_tmp)
        label_data.append(label_tmp)
    f.close()
    return np.mat(feature_data), np.mat(label_data)

def save_model(file_name, w):
    """
    :param file_name:   保存位置
    :param w:           LR模型权重
    :return:
    """
    m = np.shape(w)[0]
    f_w = open(file_name+'.txt', 'w')
    w_array = []
    for i in range(m):
        w_array.append(str(w[i,0]))
    f_w.write("\t".join(w_array))
    f_w.close()

#-----------------------------------------以上为训练时用的函数----------------------------------------------
#-----------------------------------------以下为预测时用的函数----------------------------------------------

def load_weight(file_name):
    """
    导入LR模型
    :param w:   权重所在的文件位置
    :return:    权重矩阵
    """
    f = open(file_name+'.txt')
    w = []
    for line in f.readlines():
        lines = line.strip().split('\t')
        w_tmp = []
        for x in lines:
            w_tmp.append(float(x))
        w.append(w_tmp)
    f.close()
    return np.mat(w)

def save_result(file_name, result):
    """
    保存最终预测结果
    :param file_name:   保存路径
    :param result:      结果向量
    :return:
    """
    m = np.shape(result)[0]
    tmp = []
    for i in range(m):
        tmp.append(str(result[i,0]))
    f_result = open(file_name+'.txt','w')
    f_result.write("\t".join(tmp))
    f_result.close()

if __name__ == "__main__":
    print('--------------------load data----------------------')
    feature,label = load_data("data.txt")
    print('--------------------training-----------------------')
    w = lr_train_bgd(feature, label, 10, 0.01)
    print('--------------------save model---------------------')
    save_model('weights',w)
    print("Finally weights:",w.T)

    print('=================================测试模型===================================')

    # 导入LR模型
    print('--------------------load weights----------------------')
    w = load_weight("weights")
    n = np.shape(w)[1]
    print('--------------------load data-------------------------')
    testData = load_TestData("test_data",n)

    plt.figure()
    plt.title('Logistic Regression')
    plt.xlabel('X')
    plt.ylabel('Y')
    ax = plt.gca()
    ax.spines['right'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    print('--------------------predict---------------------------')
    h = predict(testData, w)
    for i in range(len(testData)):
        if h[i,0] == 0:
            plt.scatter(testData[i,1], testData[i,2], s=12, color='red',lw=1)
        else:
            plt.scatter(testData[i,1], testData[i,2], s=12, color='blue',lw=1)

    # x = np.arange(0,10,0.1)
    # y = np.arange(0,10,0.1)
    # one = np.ones(len(x))
    # matrix = np.mat((one,x,y))
    # print(np.shape(matrix.T)[0],np.shape(matrix.T)[1])
    # res = matrix.T*w.T

    print('--------------------save prediction--------------------')
    save_result("result", h)
    plt.show()