/*
编写一个程序，把磁盘文件a.txt中的信息复制到磁盘文件b.txt
*/

#include <stdio.h>

int main()
{
    FILE *fp = fopen("a.txt", "rb"), *fp1 = fopen("b.txt", "wb");

    if (fp == NULL)
    {
        return 1;
    }
    if (fp1 == NULL)
    {
        fclose(fp); // 关键：关闭已打开的fp，避免泄漏
        return 1;
    }

    char ch;
    while (fread(&ch, 1, 1, fp) == 1)
    {
        fwrite(&ch, 1, 1, fp1);
    }

    fclose(fp), fclose(fp1);
    return 0;
}
/*
应该用二进制读写，而非字符型读写
int main(){
    FILE *fp=fopen("a.txt","r"),*fp1=fopen("b.txt","w");
    char ch;
    while(fscanf(fp,"%c",&ch) != EOF){
        fprintf(fp1,"%c",ch);
    }
    fclose(fp),fclose(fp1);
    return 0;
}
*/
