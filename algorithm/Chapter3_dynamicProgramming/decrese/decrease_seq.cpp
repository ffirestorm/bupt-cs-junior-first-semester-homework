// ���� GBK
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>
using namespace std;

void LDSpro1(vector<int>data){
    int n = data.size();
    vector<int> c(n, 1);// ��ʼ��ȫΪ1
    vector<int> s(n, -1);
    for(int i = 1; i < n ;i++){
        for(int j = 0; j < i; j++){
            if(data[j] >= data[i] && c[j]+1 > c[i]){
                c[i] = c[j]+1;
                s[i] = j;
            }
        }
    }
    int maxLen = *max_element(c.begin(), c.end());
    int i = distance(c.begin(), max_element(c.begin(), c.end()));
    vector<int> LDSpro1Seq;
    while(i!=-1){
        LDSpro1Seq.push_back(data[i]);
        i = s[i];
    }
    reverse(LDSpro1Seq.begin(), LDSpro1Seq.end());
    cout << "��ݼ������еĳ����ǣ�" << maxLen << endl;
    for(auto item : LDSpro1Seq){
        cout << item << "\t";
    }
    cout << endl;
}

int LDSpro2(vector<int>data, int*c, int*s, int n){
    int ret_index = -1;
    int maxLength = 0;
    // �Ӻ���ǰ�������������
    for(int i = n-1; i >= 0; i--){
        c[i] = 1;
        s[i] = i;
        int max = 0;
        for(int j=i+1; j < n; j++){
            if (data[j] <= data[i] && max < c[j]){
                c[i] = c[j] + 1;
                s[i] = j;
                max = c[j];
                if(maxLength < c[i]){
                    maxLength = c[i];
                    ret_index = i;
                }
            }
        }
    }
    return ret_index;
}

vector<int> getLDSpro2(vector<int> data, int *s, int index){
    vector<int> retSeq;
    retSeq.push_back(data[index]);
    while(index != s[index]){
        index = s[index];
        retSeq.push_back(data[index]);
    }
    return retSeq;
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


    int s1[data1.size()], s2[data2.size()], c1[data1.size()], c2[data2.size()];
    int index1, index2;
    index1 = LDSpro2(data1, c1, s1, data1.size());
    index2 = LDSpro2(data2, c2, s2, data2.size());
    vector<int> seq1 = getLDSpro2(data1, s1, index1);
    vector<int> seq2 = getLDSpro2(data2, s2, index2);
    cout << "����1����ݼ����г���Ϊ: " << seq1.size() << "  ��������:" << endl;
    for(int i = 0; i < seq1.size(); i++){
        cout << seq1[i] << "\t";
    }
    cout << endl;
    cout << "����2����ݼ����г���Ϊ: " << seq2.size() << "  ��������:" << endl;
    for(int i = 0; i < seq2.size(); i++){
        cout << seq2[i] << "\t";
    }
    cout << endl;
    LDSpro1(data1);
    LDSpro1(data2);    
}