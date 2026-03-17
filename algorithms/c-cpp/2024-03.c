/*
编写一个函数，能够判断一个整数是否是素数，然后调用该函数求3到100之间的所有双素数。
（双素数：如果 p 和 q都是素数，且 q = p+ 2，则称 p和 q为双素数。例如3和5）。
*/

# include<stdio.h>


int f(int a){
    // 小于2的数不是素数
    if(a<2) return 0;
    for(int i=2;i*i <= a;++i)
        if(a % i == 0) return 0;
    return 1;
}

int main(){
    for(int i=4;i<100;++i){
        if(f(i) && f(i+2)){
            printf("%d\n",i);
        }
    }
    return 0;
}