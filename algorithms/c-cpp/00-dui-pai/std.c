#include <stdio.h>
#include <string.h>

int main() {
    char str[100];  // 假设输入字符串长度不超过99
    int K, M;

    scanf("%s", str);
    scanf("%d %d", &K, &M);

    int len = strlen(str);
    // 如果要删除的太多了，就调整M为从K位到末尾的长度
    if ((K - 1) + M > len) {
        M = len - (K - 1);  
    }

    // 核心逻辑：将第K+M位及之后的字符，向前移动M位
    int start = K - 1;  // 转换为数组从0开始的索引
    for (int i = start + M; i <= len; i++) {
        str[i - M] = str[i];  // 包括移动结束符'\0'
    }

    // 输出结果
    printf("%s", str);
    return 0;
}
