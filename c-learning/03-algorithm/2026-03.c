/*
判断s1字符串中是否包含s2字符串。如："china123"包含"na12"，但不包含"ab
*/

#include<stdio.h>
#include<string.h>

int main(){
    char s1[100+1],s2[100+1];
    scanf("%s %s",s1,s2);

    int len1=strlen(s1),len2=strlen(s2);
    
    int next[100+1]={-1,0};
    for(int i=2;i<len2;++i){
        int tag=i-1;
        while(1){
            if(tag < 0 || s2[i] == s2[tag]){
                next[i]=next[tag]+1;
                break;
            }else tag = next[tag];
        }
    }

    for(int i=0,j=0 ;i<=len1;){
        if(j == len2) {
            printf("YES");
            return 0;
        } 
        if(i == len1 )break;
        if(j == -1 || s1[i] == s2[j]) i++,j++;
        else j=next[j];
    }
    printf("NO");
    return 0;
}

/*
abcdef a
abcdef f
china123 na12
china123 ab
*/

/*
暴力枚举
int main(){
    char s1[100],s2[100];
    scanf("%s %s",s1,s2);

    int len1=strlen(s1),len2=strlen(s2);
    for(int i=0;i < len1;++i){
        int t=i;
        for(int j=0;j < len2;++j)
            if(s1[t] == s2[j]) t++;
            else break;
        if(t== i+len2){
            printf("YES");
            return 0;
        }
    }
    printf("NO");
    return 0;
}
*/