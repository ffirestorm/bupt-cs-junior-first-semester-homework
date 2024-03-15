#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#define TOTAL_INSTRUCTIONS 100
#define PAGE_SIZE 10
#define PAGE_COUNT 10

int pageTableSize;

// 在页表查看是否缺页
int findPage(int pageTable[], int pageNum){
    for(int i = 0 ; i < pageTableSize; i++){
        if(pageTable[i] == pageNum){
            return i;
        }
    }
    return -1;
}
// 找到OPT要置换的那个元素下标，并返回
int findOPT(int pageTable[], int pages[], int currentIndex){
    // 在页表中，找到每个元素下一次要访问的距离
    int distance[pageTableSize];
    for(int i = 0 ; i < pageTableSize; i++){
        int j;
        for(j = currentIndex+1; j < TOTAL_INSTRUCTIONS; j++){
            // 找到了
            if(pageTable[i] == pages[j])
                break;
        }
        distance[i] = j - currentIndex;
    }
    // 比较距离，选择最大的
    int maxDistance = 0, retIndex = 0;
    for(int i = 0 ; i < pageTableSize; i++){
        if(maxDistance < distance[i]){
            maxDistance = distance[i];
            retIndex = i;
        }
    }
    return retIndex;
}
// 刷新lru的时间
void flushLruTime(int lruTime[]){
    for(int i = 0;i < pageTableSize; i++){
        lruTime[i]++;
    }
}
// 找到lru时间最大的那个表项
int findLruMax(int lruTime[]){
    int max = -1;
    int retIndex = 0;
    for(int i = 0;i < pageTableSize; i++){
        if(lruTime[i] > max){
            max = lruTime[i];
            retIndex = i;
        }       
    }
    return retIndex;
}
// 先进先出页面置换
double fifo(int pages[]){
    int pageTable[pageTableSize];
    memset(pageTable, -1, sizeof(pageTable));
    int index = 0;
    int countPageFault = 0;
    for(int i = 0; i < TOTAL_INSTRUCTIONS; i++){
        // 模拟访问页表--缺页
        if(findPage(pageTable, pages[i]) == -1){
            // 没找着--缺页
            countPageFault++;
            pageTable[index] = pages[i];
            index = (index + 1) % pageTableSize;
        }
    }
    double faultRate = 100*(double)countPageFault/(double)TOTAL_INSTRUCTIONS;
    printf("FIFO页面置换的缺页数为：%d, 缺页率是:%.2lf%%\n",countPageFault, faultRate);
    return faultRate;
}
// LRU页面置换
double lru(int pages[]){
    int lruTime[pageTableSize], pageTable[pageTableSize];
    memset(pageTable, -1, sizeof(pageTable));
    int lruPageFaultCount = 0;
    for(int i = 0; i < pageTableSize; i++){
        lruTime[i] = 100;
    }
    for(int i = 0 ; i < TOTAL_INSTRUCTIONS; i++){
        if(findPage(pageTable, pages[i]) == -1){
            // 没找着
            int victimIndex = findLruMax(lruTime);
            pageTable[victimIndex] = pages[i];
            lruTime[victimIndex] = 0;
            lruPageFaultCount++;
        }else{
            // 找着了
            int index = findPage(pageTable, pages[i]);
            lruTime[index] = 0;
        }
        flushLruTime(lruTime);
    }
    double faultRate = 100*(double)lruPageFaultCount/(double)TOTAL_INSTRUCTIONS;
    printf("LRU 页面置换算法的缺页次数是：%d, 缺页率是:%.2lf%%\n", lruPageFaultCount, faultRate);
    return faultRate;
}
// OPT置换，输出缺页信息
double opt(int pages[]){
    int pageTable[pageTableSize];
    int optCount = 0;
    memset(pageTable, -1, sizeof(pageTable));
    for(int i = 0; i < TOTAL_INSTRUCTIONS; i++){
        if(findPage(pageTable, pages[i]) == -1){
            int victimIndex = findOPT(pageTable, pages, i);
            pageTable[victimIndex] = pages[i];
            optCount ++;
        }
    }
    double faultRate = 100*(double)optCount/TOTAL_INSTRUCTIONS;
    printf("OPT 页面置换算法的缺页次数是：%d, 缺页率是:%.2lf%%\n", optCount, faultRate);
    return faultRate;
}
// 按照实验要求生成地址及页面流
void generateAddressPages(int instructions[], int pages[], int seed) {
    srand(time(NULL)+seed);
    int currentAddress = 0;
    for (int i = 0; i < TOTAL_INSTRUCTIONS; i++) {
        double probability = ((double)rand() / RAND_MAX) * 100;
        if (probability < 70) {
            // 70%的概率选择顺序执行
            currentAddress++;
        } else if (probability < 80) {
            // 10%的概率选择在前地址部分均匀分布
            currentAddress = rand() % (i == 0 ? 1 : i);
        } else {
            // 20%的概率选择在后地址部分均匀分布
            currentAddress = (rand() % (TOTAL_INSTRUCTIONS - i + 1)) + currentAddress + 1;
        }
        instructions[i] = currentAddress;
    }
    for(int i = 0; i < TOTAL_INSTRUCTIONS; i++){
        pages[i] = instructions[i] / PAGE_SIZE;
    }
}

int main() {
    int instructions[TOTAL_INSTRUCTIONS], pages[TOTAL_INSTRUCTIONS];
    double fifoSum = 0, lruSum = 0, optSum = 0;
    int total;
    printf("请输入想要实验的次数: ");
    scanf("%d", &total);
    printf("请输入想要测试的页表大小: ");
    scanf("%d", &pageTableSize);
    for(int i = 0; i < total; i++){
        printf("第 %d 次：\n", i+1);
        generateAddressPages(instructions, pages, i);
        double fifoRate = fifo(pages);
        double lruRate = lru(pages);
        double optRate = opt(pages);
        fifoSum += fifoRate;
        lruSum += lruRate;
        optSum += optRate;
    }
    double avgFifoRate = fifoSum / total ;
    double avgLruRate = lruSum / total;
    double avgOptRate = optSum / total;

    printf("经过 %d 实验\nFIFO的缺页率平均值为:\t%.2lf\nLRU的缺页率平均值为:\t%.2lf\nOPT的缺页率平均值为:\t%.2lf\n",total, avgFifoRate, avgLruRate, avgOptRate);
    printf("请输入想要测试页表的大小, 我们将测试该页表以及比它大1的页表大小: ");
    scanf("%d", &pageTableSize);
    for(int i = 0 ;i < total ; i++){
        printf("============第 %d 次==========\n", i+1);
        generateAddressPages(instructions, pages, i);
        printf("页表大小为：%d\n", pageTableSize);
        double a = fifo(pages);
        double c = lru(pages);
        double e = opt(pages);
        pageTableSize++;
        printf("页表大小为：%d\n", pageTableSize);
        double b = fifo(pages);
        double d = lru(pages);
        double f = opt(pages);
        pageTableSize--;
        if( b-a > 1e-4 || d-c >1e-4 || f-e > 1e-4)
            break;
    }
    return 0;
}