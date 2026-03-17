#!/bin/bash

gcc gen.c -o gen
gcc std.c -o std
gcc test.c -o test

cnt=1
max_cnt=1000

while [ $cnt -le $max_cnt ]; do
    echo "------------------------------"
    echo "正在测试第 $cnt 组用例..."

    # 1. 生成测试用例
    ./gen > in.txt
    # ✅ 新增：输出in.txt的内容
    echo "=== 测试用例（in.txt） ==="
    cat in.txt
    echo

    # 2. 运行标程
    ./std < in.txt > std_out.txt
    # ✅ 新增：输出std_out.txt的内容
    echo "=== 标程输出（std_out.txt） ==="
    cat std_out.txt
    echo

    # 3. 运行待测程序
    ./test < in.txt > test_out.txt

    # 4. 对比
    if diff std_out.txt test_out.txt > /dev/null; then
        echo "✅ 第 $cnt 组用例通过！"
    else
        echo "❌ 第 $cnt 组用例出错！"
        echo "错误用例已保存到 in.txt，标程输出在 std_out.txt，待测输出在 test_out.txt"
        exit 1
    fi

    cnt=$((cnt + 1))
done

echo "✅ 所有 $max_cnt 组用例全部通过！"
