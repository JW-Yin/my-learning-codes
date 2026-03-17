#include <stdio.h>

typedef struct
{
    int id;
    char name[50];
    int scores[3];
    double avg;
} stu;

void insert(stu *a,int n,stu *t){
    int pos=-1;
    for (int i = 0; i < 5; ++i)
        if(a[i].avg > t->avg){
            pos=i;
            break;
        }
    
    if(pos != -1){
        for(int i=n;i-1 >= pos;--i)
            a[i]=a[i-1];
        a[pos]=*t;
    }
}

signed main()
{
    stu t;
    scanf("%d %s %d %d %d", &t.id, t.name, &t.scores[0], &t.scores[1], &t.scores[2]);
    t.avg = 0;
    for (int j = 0; j < 3; ++j)
        t.avg += t.scores[j];
    t.avg /= 3;

    stu a[5+1];
    FILE *fp = fopen("work-file/stu_sort", "rb");
    fread(a, sizeof(stu), 5, fp);

    for (int i = 0; i < 5; ++i)
        printf("%d %s %d %d %d %lf\n", a[i].id, a[i].name, a[i].scores[0], a[i].scores[1], a[i].scores[2], a[i].avg);

    insert(a,5,&t);

    FILE*fp1=fopen("work-file/stu_sort1","wb");
    fwrite(a,sizeof(stu),6,fp1);

    printf("After insert:\n");
    for (int i = 0; i < 6; ++i)
        printf("%d %s %d %d %d %lf\n", a[i].id, a[i].name, a[i].scores[0], a[i].scores[1], a[i].scores[2], a[i].avg);

    fclose(fp),fclose(fp1);
    return 0;
}

/*
99 Bai 44 44 44
*/