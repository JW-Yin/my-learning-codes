/*
编程打印出所有的“水仙花数”，所谓“水仙花数”是指一个三位数，其各位数字立方和等于该数本身。
例如：153是一个“水仙花数”
*/

# include<stdio.h>


int main(){
    for(int i=100;i<1000;++i){
        int a=i%10,b=i/10%10,c=i/100%10;
        if(a*a*a + b*b*b + c*c*c == i)
            printf("%d\n",i);
    }
    return 0;
}