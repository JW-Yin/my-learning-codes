/*
编程打印出所有的“水仙花数”，水仙花数是指一个三位数，其各位数字立方和等于该数本身。
*/

#include <stdio.h>

int main() {
    for(int i=100;i<=999;++i){
        int a=i%10;
        int b=i/10%10;
        int c=i/100%10;
        if(a*a*a + b*b*b + c*c*c == i)
            printf("%d\n",i);
    }
    return 0;
}