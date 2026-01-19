# 示例1：硬编码脚本（固定读取 test.txt，固定是否打印长度）

import os

pwd= os.path.dirname(os.path.abspath(__file__))
def read_file():
    # 固定死的文件路径，要换文件就得修改这里的代码
    file_path = pwd + "/test.txt"
    # 固定死的开关，要关闭打印长度就得改 False
    show_length = True
    
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    print("文件内容：")
    print(content)
    
    if show_length:
        print(f"\n文件内容长度：{len(content)}")

if __name__ == "__main__":
    read_file()