/*
判断s1字符串中是否包含s2字符串。如："china123"包含"na12"，但不包含"ab
*/

#include<stdio.h>
#include<string.h>

int main() {
    char s1[101], s2[101];
    scanf("%s %s", s1, s2);
    
    int len1 = strlen(s1), len2 = strlen(s2);
    
    // 特殊情况处理
    if (len2 == 0) {
        printf("YES");  // 空串是所有字符串的子串
        return 0;
    }
    
    // 计算next数组
    int next[101] = {-1};
    int i = 0, j = -1;
    
    while (i < len2) {
        if (j == -1 || s2[i] == s2[j]) {
            i++;
            j++;
            next[i] = j;
        } else {
            j = next[j];
        }
    }
    
    // KMP匹配
    i = 0, j = 0;
    while (i < len1 && j < len2) {
        if (j == -1 || s1[i] == s2[j]) {
            i++;
            j++;
        } else {
            j = next[j];
        }
    }
    
    // 输出结果
    if (j == len2) {
        printf("YES");
    } else {
        printf("NO");
    }
    
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