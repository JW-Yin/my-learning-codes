#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/wait.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // 子进程
        printf("我是子进程 %d，我马上退出死翘翘\n", getpid());
        exit(0);  // 子进程立刻死掉
    } else {
        // 父进程
        printf("我是父进程 %d，我死不回收子进程\n", getpid());
        while (1) {  // 父进程死循环，就是不 wait()
            sleep(1);
        }
    }
}
