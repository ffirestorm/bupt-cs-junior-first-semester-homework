#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <chrono>
using namespace std;

#define MAX_DISTANCE 99999
#define MAX_INT 1000000000
// 定义全局变量
vector<int> bestx;            // 记录最佳路径
double cw;                       // 当前已经走过的部分路径的总长
vector<int> x;                // 当前已经生成的部分路径
double bestw;                    // 最优路径长度
vector<vector<double>> graph; // 图的邻接矩阵
int start;                    // TSP的起始点
int n;                        // 有多少个城市
long long nodeNum = 0;
// 将基站id转为数组的索引
int getIndexFromId(int id, vector<int> ids)
{
    for (int i = 0; i < ids.size(); i++)
    {
        if (id == ids[i])
            return i;
    }
    return -1;
}
// 获取用户输入的起点
int getInputStart(vector<int> ids)
{
    int id;
    for (int i = 0; i < ids.size(); i++)
    {
        cout << ids[i] << "\t";
    }
    cout << endl
         << "请从以上基站ID中选择一个当做起点:";
    cin >> id;
    while (true)
    {
        auto it = find(ids.begin(), ids.end(), id);
        if (it == ids.end())
        {
            cout << "输入不合法，请重新输入" << endl;
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
            // 找到更优的路径，更新
            for (int j = 1; j <= n; j++)
            {
                bestx[j] = x[j];
            }
            bestw = cw + w(x[n - 1], x[n]) + w(x[n], start);
            cout << "搜索到其中一个解 : " << bestw << endl;
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
        cerr << "文件打开失败" << endl;
        return 1;
    }
    string line;
    getline(inputFile, line);
    stringstream ss(line);
    // 读取第一行基站数据
    int id;
    double value;
    vector<int> ids;
    while (ss >> id)
    {
        ids.push_back(id);
    }
    // 跳过第一列读取距离数据
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
    cout << "回溯法"<<endl;
    cout << "最短距离为： " << bestw << endl;
    cout << "搜索过的节点数为: " << nodeNum << endl;
    cout << "程序运行时间: " << duration.count() << " 毫秒" << std::endl;
    return 0;
}