/*
输入一个以回车结束的字符串（不超过10个字符），将其中的数字字符取出组成一个整数后输出其余字符组成一个新的字符串输出。
例：输入“5ab3c4d8h2”，输出整数53482和字符串“abcdh”。
*/

#include <stdio.h>

int main() {
    char str[20]="\0",ch;
    int str_len=0;
    while((ch=getchar()) != '\n'){
        str[str_len++]=ch;
        str[str_len]='\0';
    }
    long long int ans=0,offset=0;
    for(int i=0;i<=str_len;++i){
        if(str[i] >= '0' && str[i] <= '9'){
            ans*=10,ans+=str[i]-'0';
            offset++;
        }else{
            str[i-offset]=str[i];
        }
    }
    str_len-=offset;
    printf("%lld,%s",ans,str);
    return 0;
}

/*
5ab3c4d8h2
ab
12
a1
1a
*/