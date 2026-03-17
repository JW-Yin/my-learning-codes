/*
编程求一元二次方程ax²+bx+c=0的根x1和x2
*/

#include <stdio.h>
#include <math.h>

int main() {
    double a,b,c; scanf("%lf %lf %lf",&a,&b,&c);
    if(a == 0){
        printf("非法方程");
        return 0;
    } 
    double derta=b*b-4*a*c;
    if(derta < 0) printf("无解");
    else{
        double x1=(b*(-1) + sqrt(derta))/(2*a);
        double x2=(b*(-1) - sqrt(derta))/(2*a);
        if(fabs(derta) < 1e-12) printf("有唯一解x1=x2=%lf",x1);
        else{
            printf("x1=%lf,x2=%lf",x1,x2);
        }
    }
    return 0;
}

/*
1 0 0
*/