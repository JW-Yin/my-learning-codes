#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>


int main() {
    // fork创建子进程
    pid_t pid = fork();

    if (pid < 0) {
        perror("fork失败");
        return 1;
    }

    // 子进程
    if (pid == 0) {
        printf("我是子进程，PID：%d，我爹是：%d\n", getpid(), getppid());
        
        // 睡5秒，让父进程先死掉
        sleep(5);
        
        // 父进程已经死了，再看爹是谁
        printf("我还是子进程，PID：%d，我现在的爹是：%d\n", getpid(), getppid());
        
        printf("子进程结束，自己终止啦！\n");
        exit(0);
    }
    // 父进程
    else {
        printf("我是父进程，PID：%d，我马上退出\n", getpid());
        // 父进程直接退出，不等子进程
        exit(0);
    }
}
