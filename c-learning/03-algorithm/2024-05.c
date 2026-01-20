/*
实现5个学生信息的输入、排序、输出：
用结构体数组存储学生信息（包含学号、姓名）;
学号升序排序（排序功能用函数实现）；
主函数完成信息输入，调用排序函数后输出学生信息。
*/

#include <stdio.h>

typedef struct
{
    int id;
    char name[20];
} stu;

void quick_sort(stu *a, int low, int high)
{
    if (low < high)
    {
        int i = low, j = high - 1;
        stu bas = a[low];
        while (i < j)
        {
            while (i < j && a[j].id >= bas.id)
                j--;
            if (i < j)
                a[i++] = a[j];
            while (i < j && a[i].id <= bas.id)
                i++;
            if (i < j)
                a[j--] = a[i];
        }

        a[i] = bas;
        quick_sort(a, low, i);
        quick_sort(a, i + 1, high);
    }
}

int main()
{
    stu a[5];
    for (int i = 0; i < 5; ++i)
        scanf("%d %s", &a[i].id, a[i].name);
    quick_sort(a, 0, 5);
    for (int i = 0; i < 5; ++i)
        printf("%d %s\n", a[i].id, a[i].name);

    return 0;
}

/*
4 dd
1 aa
5 ee
3 cc
2 bb
*/