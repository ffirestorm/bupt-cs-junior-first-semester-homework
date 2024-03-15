#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>

int M,K,N;   // C的行数、中间数、C的列数
int **A, **B, **C;  //矩阵，A、B为乘数，C为结果
pthread_t ** threads;   // worker threads

struct v
{
    int row;
    int column;
};

void * work(void * arg){
    struct v * data = (struct v *)arg;
    int sum = 0;
    for(int i = 0; i < N; i++){
        printf("(%d,%d): ",data->row,data->column);
        printf("sum = %d, A[%d][%d]=%d, B[%d][%d]=%d\n", sum, data->row,i,A[data->row][i],i,data->column,B[i][data->column]);
        sum += A[data->row][i] * B[i][data->column];
    }

    C[data->row][data->column] = sum;
    printf("%d,%d: %d\n",data->row,data->column,sum);
    free(data);
    pthread_exit(NULL);
}
// 检查矩阵格式是否正确
int checkMatrixFormat(FILE *file) {
    int M, N, num;
    if (fscanf(file, "%d %d %d", &M, &K, &N) != 3) {
        fprintf(stderr, "Error: Unable to read matrix dimensions from the input file.\n");
        return 0;
    }

    int expectedNumbers = K*(M + N);
    int actualNumbers = 0;

    while (fscanf(file, "%d", &num) == 1) {
        actualNumbers++;
    }

    if (actualNumbers != expectedNumbers) {
        fprintf(stderr, "Error: The number of elements in the matrix does not match the specified dimensions (M=%d, N=%d).\n", M, N);
        printf("%d\n",actualNumbers);
        return 0;
    }
    printf("File format right.\n");
    return 1;
}

int main(int argc, char *argv[]){
    // 从文件读入M、N以及矩阵A、B的值
    FILE * file = fopen(argv[1], "r");
    if(file == NULL){
        perror("Error opening input file.");
        return -1;
    }
    printf("open file success.\n");
    if(!checkMatrixFormat(file)){
        return -1;
    }
    // 检查完重定位
    fseek(file, 0, SEEK_SET);
    fscanf(file, "%d %d %d", &M, &K, &N);

    // 分配内存，并读入矩阵A和矩阵B
    A = (int **)malloc(M * sizeof(int *));
    B = (int **)malloc(K * sizeof(int *));
    C = (int **)malloc(M * sizeof(int *));
    threads = (pthread_t **)malloc(M * sizeof(pthread_t *));

    printf("malloc success.\n");
    for(int i = 0; i < M; i++){
        A[i] = (int *)malloc(K * sizeof(int));
        C[i] = (int *)malloc(N * sizeof(int));
        threads[i] = (pthread_t *)malloc(N * sizeof(pthread_t));

        for(int j = 0; j < K; j++){
            fscanf(file, "%d", &A[i][j]);
            printf("%d\t",A[i][j]);
        }
        printf("\n");
    }
    printf("A load success.\n");

    for(int i =0; i < K; i++){
        B[i] = (int *)malloc(N * sizeof(int));
        for(int j = 0; j < N; j++){
            fscanf(file, "%d", &B[i][j]);
            printf("%d\t",B[i][j]);
        }
        printf("\n");
    }
    printf("B load success.\n");
    fclose(file);
    // 创建 M * N 个工作线程
    for(int i = 0; i < M; i++){
        for(int j = 0; j < N; j++){
            struct v * data = (struct v *) malloc (sizeof(struct v));
            data->row = i;
            data->column = j;
            // 通过data创建工作线程
            pthread_create(&threads[i][j], NULL, work, data);
        }
    }

    // pthread_join 函数等待所有线程完成
    for (int i = 0; i < M; i++){
        for(int j = 0; j < N; j++){
            pthread_join(threads[i][j], NULL);
        }
    }

    // 打印结果矩阵C
    printf("=============All threads has done, Result C :=================\n");
    for(int i = 0; i < M; i++){
        for(int j = 0; j < N; j ++){
            printf("%d\t",C[i][j]);
        }
        printf("\n");
    }

    // 擦屁股
    for(int i = 0; i < M; i++){
        free(A[i]);
        free(C[i]);
        free(threads[i]);
    }
    for(int j = 0; j < K; j++){
        free(B[j]);
    }
    free(A);
    free(B);
    free(C);
    free(threads);
    return 0;
}