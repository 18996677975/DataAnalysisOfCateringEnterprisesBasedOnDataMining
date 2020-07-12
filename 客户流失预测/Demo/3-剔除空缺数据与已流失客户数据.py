import pandas as pd

# 读入客户流失特征数据表
data = pd.read_excel('../Tmp/客户流失特征数据表.xls')

# 取出所有type=0的行
drop_rows = (data.iloc[:, -1] == 0).to_list()

# 取出所有空缺行的行数
index = []
for i in range(len(drop_rows)):
    if drop_rows[i]:
        index.append(i)

# 删除空缺行
data.drop(index, axis=0, inplace=True)

# 数据保存
data.to_excel('../Tmp/去除空缺的客户流失特征数据表.xls', index=None)

# 剔除'已流失'客户数据
index = data.iloc[:, -1][data.iloc[:, -1] == '已流失'].index
index = index.to_list()
data.drop(index, axis=0, inplace=True)

data.to_excel('../Tmp/去除已流失的客户流失特征数据表.xls', index=None)