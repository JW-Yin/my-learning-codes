#include <stdio.h>
#include <stdlib.h> 
#include <time.h>    

int get_random_number(int a,int b){
    return rand()%(b-a+1)+a;
}

int main() {
    srand((unsigned int)time(NULL) ^ (unsigned int)getpid());

    
    int str_len = get_random_number(5,10);
    char str[str_len+10];for(int i=0;i<str_len;++i)str[i]=get_random_number('A','Z');str[str_len]='\0';
    int K=get_random_number(0,15),N=get_random_number(0,15);

    // FILE *fp=fopen("./input.txt","w");
    // fprintf(fp,"%s %d %d",str,K,N);
    // fclose(fp);

    printf("%s %d %d",str,K,N);
    return 0;
}
