#include<stdio.h>
#include<sys/types.h>
#include<unistd.h>
#include<sys/wait.h>
int main()
{
    int num=0;
    printf("Please input the number: ");
    scanf("%d",&num);
    pid_t pid = fork();
    if(pid>0){//这个是父进程
        printf("Parent Process pid: %d\n",getpid());
        int status;
        waitpid(pid, &status, 0);
        if(WIFEXITED(status)){
            printf("child process has done, and exit.\n");
        }else{
            fprintf(stderr, "child process exit error.\n");
        }
        printf("father process has exit.\n");
    }else if(pid==0){//在子进程中输出序列
	    printf("Child Process pid: %d\n",getpid());
        while(num!=1)
        {
            printf("child process ouput the number: ");
            if(num%2==0)
            {
                num=num/2;
                printf("%d ",num);
            }
            else
            {
                num=3*num+1;
                printf("%d ",num);
            }
            printf("\n");
        }
    }else{
        perror("Fork falied.\n");
    }
    return 0;
}