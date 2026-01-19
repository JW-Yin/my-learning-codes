#include<stdio.h>

typedef struct{
    int id;
    char name[50];
    int scores[3];
    double avg;
}stu;

signed main(){
    stu a[5];
    for(int i=0;i<5;++i){
        scanf("%d %s %d %d %d",&a[i].id,a[i].name,&a[i].scores[0],&a[i].scores[1],&a[i].scores[2]);
        a[i].avg=0;
        for(int j=0;j<3;++j)
            a[i].avg+=a[i].scores[j];
        a[i].avg/=3;
    }
    FILE *fp=fopen("work-file/stud","wb");

    fwrite(a,sizeof(stu),5,fp);

    fclose(fp);
    return 0;
}

/*
4 ZhangSan 44 55 66
1 LiMing 11 22 33
3 LiLei 33 44 55
5 XiaoBai 55 66 77
2 LiHua 22 33 44
*/