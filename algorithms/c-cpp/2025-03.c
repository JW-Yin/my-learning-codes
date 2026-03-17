/*
编写一个C语言函数，接收一个字符串和两个整数K、N：
从字符串的第K个字符开始，连续插入N个字符 " "；若K超出字符串长度，则在末尾追加 "*"。
例如：输入字符串“HelloWorld”，K=6,N=3，输出“Hello***World”。
要求在主函数中输入字符串、K、N，调用函数处理后输出结果。
*/

#include <stdio.h>
#include <string.h>

void fun(char *str,int K,int N){
    int len=strlen(str);
    if(K <= len){
        // 先把K位置及其右面所有往后移动N个位置
        for(int i=0; len-i >= K-1 ;++i)
            str[len+N-i]=str[len-i];
        // 从K位置开始的N个位置全填充' '
        for(int i=0;i<N;++i)
            str[i+K-1]=' ';
    }else{
        for(int i=0;i<N;++i){
            str[len++]='*';
            str[len]='\0';
        }
    }
    printf("%s\n",str);
}
int main() {
    char str[100];
    int K,N;
    scanf("%s %d %d",str,&K,&N);
    fun(str,K,N);
    return 0;
}

/*
helloworld 1 3
helloworld 6 3
helloworld 100 3
*/