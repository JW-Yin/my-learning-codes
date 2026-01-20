/*
编程求一元二次方程ax²+bx+c=0的根x1和x2
*/

#include<stdio.h>
#include<math.h>

int main(){
    double a,b,c;
    scanf("%lf %lf %lf",&a,&b,&c);

    double fenzi1=b*(-1)+sqrt(b*b-4*a*c),fenzi2=b*(-1)-sqrt(b*b-4*a*c),fenmu=2*a;
    printf("x1=%lf\nx2=%lf",fenzi1/fenmu,fenzi2/fenmu);
    return 0;
}

/*
1 0 0
*/