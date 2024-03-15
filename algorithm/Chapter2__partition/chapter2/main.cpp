#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#define STRAIGHT_SORT_LENGTH 50
using namespace std;

int recursionDepth = 0;

class BaseStation{
public:
    int ENODEBID;
    double K_DIST;
    BaseStation(){
        ENODEBID = -1;
        K_DIST = 0;
    }
};
/**
 * @brief 简单的数组内交换函数
 * 
 * @param a 数组
 * @param i 待交换的元素下标
 * @param j 待交换的元素下标
 */
void swapBaseStations(vector<BaseStation> & a, int i, int j) {
    BaseStation temp = a[i];
    a[i] = a[j];
    a[j] = temp;
}

/**
 * @brief 根据快排修改的划分基准算法，可传入基准数据
 * 
 * @param arr 待更新数组
 * @param low 数组低位
 * @param high 数组高位
 * @param x 划分基准
 * @return int 划分基准更新完的位置
 */
int partition(vector<BaseStation>& arr, int low, int high, const BaseStation& x = BaseStation()){
    // 在数组中找到划分基准
    for(int i = 0; i <= high;i++){
        if(x.ENODEBID == arr[i].ENODEBID){
            swapBaseStations(arr, i, high);
            break;
        }
    }
    // 将划分基准放到末尾
    BaseStation pivot = arr[high];
    int i = low -1;
    for (int j = low; j <= high; j++){
        if(arr[j].K_DIST < pivot.K_DIST){
            i++;
            swapBaseStations(arr, i, j);
        }
    }
    swapBaseStations(arr, i+1, high);
    return i + 1;
}

/**
 * @brief 基于递归的简单快排
 * 
 * @param arr 待排序的数组
 * @param low 待排序的区间低位
 * @param high 待排序的区间高位
 */
void quickSort(vector<BaseStation>& arr, int low, int high) {
    if (low < high) {
        int pivotIndex = partition(arr, low, high);

        quickSort(arr, low, pivotIndex - 1);
        quickSort(arr, pivotIndex + 1, high);
    }
}

/**
 * @brief 一分为三的线性时间选择，找第k小元素
 * 
 * @param a 待查找的数组
 * @param p 查找的数组区间的低位
 * @param r 高位
 * @param k 找第几小，比如k=1就是找最小的
 * @return BaseStation 返回第k小的数据
 */
BaseStation select(vector<BaseStation>a, int p, int r, int k){
    // 查找区间小，直接排序更快
    if(r - p < STRAIGHT_SORT_LENGTH){
        quickSort(a, p, r);
        return a[p+k-1];
    }
    // 找到各个区间的中位数，并放到数组的最前面
    for(int i = 0; i <= (r-p-4)/5; i++){
        int s = p + 5 * i;
        int t = s + 4;
        quickSort(a, s, t);
        swapBaseStations(a, p+i, s+2);
    }
    // 选择中位数的中位数作为划分基准x
    BaseStation x = select(a, p, p+(r-p-4)/5, (r-p+6)/10);
    // 根据x将a[p:r]分成三部分
    int i, j;
    i = partition(a, p, r, x);
    j = i - p + 1; //左子段长度
    if(k == j)
        return a[i];
    else{
        recursionDepth++;
        if(k < j){
            return select(a, p, i-1, k);
        }
        else {
            return select(a, i+1, r, k-j); 
        }
    } 
}

// 一分为二
BaseStation select_2(vector<BaseStation>a, int p, int r, int k){
    recursionDepth++;
    // 查找区间小，直接排序更快
    if(r - p < STRAIGHT_SORT_LENGTH){
        quickSort(a, p, r);
        return a[p+k-1];
    }
    // 找到各个区间的中位数，并放到数组的最前面
    for(int i = 0; i <= (r-p-4)/5; i++){
        int s = p + 5 * i;
        int t = s + 4;
        quickSort(a, s, t);
        swapBaseStations(a, p+i, s+2);
    }
    // 选择中位数的中位数作为划分基准x
    BaseStation x = select_2(a, p, p+(r-p-4)/5, (r-p+6)/10);
    // 根据x将a[p:r]分成三部分
    int i, j;
    i = partition(a, p, r, x);
    j = i - p + 1; //左子段长度

    if(k <= j)
        return select_2(a, p, i, k);
    else 
        return select_2(a, i+1, r, k-j); 
}

int main(){
    vector<BaseStation> datas;
    BaseStation data;
    FILE * fp;
    fp = fopen("./02-1.csv", "r");
    while(fscanf(fp,"%d,%lf", &data.ENODEBID, &data.K_DIST) != EOF){
        datas.push_back(data);
    }
    fclose(fp);

    printf("===============Following are divide into THREE: ===============\n");
    BaseStation result = select(datas, 0, datas.size()-1, 1); 
    printf("The  smallest k-dist station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);
    
    recursionDepth = 0;
    result = select(datas, 0, datas.size()-1, 5); 
    printf("The 5th smallest k-dist  station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);
    
    recursionDepth = 0;
    result = select(datas, 0, datas.size()-1, 50); 
    printf("The 50th smallest k-dist  station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);
    
    recursionDepth = 0;
    result = select(datas, 0, datas.size()-1, datas.size()); 
    printf("The biggest k-dist station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);


    printf("===============Following are divide into TWO: ===============\n");
    recursionDepth = 0;
    result = select_2(datas, 0, datas.size()-1, 1); 
    printf("The  smallest k-dist station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);
    
    recursionDepth = 0;
    result = select_2(datas, 0, datas.size()-1, 5); 
    printf("The 5th smallest k-dist  station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);
    
    recursionDepth = 0;
    result = select_2(datas, 0, datas.size()-1, 50); 
    printf("The 50th smallest k-dist  station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);
    
    recursionDepth = 0;
    result = select_2(datas, 0, datas.size()-1, datas.size()); 
    printf("The biggest k-dist station is: %d,%.3lf\nAnd the recursion depth is : %d\n\n", result.ENODEBID, result.K_DIST, recursionDepth);

    return 0;
}