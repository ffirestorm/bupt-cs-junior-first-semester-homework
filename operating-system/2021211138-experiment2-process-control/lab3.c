#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <ctype.h>
#include <sys/types.h>
#include <sys/mman.h>
#include <sys/wait.h>

#define MSG_SIZE 1024

int main() {
    // 0读 1写
    int pipeParent[2], pipeChild[2];
    char message[MSG_SIZE];

    // 创建两个管道
    if (pipe(pipeParent) == -1 || pipe(pipeChild) == -1) {
        perror("Pipe creation failed");
        exit(1);
    }

    pid_t child_pid = fork();

    if (child_pid == -1) {
        perror("Fork failed");
        exit(1);
    }

    if (child_pid == 0) {
        // 子进程 - 接收消息并修改大小写
        close(pipeParent[1]); // 关闭父进程管道的写端

        // 从父进程管道中读取消息
        read(pipeParent[0], message, MSG_SIZE);
        printf("Child process receive the message: %s\n",message);
        close(pipeParent[0]);

        // 修改消息大小写
        for (int i = 0; message[i] != '\0'; i++) {
            if (islower(message[i])) {
                message[i] = toupper(message[i]);
            } else if (isupper(message[i])) {
                message[i] = tolower(message[i]);
            }
        }

        // 发送修改后的消息到子线程管道
        close(pipeChild[0]);    //关闭子线程管道读端
        write(pipeChild[1], message, strlen(message) + 1);
        printf("Child send the message: %s\n",message);
        close(pipeChild[1]);
    } else {
        // 父进程 - 发送消息
        close(pipeParent[0]); // 关闭管道1的读端
        printf("Enter a message: ");
        fgets(message, MSG_SIZE, stdin);

        // 发送消息到管道1
        write(pipeParent[1], message, strlen(message) + 1);
        close(pipeParent[1]);
        close(pipeChild[1]); // 关闭管道2的写端
        // 从管道2中读取修改后的消息
        read(pipeChild[0], message, MSG_SIZE);
        close(pipeChild[0]);

        printf("Received modified message: %s", message);
    }

    return 0;
}