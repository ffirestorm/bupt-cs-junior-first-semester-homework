#include <stdio.h>
#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
int maxNum, minNum;
double averageNum;
int number;
int * numberSeq;

void averageCal(){
    double sum = 0.0;
    for(int i = 0; i < number; i++){
        sum += numberSeq[i];
    }
    averageNum = sum / number;
    printf("\tthread1 calculate the average: %.2lf\n", averageNum);
    pthread_exit(NULL);
}

void minimum(){
    minNum = 65535;
    for(int i = 0; i < number; i++){
        if(minNum > numberSeq[i]){
            minNum = numberSeq[i];
        }
    }
    printf("\tthread2 find the minimum: %d\n", minNum);
    pthread_exit(NULL);
}

void maximum(){
    maxNum = -65535;
    for(int i = 0;i < number; i++){
        if(maxNum < numberSeq[i]){
            maxNum = numberSeq[i];
        }
    }
    printf("\tthread3 find the maxmum: %d\n", maxNum);
    pthread_exit(NULL);
}

int main(){
    pthread_t thread1, thread2, thread3;
    int ret;
    printf("Please enter the number: ");
    scanf("%d",&number);
    numberSeq = (int*)malloc(sizeof(int)*number);
    memset(numberSeq, 0, sizeof(numberSeq));
    for(int i =0; i < number; i++){
        printf("please input the %d number: ",i+1);
        scanf("%d",&numberSeq[i]);
    }

    // 创建线程
    ret = pthread_create(&thread1, NULL, (void *)averageCal, NULL);
    if(ret != 0){
        printf("Create thread1 error.\n");
        return -1;
    }
    ret = pthread_create(&thread2, NULL, (void *)minimum, NULL);
    if(ret != 0){
        printf("Create thread1 error.\n");
        return -1;
    }
    ret = pthread_create(&thread3, NULL, (void *)maximum, NULL);
    if(ret != 0){
        printf("Create thread1 error.\n");
        return -1;
    }

    pthread_join(thread1, NULL);
    pthread_join(thread2, NULL);
    pthread_join(thread3, NULL);
    printf("The parent get the result\n\taverage: %.2lf\n\tminimum: %d\n\tmaxmum:%d\n",averageNum,minNum,maxNum);

    free(numberSeq);
    return 0;
}