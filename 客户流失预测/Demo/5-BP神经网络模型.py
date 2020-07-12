import pandas as pd
from sklearn.utils import shuffle     # 打乱数据的函数
import tensorflow as tf
import time

# 读入去除空缺的客户流失特征数据表
data = pd.read_excel('../Tmp/去除已流失的客户流失特征数据表.xls')

# 打乱数据
# data = shuffle(data)

data.iloc[:, -1][data.iloc[:, -1] == '准流失'] = 0
data.iloc[:, -1][data.iloc[:, -1] == '非流失'] = 1

# 数据划分（9/10为训练集，1/10为测试集）
train_x = data.iloc[:int(len(data)*9/10), 2:-1].values.astype(float)
train_y = data.iloc[:int(len(data)*9/10), -1].values.astype(int)
test_x = data.iloc[int(len(data)*9/10):, 2:-1].values.astype(float)
test_y = data.iloc[int(len(data)*9/10):, -1].values.astype(int)

# 搭建DNN网络
start_time = time.time()
model = tf.keras.Sequential()
model.add(tf.keras.layers.Dense(512, input_shape=(4,), activation='relu'))
model.add(tf.keras.layers.Dense(256, activation='relu'))
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# 优化器、损失函数
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])

# 模型训练
history = model.fit(train_x, train_y, epochs=100)

result = model.evaluate(test_x, test_y)
end_time = time.time()

print("正确率：" + str(result[1]))
print('总用时：' + str(end_time-start_time))
