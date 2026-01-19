#include<stdio.h>

typedef struct{
    int id;
    char name[50];
    int scores[3];
    double avg;
}stu;

void quick_sort(stu *a, int low, int high){
    if(low < high){
        int i=low,j=high-1;
        stu bas=a[low];
        while(i<j){
            while(i<j && a[j].avg >= bas.avg) j--;
            if(i<j) a[i++]=a[j];
            while(i<j && a[i].avg <= bas.avg) i++;
            if(i<j) a[j--]=a[i];
        }
        a[i]=bas;
        quick_sort(a,low,i);
        quick_sort(a,i+1,high);
    }
}

signed main(){
    stu a[5];
    FILE*fp1=fopen("work-file/stud","rb");
    fread(a,sizeof(stu),5,fp1);

    quick_sort(a,0,5);

    for(int i=0;i<5;++i) 
        printf("%d %s %d %d %d %lf\n",a[i].id,a[i].name,a[i].scores[0],a[i].scores[1],a[i].scores[2],a[i].avg);

    FILE*fp2=fopen("work-file/stu_sort","wb");
    fwrite(a,sizeof(stu),5,fp2);

    fclose(fp1),fclose(fp2);
    return 0;
}