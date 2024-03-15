#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>

#define BUFSIZE 2048 // 共享内存大小

int main()
{
    printf("=============lab2 shared memory=============\n");
    printf("please input the number: ");
    int start;
    int seqLen = 0;
    scanf("%d", &start);

    // 创建共享内存对象
    const char *shmName = "collatz_shared_memory";
    int shmFd = shm_open(shmName, O_CREAT | O_RDWR, 0777);
    if (shmFd == -1)
    {
        perror("shm_open");
        return 1;
    }
    if (ftruncate(shmFd, BUFSIZE) == -1)
    {
        perror("ftruncate error.\n");
        return 1;
    }
    // 将共享内存映射到地址空间
    int *sharedSeq = (int *)mmap(NULL, BUFSIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shmFd, 0);
    if (sharedSeq == MAP_FAILED)
    {
        perror("mmap error.\n");
        return 1;
    }

    pid_t childPid = fork();
    if (childPid < 0)
    {
        perror("child process doesn't forked.\n");
        return 1;
    }
    else if (childPid == 0)
    {
        printf("child process start.\n");
        int index = 0;
        while (start != 1 && index < BUFSIZE)
        {
            printf("child: %d\n",start);
            sharedSeq[index++] = start;
            if (start % 2 == 0)
            {
                start = start / 2;
            }
            else
            {
                start = 3 * start + 1;
            }
        }
        sharedSeq[index] = 1;
        printf("child process has writen data to shared memory.\n");
        // 子进程退出状态设置为序列长度
        exit(index + 1);
    }
    else
    {
        int status;
        waitpid(childPid, &status, 0);
        if (WIFEXITED(status))
        {
            // 父进程接收子进程的序列退出长度
            seqLen = WEXITSTATUS(status);
            printf("child process has done, and exit.\n");
            printf("seqlength in father process: %d\n", seqLen);
            for (int i = 0; i < seqLen; i++)
            {
                printf("father process output the seq: %d\n", sharedSeq[i]);
            }
        }
        else
        {
            fprintf(stderr, "child process exit error.\n");
        }
    }
}

/*
seqLen 没有更新
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <fcntl.h>
#include <string.h>
#include <errno.h>

#define BUFSIZE 2048  // 共享内存大小
int seqLen = 0;       // 全局变量序列长度
void collatzSeq(int start, int* seq){
    int index = 0;
    printf("bufsize: %d\n",BUFSIZE);
    while(start != 1 && index < BUFSIZE){
        seq[index++] = start;
        if(start % 2 == 0){
            start = start / 2;
        }else{
            start = 3 * start + 1;
        }
    }
    seq[index] = 1;
    seqLen = index + 1;
    printf("%d\n", seqLen);
    printf("collatz finished\n");
}
int main(){
    printf("=============lab2 shared memory=============\n");
    printf("please input the number: ");
    int start = scanf("%d",&start);

    // 创建共享内存对象
    const char* shmName = "collatz_shared_memory";
    int shmFd=shm_open(shmName,O_CREAT | O_RDWR,0666);
    if (shmFd == -1) {
        perror("shm_open");
        return 1;
    }
    if(ftruncate(shmFd, sizeof(int)*BUFSIZE) == -1){
        perror("ftruncate error.\n");
        return 1;
    }
    // 将共享内存映射到地址空间
    int * sharedSeq = (int*)mmap(NULL, sizeof(int)*BUFSIZE, PROT_READ | PROT_WRITE, MAP_SHARED, shmFd, 0);
    if(sharedSeq == MAP_FAILED){
        perror("mmap error.\n");
        return 1;
    }
    pid_t childPid = fork();
    if(childPid < 0){
        perror("child process doesn't forked.\n");
        return 1;
    }else if (childPid == 0){
        printf("child process start.\n");
        collatzSeq(start,sharedSeq);
    }else{
        int status;
        waitpid(childPid, &status, 0);
        if(WIFEXITED(status)){
            printf("child process has done, and exit.\n");
            printf("%d\n", seqLen);
            for(int i = 0; i < seqLen;i++){
                printf("father process output the seq: %d\n",sharedSeq[i]);
            }
        }else{
            fprintf(stderr, "child process exit error.\n");
        }
    }

}

*/