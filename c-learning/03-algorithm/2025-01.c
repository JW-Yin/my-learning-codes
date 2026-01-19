/*
某人有100元零钱，需兑换成1元、2元、5元三种面值的硬币，要求每种面值至少有一枚，且硬币总数不超过30枚。
请编写C语言程序，输出所有可能的兑换方案
*/

#include <stdio.h>

signed main(){

    for(int i=1;i<100;++i)
        for(int j=1;j<50;++j)
            for(int k=1;k<20;++k){
                if(i*1+j*2+k*5 == 100 && i+j+k <=30){
                    printf("%d one-yuan coins, %d two-yuan coins, %d five-yuan coins\n",i,j,k);
                }
            }

    return 0;
}
