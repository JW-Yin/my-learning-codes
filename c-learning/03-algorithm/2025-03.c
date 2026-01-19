/*
编写一个C语言函数，接收一个字符串和两个整数K、N：
从字符串的第K个字符开始，连续插入N个字符 " "；若K超出字符串长度，则在末尾追加 "*"。
例如：输入字符串“HelloWorld”，K=6,N=3，输出“Hello***World”。
要求在主函数中输入字符串、K、N，调用函数处理后输出结果。
*/

#include<stdio.h>
#include<string.h>

void f1(char *str,int len, int n){
    for(int j=0;j<n;++j){
        str[len++]='*';
    }
    str[len]='\0';
}
void f2(char *str,int len, int K,int n){
    for(int j=len;j>=K;j--){
        str[j+n] = str[j];
    }
    for(int i=K,j=0;j<n;++j){
        str[i++]='*';
    }
}

int main(){
    int K,N;
    char str[100];
    scanf("%s %d %d",str,&K,&N);

    int len=strlen(str);
    if(len < K){
        f1(str,len,N);
    }else{
        f2(str,len,K-1,N);
    }
    printf("%s",str);
    return 0;
}

/*
helloworld 1 3
helloworld 6 3
helloworld 100 3
*/