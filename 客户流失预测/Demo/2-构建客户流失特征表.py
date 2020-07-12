import pandas as pd

# 读入合并客户信息和订单表后的数据表
data = pd.read_excel('../Tmp/合并客户信息和订单表后的数据.xls')

# 以客户名分类
unique_data = data.drop_duplicates(subset='name')
new_data = []
for i in range(0, len(unique_data)):
    index1 = unique_data.index[i]
    if i+1 == len(unique_data):
        new_data.append(data.iloc[index1:, :])
    else:
        index2 = unique_data.index[i+1]
        new_data.append(data.iloc[index1:index2, :])

# 总用餐次数（frequence），即观测时间内每个客户的总用餐次数
frequence = []
for i in new_data:
    frequence.append(len(i))

# 客户在观测时间内的总消费金额（amount）
amount = []
for i in new_data:
    amount.append(i.iloc[:, 5].sum())

# 客户在观测时间内用餐人均销售额（average）
average = []
for i in new_data:
    average.append(round(i.iloc[:, 5].sum()/i.iloc[:, 4].sum(), 2))

# 客户最近一次用餐的时间距离观测窗口结束的天数（recently）
# 观测窗口结束时间为2016/8/31
recently = []
for i in new_data:
    days = []
    for j in range(len(i)):
        day = (2016 - eval(i.iloc[j, 2][:i.iloc[j, 2].index('/')])) * 365 + (8 - eval(i.iloc[j, 2][i.iloc[j, 2].index('/')+1:i.iloc[j, 2].rindex('/')])) * 30 + (31 - eval(i.iloc[j, 2][i.iloc[j, 2].rindex('/')+1:]))
        days.append(day)
    recently.append(min(days))

# 客户的流失状态（type）
user_type = []
for i in new_data:
    now_type = 0
    for j in range(len(i)):
        if i.iloc[j, -1] != 0:
            now_type = i.iloc[j, -1]
            break
    user_type.append(now_type)

# 格式设置
frequence = pd.DataFrame(frequence, columns=['frequence'])
amount = pd.DataFrame(amount, columns=['amount'])
average = pd.DataFrame(average, columns=['average'])
recently = pd.DataFrame(recently, columns=['recently'])
user_type = pd.DataFrame(user_type, columns=['type'])
unique_data.index = [i for i in range(len(unique_data))]

# 数据合并
result = unique_data.iloc[:, :2].join(frequence).join(amount).join(average).join(recently).join(user_type)

# 数据保存
result.to_excel('../Tmp/客户流失特征数据表.xls', index=None)