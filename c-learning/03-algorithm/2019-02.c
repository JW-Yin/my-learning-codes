/*
某人用100元买100只活鸡（公鸡5元1只，母鸡3元1只，小鸡1元3只）;
要求三种鸡都买到且钱刚好用完，编写程序求解。
*/
# include<stdio.h>

int main(){
    for(int a=1;a<100;++a)
        for(int b=1;b<100;++b)
            for(int c=1;c<100;++c)
                if(c%3 == 0 && a*5 + b*3 + c/3 == 100 && a+b+c == 100)
                    printf("rooster: %d,\nhen: %d,\nchick: %d\n",a,b,c);
    return 0;
}