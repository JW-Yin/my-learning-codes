import argparse

def read_file():
    parser = argparse.ArgumentParser(description="一个简单的文件读取脚本（小白入门示例）")
    
    # 位置参数：必须传入的文件路径
    parser.add_argument("file_path", help="要读取的文件路径（比如 test.txt）")
    
    # 可选参数：是否打印文件长度（非必须传入）
    parser.add_argument(
        "--show-length",  # 长格式参数名（推荐，语义清晰）
        "-l",  # 短格式参数名（简写，方便快速输入）
        action="store_true",  # 关键配置：传入该参数则为 True，不传则为 False（布尔开关）
        help="是否打印文件内容的长度（可选参数，无需传值）"
    )
    # 可选参数：设置输出文件路径，默认值为 output.txt
    parser.add_argument("--output", "-o", default="output.txt", help="输出文件路径（默认：output.txt）")
    
    args = parser.parse_args()
    
    try:
        with open(args.file_path, "r", encoding="utf-8") as f:
            content = f.read()
        print("文件内容：")
        print(content)
        
        # 使用可选参数：判断是否打印长度
        if args.show_length:  # 直接用 args.长格式参数名 调用
            print(f"\n文件内容长度（字符数）：{len(content)}")
    except FileNotFoundError:
        print(f"错误：找不到文件 {args.file_path}")

if __name__ == "__main__":
    read_file()