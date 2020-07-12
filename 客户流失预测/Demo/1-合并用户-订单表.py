import pandas as pd
import numpy as np

# 读入用户信息表、订单表
users = pd.read_csv('../Data/users.csv', encoding='gbk')
new_users = pd.read_csv('../Data/user_loss.csv', encoding='gbk')
orders = pd.read_csv('../Data/meal_order_info.csv', encoding='gbk')
new_orders = pd.read_csv('../Data/info_new.csv', encoding='gbk')

# 新旧表合并
users = pd.concat([new_users, users], axis=0, ignore_index=False, sort=False)
orders = pd.concat([new_orders, orders], axis=0, ignore_index=False, sort=False)

# 提取有用信息列
users = users.iloc[:, [0, 2, 14, -1]]
users = users.fillna(0)
orders = orders.iloc[:, [-1, 2, 6, 9]]
orders = orders.fillna(0)
orders.rename(columns={'name': 'ACCOUNT'}, inplace=True)

# 用户、订单表合并
result = pd.merge(users, orders, on='ACCOUNT')
result = result.iloc[:, [0, 1, 6, 2, 4, 5, 3]]
result.columns = ['user_id', 'name', 'time', 'LAST_VISITS', 'consumers', 'expenditure', 'type']
result.sort_values(by='user_id', inplace=True)

# 去掉time后面具体时间，只保留年月日
for i in range(len(result)):
    result.iloc[i, 2] = result.iloc[i, 2][:result.iloc[i, 2].index(' ')]

result.to_excel('../Tmp/合并客户信息和订单表后的数据.xls', index=None)