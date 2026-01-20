/*
有三个开放的兔子窟A、B、C串门过程如下：
A号兔子窟派出与B号当前兔子数相等的兔子，跑去B号兔子窟；
接着B号兔子窟派出与C号当前兔子数相等的兔子，跑去C号兔子窟；
最后C号兔子窟派出与A号当前兔子数相等的兔子，跑去A号兔子窟；
最终三个兔子窟的兔子数量均为16只。
要求：用C语言程序设计，求出三个兔子窟一开始各自的兔子数量。
*/

# include<stdio.h>

// 直接逆推
int main(){
    int a=16,b=16,c=16;
    a/=2;
    c+=a;

    c/=2;
    b+=c;

    b/=2;
    a+=b;
    printf("the number of Rabbits A: %d,\nthe number of Rabbits B: %d,\nthe number of Rabbits C: %d",a,b,c);
    return 0;
}

/*
暴力枚举

int f(int a,int b,int c){
    a-=b,b+=b;
    b-=c,c+=c;
    c-=a,a+=a;
    if(a == b && a == c && a == 16) return 1;
    return 0;
}

int main(){
    
    for(int a=0;a<50;++a)
        for(int b=0;b<50;++b)
            for(int c=0;c<50;++c){
                if(a+b+c == 16*3 && f(a,b,c)){
                    printf("the number of Rabbits A: %d,\nthe number of Rabbits B: %d,\nthe number of Rabbits C: %d",a,b,c);
                }
            }
    return 0;
}
*/
