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
    vector <int> currentPath;   // ����·��
    double lb;  // �½�
    int city;   // ��ǰ��չ���
    int level;  // �����������ڼ��㣬����·���еĵڼ���λ��
    double cc;  // currentPath�Ļ���
};
bool cmp(const Node&a, const Node&b){
    return a.lb > b.lb;
}
bool isExist(const vector<int>&cPath, int city){
    return find(cPath.begin(), cPath.end(), city) != cPath.end();
}

// ����ȫ�ֱ���
vector<vector<double>> graph; // ͼ���ڽӾ���
int start;                    // TSP����ʼ��
int n;                        // �ж��ٸ�����
long nodeNum = 0;             // �����鿴�ܹ���ѯ�˶��ٽ��

void printNode(Node node){
    cout << endl << "city : " << node.city << endl << "lb : " << node.lb << endl;
    cout << "current cost : " << node.cc << endl;
    cout << "path : " << endl;
    for(int i = 0; i < node.level; i++){
        cout << node.currentPath[i] << "-->" ;
    }
    cout << start << endl;    
}

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


bool getUpBound(vector<int>&path , double& cost, int current){
    // �߽������������������һ����ʱ���鿴����ʼ����û��·��
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
    // ���ڸõ㣬����һ�� �������+̰��
    for(int i = 0; i < n; i++){
        // ���ѭ��������
        int min = MAX_INT;
        int next = -1;
        for(int j =0; j < n; j++){
            if(!isVisited[j] && graph[current][j] != MAX_DISTANCE && graph[current][j] < min){
                min = graph[current][j];
                next = j;
            }
        }
        // û��·���ˣ�����
        if(next == -1){
            return false;
        }
        // ��·�������Ҹ�·��
        isVisited[next] = true;
        path.push_back(next);
        cost += graph[current][next];
        if(getUpBound(path, cost, next) == true){
            return true;
        }
        // ��·��֮��Ҳû·�ˣ�����ԭ��״̬������һ�����
        path.pop_back();
        cost -= graph[current][next];
    }
    // ��Ѱʧ���ˣ�û��ͨ·
    return false;
}

double getLb(const Node& node){
    double lb = 2*node.cc;
    for(int i = 0; i < n; i++){
        if(i == node.currentPath[0] || i == node.currentPath[node.level-1]){
            // �����δ�������еľ���
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
        // ����δ������е���С�ɱ�
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
    // ��ʼ�����ȶ��У���lbС������
    priority_queue<Node, vector<Node>, decltype(&cmp)> ant(cmp);
    Node root;
    root.currentPath = {start};
    root.lb = getLb(root);
    root.level=1, root.cc = 0, root.city = start;
    ant.push(root);
    // ��ȡ�Ͻ�
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
                // ���ĳ�����Ž�
                current.cc += graph[current.city][start];
                result = current;
            }
        }else{
            // �����ӽ��
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
    Node result;
    auto startTime = chrono::high_resolution_clock::now();
    branchLimitTSP();
    auto endTime = chrono::high_resolution_clock::now();

    auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(endTime - startTime);
    cout << "��������ʱ��: " << duration.count() << " ����" << std::endl;
    cout << "�������Ľڵ���Ϊ: " << nodeNum << endl;
    return 0;
}