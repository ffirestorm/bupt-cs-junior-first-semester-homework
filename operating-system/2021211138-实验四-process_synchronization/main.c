#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <pthread.h>
#include <semaphore.h>

#define BUFFER_SIZE 5  

sem_t empty, full, mutex;
typedef int buffer_item;  // 实验指导的定义
buffer_item buffer[BUFFER_SIZE];
int in = 0, out = 0;

int insert_item(buffer_item item) {
    // 插入item到缓冲区，成功返回0，否则返回-1
    buffer[in] = item;
    in = (in + 1) % BUFFER_SIZE;
    return 0;
}

int remove_item(buffer_item *item) {
    // 从缓冲区删除一个item，放入item，成功返回0，否则返回-1
    *item = buffer[out];
    out = (out + 1) % BUFFER_SIZE;
    return 0;
}

void *producer(void *arg) {
    while (1) {
        // 生产随机数
        buffer_item item = rand() % 100;

        sem_wait(&empty);
        sem_wait(&mutex);

        // 插入随机数
        if (insert_item(item) == 0) {
            fprintf(stderr, "Error: Buffer full\n");
        } else {
            printf("Produced: %d\n", item);
        }

        sem_post(&mutex);
        sem_post(&full);

        // 随机睡眠一段时间
        usleep(rand() % 1000000);
    }
}

void *consumer(void *arg) {
    while (1) {
        sem_wait(&full);
        sem_wait(&mutex);

        buffer_item item;

        // 从缓冲区删除一个数
        if (remove_item(&item) == 0) {
            fprintf(stderr, "Error: Buffer empty\n");
        } else {
            printf("Consumed: %d\n", item);
        }

        sem_post(&mutex);
        sem_post(&empty);

        // 随机睡眠一段时间
        usleep(rand() % 1000000);
    }
}

int main(int argc, char *argv[]) {
    // 解析命令行输入的信息
    if (argc != 4) {
        fprintf(stderr, "Usage: %s <sleep duration> <num producers> <num consumers>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    int sleep_duration = atoi(argv[1]);
    int num_producers = atoi(argv[2]);
    int num_consumers = atoi(argv[3]);

    // 初始化三个信号量
    sem_init(&empty, 0, BUFFER_SIZE);
    sem_init(&full, 0, 0);
    sem_init(&mutex, 0, 1);

    // 创建一定数量的生产者
    pthread_t producer_threads[num_producers];
    for (int i = 0; i < num_producers; ++i) {
        pthread_create(&producer_threads[i], NULL, producer, NULL);
    }

    // 创建一定数量的消费者
    pthread_t consumer_threads[num_consumers];
    for (int i = 0; i < num_consumers; ++i) {
        pthread_create(&consumer_threads[i], NULL, consumer, NULL);
    }

    // 主函数休息一会
    sleep(sleep_duration);

    // 在主函数醒来时终结这些线程
    for (int i = 0; i < num_producers; ++i) {
        pthread_cancel(producer_threads[i]);
    }

    for (int i = 0; i < num_consumers; ++i) {
        pthread_cancel(consumer_threads[i]);
    }

    // 销毁信号量
    sem_destroy(&empty);
    sem_destroy(&full);
    sem_destroy(&mutex);

    return 0;
}