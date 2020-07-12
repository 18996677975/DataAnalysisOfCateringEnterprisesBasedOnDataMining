import pandas as pd
from sklearn.naive_bayes import MultinomialNB
from sklearn.utils import shuffle     # 打乱数据的函数
from sklearn.preprocessing import MinMaxScaler     # 归一化器

mms = MinMaxScaler()

# 读入去除空缺的客户流失特征数据表
data = pd.read_excel('../Tmp/去除已流失的客户流失特征数据表.xls')

# 打乱数据
data = shuffle(data)

data.iloc[:, -1][data.iloc[:, -1] == '准流失'] = -1
data.iloc[:, -1][data.iloc[:, -1] == '非流失'] = 1

# 数据归一化
data.iloc[:, 2:-1] = mms.fit_transform(data.iloc[:, 2:-1])

# 数据划分（9/10为训练集，1/10为测试集）
train_x = data.iloc[:int(len(data)*9/10), 2:-1].values.astype(float)
train_y = data.iloc[:int(len(data)*9/10), -1].values.astype(int)
test_x = data.iloc[int(len(data)*9/10):, 2:-1].values.astype(float)
test_y = data.iloc[int(len(data)*9/10):, -1].values.astype(int)

# 建立朴素贝叶斯模型
nb = MultinomialNB(alpha=1.0)

# 模型训练
nb.fit(train_x, train_y)

# 预测结果，并查看正确率
answer = nb.predict(test_x)
right = 0
for i in range(len(answer)):
    if answer[i] == test_y[i]:
        right += 1
print('正确率：' + str(right/len(answer)))