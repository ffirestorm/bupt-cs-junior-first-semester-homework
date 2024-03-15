// 编码：GBK
#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

void newArray(int **&array, size_t rows, size_t cols){
    array = new int *[rows];
    for(size_t i = 0; i < rows; i++){
        array[i] = new int[cols];
    }
}

int checkBIJ(int ** c, int i, int j){
    if(i == 0||j == 0){
        cout << "checkBIJ : 下标出错" <<endl;
        exit(1);
    }
    if(c[i][j] == c[i-1][j-1] + 1){
        return 1;
    }
    if(c[i-1][j] >= c[i][j-1]){
        return 2;
    }
    return 3;
}

void LCSLength(int m, int n, string x, string y, int **c, int **b){
    int i, j;
    // Y[j]空时，最小子问题<i, 0>
    for(i = 1; i <= m; i++)
        c[i][0] = 0;
        
    // X[i]空时，最小子问题<0, j>
    for(i = 1;i <= n; i++)
        c[0][i] = 0;
    for(i = 1; i <= m; i++){
        for(j = 1; j <= n; j++){
            if(x[i] == y[j]){
                c[i][j] = c[i-1][j-1] + 1;
                b[i][j] = 1;
            }else if(c[i-1][j] >= c[i][j-1]){
                c[i][j] = c[i-1][j];
                b[i][j] = 2;
            }else{
                c[i][j] = c[i][j-1];
                b[i][j] = 3;
            }
        }
    }
}

void LCS(int i, int j, string x, int **b){
    if(i==0 || j==0)
        return;
    // 第一种情况下，最长公共子序列由x[i-1]y[j-1]的解由x[i]构成
    if(b[i][j] == 1){
        LCS(i-1, j-1, x, b);
        cout << x[i];
    }else if(b[i][j] == 2){
        LCS(i-1, j, x, b);
    }else{
        LCS(i, j-1, x, b);
    }
}

void LCSLengthPro(int m, int n, string x, string y, int **c){
    int i, j;
    // Y[j]空时，最小子问题<i, 0>
    for(i = 1; i <= m; i++)
        c[i][0] = 0;
        
    // X[i]空时，最小子问题<0, j>
    for(i = 1;i <= n; i++)
        c[0][i] = 0;
    for(i = 1; i <= m; i++){
        for(j = 1; j <= n; j++){
            if(x[i] == y[j]){
                c[i][j] = c[i-1][j-1] + 1;
            }else if(c[i-1][j] >= c[i][j-1]){
                c[i][j] = c[i-1][j];
            }else{
                c[i][j] = c[i][j-1];
            }
        }
    }
}

void LCSpro(int i, int j, string x, int **c){
    if(i ==0 || j== 0){
        return;
    }
    // 第一种情况下，最长公共子序列由x[i-1]y[j-1]的解和x[i]构成
    if(checkBIJ(c, i, j) == 1){
        LCSpro(i-1, j-1, x, c);
        cout << x[i];
    }else if(checkBIJ(c, i, j) == 2){
        LCSpro(i-1, j, x, c);
    }else{
        LCSpro(i, j-1, x, c);
    }
}

int main(){
    vector <string> strings;
    
    ifstream inputFile("./附件1.最长公共子序列输入文件-2023.txt");
    if(!inputFile.is_open()){
        cerr << "打开附件1失败" <<endl;
        return 1;
    }
    string line;
    while(getline(inputFile, line)){
        strings.push_back(line);
    }
    
    inputFile.close();
    // 第0个字符是没用的
    string A = " "+strings[1], B = " "+strings[4], C = " "+strings[7], D = " "+strings[10];
    // cout << A << endl << B << endl << C << endl << D << endl;
    int **bab , **bcd, **bad, **bcb, **cab, **ccd, ** cad, ** ccb;
    newArray(bab, A.length()+1, B.length()+1);
    newArray(cab, A.length()+1, B.length()+1);

    newArray(bcd, C.length()+1, B.length()+1);
    newArray(ccd, C.length()+1, B.length()+1);

    newArray(bad, A.length()+1, D.length()+1);
    newArray(cad, A.length()+1, D.length()+1);

    newArray(bcb, C.length()+1, B.length()+1);
    newArray(ccb, C.length()+1, B.length()+1);

    LCSLength(A.length(), B.length(), A, B, cab, bab);
    LCSLength(A.length(), D.length(), A, D, cad, bad);
    LCSLength(C.length(), D.length(), C, D, ccd, bcd);
    LCSLength(C.length(), B.length(), C, B, ccb, bcb);
    cout << "A-B: ";
    LCS(A.length(), B.length(), A, bab);
    cout << endl << endl << "A-D: ";
    LCS(A.length(), D.length(), A, bad);
    cout << endl << endl << "C-D: ";
    LCS(C.length(), D.length(), C, bcd);
    cout << endl << endl << "C-B: ";
    LCS(C.length(), B.length(), C, bcb);

    cout << endl << endl << "=====================算法改进之后，输出如下：====================" << endl;
    LCSLengthPro(A.length(), B.length(), A, B, cab);
    LCSLengthPro(A.length(), D.length(), A, D, cad);
    LCSLengthPro(C.length(), D.length(), C, D, ccd);
    LCSLengthPro(C.length(), B.length(), C, B, ccb);
    cout << "A-B: ";
    LCSpro(A.length(), B.length(), A, cab);
    cout << endl << endl << "A-D: ";
    LCSpro(A.length(), D.length(), A, cad);
    cout << endl << endl << "C-D: ";
    LCSpro(C.length(), D.length(), C, ccd);
    cout << endl << endl << "C-B: ";
    LCSpro(C.length(), B.length(), C, ccb);
    return 0;
}