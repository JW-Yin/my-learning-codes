# 步骤1：导入 argparse 模块
import argparse

def read_file():
    # 步骤2：创建解析器对象
    parser = argparse.ArgumentParser(description="一个简单的demo")
    
    # 步骤3：
    ## 添加位置参数(不显式指定 type 参数，命令行传入的参数会被默认解析为 str 类型)
    parser.add_argument("file_path", help="要读取的文件路径")
    parser.add_argument("line_num", type=int, help="要读取的文件前 N 行（必须是整数，否则报错）")
    ## 添加可选参数：-o/--output（输出文件路径，可选参数，有默认值）
    parser.add_argument(
        "-o", # 短选项，单个字母，使用时输入 -o
        "--output", # 长选项，单词组合，使用时输入 --output，短/长选项可任选其一使用
        type=str, # 参数类型，这里是字符串
        required=True,  # 是否必传，这里设为True（命令行必须指定输出路径），可选属性（默认False）
        default="download.html",  # 默认值：如果用户不传-o，就使用这个默认文件名
        help="网页下载后的输出文件路径（可选），默认值：download.html" # 帮助信息，-h时显示，必填属性
    )

    # 步骤4：解析命令行参数
    args = parser.parse_args()
    
    # 步骤5：使用解析后的参数
    print(args.file_path)

    # 步骤6：判断可选参数是否有传入
    if args.output is not None:
        print(f"✅ 用户传入了 --output 参数，值为：{args.output}（类型：{type(args.output)}）")
    else:
        print(f"❌ 用户未传入 --output 参数，当前值为：{args.output}")
    
    try:
        print("文件内容：")
        with open(args.file_path, "r", encoding="utf-8") as f:
            for i in range(args.line_num):
                line = f.readline()
                if not line:
                    print("没有更多行可读了！")
                    break
                print(f"第{i}行内容："+line.strip())
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.file_path}")

if __name__ == "__main__":
    read_file()
