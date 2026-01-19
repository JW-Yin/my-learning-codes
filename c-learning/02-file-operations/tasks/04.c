#include<stdio.h>
#include<stdlib.h>
const int MAXSIZE= 1e5+1;

void quick_sort(char *a, int low, int high){
    if(low < high){
        int i=low,j=high-1;
        char bas=a[low];
        while(i < j){
            while(i<j && a[j] >= bas) j--;
            if(i<j) a[i++]=a[j];
            while(i<j && a[i] <= bas) i++;
            if(i<j) a[j--]=a[i];
        }
        a[i]=bas; //将 bas 放回正确位置

        quick_sort(a,low,i);
        quick_sort(a,i+1,high);
    }
}
int len(char *a){
    int ret=0;
    for(int i=0;a[i] != '\0';++i) ret++;
    return ret;
} 

signed main(){
    char *c;
    c=(char *)calloc(MAXSIZE,sizeof(char));

    FILE *A=fopen("work-file/A","r"),*B=fopen("work-file/B","r"),*C=fopen("work-file/C","w");
    
    fscanf(A,"%s",c);
    fscanf(B,"%s",c+len(c));

    printf("%s\n",c);

    quick_sort(c,0,len(c));

    printf("%s\n",c);
    
    fprintf(C,"%s",c);

    // 处理好善后工作
    fclose(A),fclose(B),fclose(C);
    free(c);
    return 0;
}