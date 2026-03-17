import os
pwd=os.path.dirname(os.path.abspath(__file__))
file_path=pwd+"/test.txt"


# 方式1：覆盖写（原有内容会被清空）
with open(file_path, "w", encoding="utf-8") as f:
    f.write("王五 13700137000")  # 写入一行内容


# 方式2：追加写（在原有内容后面加）
with open(file_path, "a", encoding="utf-8") as f:
    f.write("\n赵六 13600136000")  # \n是换行

