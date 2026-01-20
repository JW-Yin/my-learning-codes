/*
一个数如果恰好等于它的因子之和，这个数就称为“完数”。
例如6=1十2十3。编程找出1000以内的所有完数
*/

#include<stdio.h>


int main(){
    for(int i=2;i<1000;++i){
        int sum=1;
        for(int j=2;j*j <= i;++j){
            if(i%j == 0){
                sum+=j;
                // 首先得能除尽，此时的另一半才是因子
                if(j*j != i) sum+=i/j;
            }
        }
        if(sum == i) printf("%d\n",i);
    }
    return 0;
}