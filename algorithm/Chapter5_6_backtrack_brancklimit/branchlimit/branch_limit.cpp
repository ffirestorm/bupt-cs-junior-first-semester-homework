#include <iostream>
#include <vector>
#include <fstream>
#include <sstream>
#include <algorithm>
#include <chrono>
#include <queue>

using namespace std;

#define MAX_DISTANCE 99999
#define MAX_INT 1000000000

class Node{
public:
    vector <int> currentPath;   // 已有路径
    double lb;  // 下界
    int city;   // 当前扩展结点
    int level;  // 属于搜索树第几层，或处于路径中的第几号位置
    double cc;  // currentPath的花销
};
bool cmp(const Node&a, const Node&b){
    return a.lb > b.lb;
}
bool isExist(const vector<int>&cPath, int city){
    return find(cPath.begin(), cPath.end(), city) != cPath.end();
}

// 定义全局变量
vector<vector<double>> graph; // 图的邻接矩阵
int start;                    // TSP的起始点
int n;                        // 有多少个城市
long nodeNum = 0;             // 用来查看总共查询了多少结点

void printNode(Node node){
    cout << endl << "city : " << node.city << endl << "lb : " << node.lb << endl;
    cout << "current cost : " << node.cc << endl;
    cout << "path : " << endl;
    for(int i = 0; i < node.level; i++){
        cout << node.currentPath[i] << "-->" ;
    }
    cout << start << endl;    
}

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


bool getUpBound(vector<int>&path , double& cost, int current){
    // 边界条件：当搜索到最后一个点时，查看和起始点有没有路径
    if(path.size() == n){
        if(graph[current][start] != MAX_DISTANCE){
            cost += graph[current][start];
            return true;
        }
        return false;
    }
    vector<bool> isVisited(n, false);
    for(int i =0; i < path.size();i++){
        isVisited[path[i]] = true;
    }
    // 对于该点，进行一个 深度优先+贪心
    for(int i = 0; i < n; i++){
        // 这层循环用来找
        int min = MAX_INT;
        int next = -1;
        for(int j =0; j < n; j++){
            if(!isVisited[j] && graph[current][j] != MAX_DISTANCE && graph[current][j] < min){
                min = graph[current][j];
                next = j;
            }
        }
        // 没有路径了，回溯
        if(next == -1){
            return false;
        }
        // 有路径，查找该路径
        isVisited[next] = true;
        path.push_back(next);
        cost += graph[current][next];
        if(getUpBound(path, cost, next) == true){
            return true;
        }
        // 该路径之后也没路了，返回原来状态，找下一个结点
        path.pop_back();
        cost -= graph[current][next];
    }
    // 找寻失败了，没有通路
    return false;
}

double getLb(const Node& node){
    double lb = 2*node.cc;
    for(int i = 0; i < n; i++){
        if(i == node.currentPath[0] || i == node.currentPath[node.level-1]){
            // 到最近未遍历城市的距离
            double min = MAX_INT;
            for(int j = 0; j < n; j++){
                if(!isExist(node.currentPath, j) && graph[i][j] != MAX_DISTANCE && min > graph[i][j]){
                    min = graph[i][j];
                }
            }
            if(min == MAX_INT) min = 0;
            lb += min;
            continue;
        }
        // 估计未到达城市的最小成本
        if(!isExist(node.currentPath, i)){
            double min1 = MAX_INT;
            double min2 = MAX_INT;
            for(int j = 0; j < n; j++){
                if(graph[i][j] < min1){
                    min2 = min1;
                    min1 = graph[i][j];
                }else if(graph[i][j] < min2){
                    min2 = graph[i][j];
                }
            }
            lb += min1 + min2;
        }
    }
    lb/=2;
    return lb;
}

void branchLimitTSP(){
    // 初始化优先队列，以lb小的优先
    priority_queue<Node, vector<Node>, decltype(&cmp)> ant(cmp);
    Node root;
    root.currentPath = {start};
    root.lb = getLb(root);
    root.level=1, root.cc = 0, root.city = start;
    ant.push(root);
    // 获取上界
    vector<int>path = {start};
    double up;
    getUpBound(path, up, start);
    Node current, result;
    while(!ant.empty()){
        nodeNum ++ ;
        current = ant.top();
        ant.pop();
        if(current.level == n){
            if(graph[current.city][start]+current.lb <= up){
                up = current.lb + graph[current.city][start];
                // 获得某个次优解
                current.cc += graph[current.city][start];
                result = current;
            }
        }else{
            // 生成子结点
            for(int i = 0; i < n; i++){
                if(isExist(current.currentPath, i) || graph[current.city][i] == MAX_DISTANCE){
                    continue;
                }
                Node child;
                child.city = i;
                child.currentPath = current.currentPath;
                child.currentPath.push_back(i);
                child.cc = current.cc + graph[current.city][child.city];
                child.lb = getLb(child);
                if(child.lb <= up){
                    child.level = current.level + 1;
                    ant.push(child);
                }
            }
        }
    }
    printNode(result);
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
    Node result;
    auto startTime = chrono::high_resolution_clock::now();
    branchLimitTSP();
    auto endTime = chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
    cout << "程序运行时间: " << duration.count() << " 毫秒" << std::endl;
    cout << "搜索过的节点数为: " << nodeNum << endl;
    return 0;
}