#include <stdio.h>

typedef struct
{
    int id;
    char name[20];
} stu;

signed main()
{
    stu s1 = {1001, "zhangsan"};
    // 以二进制读写方式打开文件
    FILE *fp = fopen("example.txt", "wb+");

    fwrite(&s1, sizeof(stu), 1, fp);

    // 将文件指针重新定位到文件开头，同时会触发刷盘机制，强制写缓冲区入磁盘
    fseek(fp, 0, SEEK_SET);

    stu s2;

    fread(&s2, sizeof(stu), 1, fp);

    printf("id: %d, name: %s\n", s2.id, s2.name);

    fclose(fp);
    return 0;
}