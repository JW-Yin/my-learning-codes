# 硬编码脚本：计算两个数的和（固定计算 10 和 20）
import argparse

parser = argparse.ArgumentParser(description="计算命令行传入的两个数的和")
parser.add_argument("--a","-a",help="第一个数的值",default=10,type=int)
parser.add_argument("--b","-b",help="第二个数的值",default=20,type=int)
parser.add_argument("--d","-d",help="详细过程",action="store_true")

def add_two_numbers():
    args=parser.parse_args()
    a = (args.a)
    b = (args.b)
    result = a + b
    if args.d:
        print(f"{a} + {b} = {result}")
    else:
        print(a+b)

if __name__ == "__main__":
    add_two_numbers()