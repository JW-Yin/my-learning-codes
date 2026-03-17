import json
import os
pwd = os.path.dirname(os.path.abspath(__file__))
file_path = pwd + '/test.json'

with open(file_path, "r", encoding="utf-8") as f:
    data = json.load(f)  # 把JSON内容转成Python的列表/字典

print(data)  
# 输出：[{'姓名': '张三', '电话': '13800138000'}, {'姓名': '李四', '电话': '13900139000'}]

print(data[0]["姓名"])  
# 输出：张三（取第一个联系人的姓名）
