/*
字符串裁剪拼接功能：
用户输入一段字符串、K、M，实现“从字符串第K位字符开始，删去M位字符，再拼接剩余部分”；
用函数实现该功能（示例：输入字符串"I am a new student"、K=7、M=4，输出"I am a student") ;
主函数完成字符串、K、M的输入，调用函数后输出结果。
*/

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
    scanf("%[a-zA-Z ] %d %d",str,&K,&M);
    f(str,K,M);
    printf("%s",str);
    return 0;
}

/*
I am a new student 7 4
I am a new student 0 99
I am a new student 99 0
I am a new student 0 1
I am a new student 17 1
*/