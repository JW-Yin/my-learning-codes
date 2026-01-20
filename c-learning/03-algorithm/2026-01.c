/*
程实现输入三角形的边长a,b,C，求三角形的面积area
*/

#include<stdio.h>
#include<math.h>
int main(){
    double a,b,c; scanf("%ld %lf %lf",&a,&b,&c);
    double p= (a+b+c)/2;
    printf("%lf",sqrt(p*(p-a)*(p-b)*(p-c)));
    return 0;
}