/*
有n个人围成一圈，从1开始顺序排号。
从第一个人开始报数（从1到3报数），凡报到3的人退出圈子，问最后留下的是原来第几号的那位
*/

#include <stdio.h>

int main()
{

    int n, k=3;
    scanf("%d", &n);

    int ans = 0; // 当只剩下一个人时，编号为0（如果编号从0开始）
    for (int i = 2; i <= n; i++)
    {
        ans = (ans + k) % i;
    }
    // 如果编号从1开始，则 ans+1
    printf("%d", ans+1);

    return 0;
}
/*
循环队列模拟
int main(){
    int n; scanf("%d",&n);

    int a[n+1]; //循环队列
    for(int i=0;i<n;++i) a[i]=i+1; //所有人都先入循环队列

    int l=0,r=n;// l为队头下标，r为队尾下标的下一个位置

    for(int i=1; (r-l +n+1)%(n+1) > 1 ;i = (i == 3 ? 1: i+1)){
        if(i != 3) a[r]=a[l],l=(l+1)%(n+1),r=(r+1)%(n+1); // 放入队尾，同时队头出队
        else l=(l+1)%(n+1); //报3出队即可，无需入队
    }
    printf("%d",a[l]);
    return 0;
}
*/
