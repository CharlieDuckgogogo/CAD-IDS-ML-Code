import numpy as np
from pandas import read_csv
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score, cross_val_predict
from sklearn.preprocessing import MinMaxScaler
import joblib
# 机器学习模型导入包

from sklearn.linear_model import SGDClassifier

np.random.seed(7)

# load the dataset
dataframe_train1 = read_csv('dt1.csv', engine='python', sep=",", header=None)
trainY1 = read_csv('dt1y.csv', engine='python', header=None)
dataset1 = dataframe_train1.values

# 将整数值转换为浮点值
dataset1 = dataset1.astype('float32')

# normalize the dataset
# MinMaxScaler预处理类轻松地规范化数据集
scaler = MinMaxScaler(feature_range=(0, 1))
trainX1 = scaler.fit_transform(dataset1)


dataframe_train2 = read_csv('dt2.csv', engine='python', sep=",", header=None)
trainY2 = read_csv('dt2y.csv', engine='python', header=None)
dataset2 = dataframe_train2.values
dataset2 = dataset2.astype('float32')
trainX2 = scaler.fit_transform(dataset2)



dataframe_test = read_csv('testx.csv', engine='python', sep=",", header=None)
testy = read_csv('testy.csv', engine='python', header=None)
dataset = dataframe_test.values
test = dataset.astype('float32')
test = scaler.fit_transform(test)


print(test.shape)
print(testy.shape)


from sklearn.neural_network import MLPClassifier
clf = SGDClassifier()
clf.partial_fit(trainX1[:100],trainY1[:100],classes=[0,1])
scores=clf.score(test,testy)
print("Tree1:")
print(scores)
joblib.dump(clf,"sgd1.model")
from sklearn.neural_network import MLPClassifier
clf.partial_fit(trainX2,trainY2)

    #.fit(trainX1,trainY1)
scores=clf.score(test,testy)
print("Tree2:")
print(scores)
joblib.dump(clf,"sgd2.model")