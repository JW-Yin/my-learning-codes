/*
定义一个结构体 Book ，包含属性：书号（int）、书名（字符串）、价格（float）。编写程序实现以下功能：
（1）输入5本书的信息存入结构体数组；
（2）按价格从高到低排序；
（3）输出排序后的图书信息。
要求排序过程封装为一个独立函数。
*/

#include <stdio.h>

typedef struct{
    int id;
    char name[100];
    float price;
}Book;

void quick_sort(Book *a,int low,int high){
    if(low < high){
        int i=low, j=high-1;
        Book bas=a[low];
        while(i < j){
            while(i<j && a[j].price >= bas.price) j--;
            if(i<j) a[i++] = a[j];

            while(i<j && a[i].price <= bas.price) i++;
            if(i<j) a[j--]=a[i];
        }
        a[i] = bas;
        quick_sort(a,low,i);
        quick_sort(a,i+1,high);
    }
}

signed main(){
    Book a[5];
    for(int i=0;i<5;++i)
        scanf("%d %s %f",&a[i].id,&a[i].name,&a[i].price);
    
    quick_sort(a,0,5);

    for(int i=0;i<5;++i)
        printf("%d %s %f\n",a[i].id,a[i].name,a[i].price);
    
    return 0;
}
/*
4 dd 45.6
1 aa 12.3
5 ee 56.7
3 cc 34.5
2 bb 23.4
*/