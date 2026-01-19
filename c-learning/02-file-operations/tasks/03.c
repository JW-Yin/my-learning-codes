#include <stdio.h>

signed main(){
    char ch;
    FILE *fp=fopen("work-file/test","w");

    do{
        scanf("%c", &ch);
        if(ch == '!') break;
        if(ch >= 'a' && ch <= 'z'){
            ch-=32;
        }
        fprintf(fp,"%c",ch);
    }while(1);
    
    fclose(fp);
    return 0;
}