/*
有一分数序列：
\frac{2}{1},\frac{3}{2},\frac{5}{3},\frac{8}{5},\frac{13}{8},\frac{21}{13},\dots，
编写一个程序计算这个数列的前20项之和。
*/

#include<stdio.h>

int main(){
    double ret=0;
    int fenzi=2,fenmu=1;
    for(int i=0;i<20;++i){
        ret+=fenzi*1.0/fenmu;
        int t=fenzi;
        fenzi = fenzi + fenmu;
        fenmu = t;
    }
    printf("%lf",ret);
    return 0;
}