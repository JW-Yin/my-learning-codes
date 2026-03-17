import json  # 先导入json模块
import os
pwd = os.path.dirname(os.path.abspath(__file__))
file_path = pwd + '/test.json'

# 你的通讯录数据
test = [
    {"姓名": "张三", "电话": "13800138000"},
    {"姓名": "李四", "电话": "13900139000"}
]

# 把数据写入JSON文件
with open(file_path, "w", encoding="utf-8") as f:
    # ensure_ascii=False：让中文正常显示（不然会变成unicode编码）
    # indent=2是格式化缩进，更美观
    json.dump(test, f, ensure_ascii=False, indent=2)  

