/*
编写C语言函数，接收字符串和两个整数K、N：从字符串第K个字符开始插入N个""；若K超出字符串长度则在末尾追加N个""。主函数输入参数并调用函数输出结果。
*/

#include <stdio.h>
#include <string.h>


void fun(char *str,int K,int N){
    int len=strlen(str);
    if(K <= len){
        K--;
        char s[100];for(int i=0;K+i <= len;++i) s[i]=str[K+i];
        int len2=strlen(str);

        for(int i=K;i<K+N;++i) str[i]=' ';

        for(int i=K+N,j=0;j<=len2;){
            str[i++]=s[j++];
        }
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
    // FILE *f=fopen("./test","w");
    // fprintf(f,"%s",str);
    return 0;
}