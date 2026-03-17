/*
输入某年某月某日，判断这一天是这一年的第几天?
*/

#include<stdio.h>

int main(){
    int year,month,day;
    scanf("%d.%d.%d",&year,&month,&day);
    int months[13]={-1,31,28,31,30,31,30,31,31,30,31,30,31};
    if((year % 4 == 0 && year % 100 != 0) || (year%400 == 0)) months[2]++;
    int ret=0;
    for(int i=1;i < month;++i) ret+=months[i];
    printf("%d",ret+day);  
    return 0;
}

