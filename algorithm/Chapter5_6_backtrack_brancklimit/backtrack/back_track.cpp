#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <chrono>
using namespace std;

#define MAX_DISTANCE 99999
#define MAX_INT 1000000000
// ����ȫ�ֱ���
vector<int> bestx;            // ��¼���·��
double cw;                       // ��ǰ�Ѿ��߹��Ĳ���·�����ܳ�
vector<int> x;                // ��ǰ�Ѿ����ɵĲ���·��
double bestw;                    // ����·������
vector<vector<double>> graph; // ͼ���ڽӾ���
int start;                    // TSP����ʼ��
int n;                        // �ж��ٸ�����
long long nodeNum = 0;
// ����վidתΪ���������
int getIndexFromId(int id, vector<int> ids)
{
    for (int i = 0; i < ids.size(); i++)
    {
        if (id == ids[i])
            return i;
    }
    return -1;
}
// ��ȡ�û���������
int getInputStart(vector<int> ids)
{
    int id;
    for (int i = 0; i < ids.size(); i++)
    {
        cout << ids[i] << "\t";
    }
    cout << endl
         << "������ϻ�վID��ѡ��һ���������:";
    cin >> id;
    while (true)
    {
        auto it = find(ids.begin(), ids.end(), id);
        if (it == ids.end())
        {
            cout << "���벻�Ϸ�������������" << endl;
            cin >> id;
        }
        else
        {
            break;
        }
    }
    return getIndexFromId(id, ids);
}

double w(int a, int b)
{
    // cout << a << "--" << b << ":" << graph[a][b] << endl;
    return graph[a][b];
}

void swap(int &a, int &b)
{
    // cout << "swap" << a << " : " << b << endl;
    int temp = a;
    a = b;
    b = temp;
}

void backTrackTSP(int layer)
{
    nodeNum+=1;
    if (layer == n)
    {
        // cout << "layer == n" << endl;
        if (!abs(w(x[n - 1], x[n]) - MAX_DISTANCE) < 1e-4 && !abs(w(x[n], start) - MAX_DISTANCE) < 1e-4 && cw + w(x[n - 1], x[n]) + w(x[n], start) < bestw)
        {
            // �ҵ����ŵ�·��������
            for (int j = 1; j <= n; j++)
            {
                bestx[j] = x[j];
            }
            bestw = cw + w(x[n - 1], x[n]) + w(x[n], start);
            cout << "����������һ���� : " << bestw << endl;
        }
    }
    else
    {
        for (int j = layer; j <= n; j++)
        {
            if (!abs(w(x[layer - 1], x[j]) - MAX_DISTANCE) < 1e-4 && cw + w(x[layer - 1], x[j]) < bestw)
            {
                swap(x[layer], x[j]);
                cw += w(x[layer - 1], x[layer]);
                backTrackTSP(layer + 1);
                cw -= w(x[layer - 1], x[layer]);
                swap(x[layer], x[j]);
            }
        }
    }
}

int main()
{
    ifstream inputFile("./1-2-30.txt");
    if (!inputFile.is_open())
    {
        cerr << "�ļ���ʧ��" << endl;
        return 1;
    }
    string line;
    getline(inputFile, line);
    stringstream ss(line);
    // ��ȡ��һ�л�վ����
    int id;
    double value;
    vector<int> ids;
    while (ss >> id)
    {
        ids.push_back(id);
    }
    // ������һ�ж�ȡ��������
    while (inputFile >> id)
    {
        vector<double> row;
        for (int i = 0; i < ids.size(); i++)
        {
            inputFile >> value;
            row.push_back(value);
        }
        graph.push_back(row);
    }
    inputFile.close();
    for (int i = 0; i < graph.size(); i++)
    {
        for (int j = 0; j < graph[i].size(); j++)
        {
            cout << graph[i][j] << "\t";
        }
        cout << endl;
    }
    n = ids.size();
    start = getInputStart(ids);
    bestx.resize(n + 1);
    x.resize(n + 1);
    cw = 0;
    bestw = MAX_INT;
    for (int i = 1; i <= n; i++)
    {
        x[i] = getIndexFromId(ids[i - 1], ids);
    }
    swap(x[start + 1], x[1]);
    auto startTime = chrono::high_resolution_clock::now();
    backTrackTSP(2);
    auto endTime = chrono::high_resolution_clock::now();
    for (int i = 1; i <=n; i++)
    {
        cout << ids[bestx[i]] << "-->";
    }
    cout << ids[start] << endl;
    for (int i = 1; i <=n; i++)
    {
        cout << bestx[i] << "-->";
    }
    cout << start << endl;
    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
    cout << "���ݷ�"<<endl;
    cout << "��̾���Ϊ�� " << bestw << endl;
    cout << "�������Ľڵ���Ϊ: " << nodeNum << endl;
    cout << "��������ʱ��: " << duration.count() << " ����" << std::endl;
    return 0;
}