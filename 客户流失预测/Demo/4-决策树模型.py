import pandas as pd
from sklearn.utils import shuffle     # 打乱数据的函数
from sklearn.tree import DecisionTreeClassifier as DTC
import time

# 读入去除空缺的客户流失特征数据表
data = pd.read_excel('../Tmp/去除已流失的客户流失特征数据表.xls')

# 打乱数据
# data = shuffle(data)

data.iloc[:, -1][data.iloc[:, -1] == '准流失'] = -1
data.iloc[:, -1][data.iloc[:, -1] == '非流失'] = 1

# 数据划分（9/10为训练集，1/10为测试集）
train_x = data.iloc[:int(len(data)*9/10), 2:-1].values.astype(float)
train_y = data.iloc[:int(len(data)*9/10), -1].values.astype(int)
test_x = data.iloc[int(len(data)*9/10):, 2:-1].values.astype(float)
test_y = data.iloc[int(len(data)*9/10):, -1].values.astype(int)

# 建立决策树模型，基于信息熵
start_time = time.time()
dtc = DTC(criterion='entropy')

# 模型训练
dtc.fit(train_x, train_y)

# 预测结果，并查看正确率
answer = dtc.predict(test_x)
end_time = time.time()
right = 0
for i in range(len(answer)):
    if answer[i] == test_y[i]:
        right += 1
print('正确率：' + str(right/len(answer)))
print('总用时：' + str(end_time-start_time))

#导入相关函数，可视化决策树。
#导出的结果是一个dot文件，需要安装Graphviz才能将它转换为pdf或png等格式。
from sklearn.tree import export_graphviz
with open("../Tmp/tree.dot", 'w') as f:
    f = export_graphviz(dtc, feature_names=data.columns[2:-1], out_file=f, class_names=['notloss', 'lossing'], filled=True)