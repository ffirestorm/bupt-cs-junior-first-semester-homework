// ���� GBK
#include <iostream>
#include <fstream>
#include <vector>
using namespace std;

void maxSumSeq(vector<int> data){
    int sum = 0, index = -1;
    int *b = new int[data.size()];
    int *c = new int[data.size()];
    b[0] = data[0];
    for(int i = 1; i < data.size(); i++){
        if(b[i-1] > 0){
            b[i] = b[i-1] + data[i];
            c[i] = c[i-1];
        }else{
            b[i] = data[i];
            c[i] = i;
        }
        if(b[i] > sum){
            sum = b[i];
            index = i;
        }
    }
    cout << "����Ӷκ�Ϊ��" << sum <<"\t" << "����λ����: " 
        << c[index]+1 << "--" << index+1 << endl << "�����Ԫ�����£�" << endl;
    for(int i = c[index]; i <= index; i++)
        cout << data[i] << "  ";
    cout << endl;
}

void maxSumSeqPro (vector<int> data){
    int sum = 0, b = 0, c = 0, start = 0, end = 0;
    for(int i = 0; i < data.size(); i++){
        if(b > 0){
            b += data[i];
        }else{
            b = data[i];
            c = i;
        }
        if(b > sum){
            sum = b;
            end = i;
            start = c;
        }  
    }
    cout << "�����������Ӷκ�Ϊ��" << sum <<"\t" << "����λ����: " 
        << start+1 << "--" << end+1 << endl << "�����Ԫ�����£�" << endl;
    for(int i = start; i <= end; i++)
        cout << data[i] << "  ";
    cout << endl;
}

int main(){

    vector <int> data1, data2;// �����������
    ifstream inpuFile("./����2.����Ӷκ���������-����1-2023.txt");
    if(!inpuFile.is_open()){
        cerr << "��ʧ�ܣ�����2������1" << endl;
        return 1;
    }
    int value;
    while(inpuFile >> value){
        data1.push_back(value);
    }
    inpuFile.close();

    ifstream inputFile("./����2.����Ӷκ���������-����2-2023.txt");
    if(!inputFile.is_open()){
        cerr << "��ʧ�ܣ�����2������2" << endl;
        return 1;
    }
    while(inputFile >> value){
        data2.push_back(value);
    }
    inputFile.close();
    int* c1 = new int[data1.size()];
    int* c2 = new int[data2.size()];

    maxSumSeq(data1);
    maxSumSeq(data2);
    maxSumSeqPro(data1);
    maxSumSeqPro(data2);
    return 0;
}
