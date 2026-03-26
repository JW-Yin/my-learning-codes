// # include<stdio.h>
// # include<string.h>

// int main(){
//     char s[100];
//     int K,M;
//     scanf("%s%d%d",s,&K,&M);
//     K--;
//     int len=strlen(s);

//     if(K+M > len) M=len-K;
//     for(int i=K+M;i<=len;++i){
//         s[i-M]=s[i];
//     }
//     printf("%s",s);
//     return 0;
// }

# include<stdio.h>
# include<string.h>

void f(char *s,int K,int M){
    int len = strlen(s);
    for(int i=K;i <= len;++i)
        //若是要粘贴过来的内容超出了字符串，补'\0'即可
        s[i]=(i+M)<=len?s[i+M]:'\0';
}

int main(){
    int K,M;
    char str[100];
    scanf("%[a-zA-Z] %d %d",str,&K,&M);
    f(str,K-1,M);
    printf("%s",str);
    return 0;
}