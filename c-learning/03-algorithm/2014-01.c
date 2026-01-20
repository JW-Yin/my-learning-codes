/*
输入一个以回车结束的字符串（不超过10个字符），将其中的数字字符取出组成一个整数后输出其余字符组成一个新的字符串输出。
例：输入“5ab3c4d8h2”，输出整数53482和字符串“abcdh”。
*/

#include<stdio.h>
#include<string.h>

int main() {
    char str[20];
    long num = 0;
    
    scanf("%s", str);
    int len=strlen(str);
    for(int i=0,j=0;i <= len;++i){
        if(str[i] >= '0' && str[i] <= '9'){
            num=num*10 + str[i]-'0';
            j++;
        }else str[i-j]=str[i];
    }
    
    printf("%ld\n%s\n", num, str);
    
    return 0;
}

/*
5ab3c4d8h2
ab
12
a1
1a
*/