import os
pwd=os.path.dirname(os.path.abspath(__file__))
file_path=pwd+"/test.txt"

# 方式1：一次性读全部内容（适合小文件）
with open(file_path, "r", encoding="utf-8") as f:  # encoding指定中文编码
    content = f.read()  # 把文件所有内容读到content里
print(content)  # 输出：张三 13800138000\n李四 13900139000


# 方式2：逐行读（适合大文件，省内存）
with open(file_path, "r", encoding="utf-8") as f:
    line1 = f.readline()  # 读第一行
    line2 = f.readline()  # 读第二行
print("第一行：", line1)  # 第一行：张三 13800138000
print("第二行：", line2)  # 第二行：李四 13900139000


# 方式3：读所有行到列表里
with open(file_path, "r", encoding="utf-8") as f:
    lines = f.readlines()  # 得到列表：["张三 13800138000\n", "李四 13900139000"]
print(lines)

