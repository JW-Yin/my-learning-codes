#include<stdio.h>

signed main(){
    FILE *fp=fopen("example.txt", "w+");
    // 向文件写入 abc
    fprintf(fp,"%s","abc");

    // 将文件指针重新定位到文件开头 (同时会触发刷盘机制，强制写缓冲区入磁盘)
    fseek(fp,0,SEEK_SET);

    char str[100];
    fscanf(fp,"%s",str);

    printf("Read from file: %s\n", str);
    fclose(fp);
    return 0;
}