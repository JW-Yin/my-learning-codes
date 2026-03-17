/*
某人用100元买100只活鸡（公鸡5元1只，母鸡3元1只，小鸡1元3只）;
要求三种鸡都买到且钱刚好用完，编写程序求解。
*/


#include <stdio.h>

int main() {
    for(int i=1;i<=100/5;++i)
        for(int j=1;j<=100/3;++j)
            for(int k=3;k<=100;k+=3){
                if(i+j+k == 100 && i*5+j*3+k/3 == 100){
                    printf("公鸡=%d,母鸡=%d,小鸡=%d\n",i,j,k);
                }
            }
    return 0;
}