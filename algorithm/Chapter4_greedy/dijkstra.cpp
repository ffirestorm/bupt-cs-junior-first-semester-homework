#include <iostream>
#include <vector>
#include <set>
#include <algorithm>
#include <unordered_map>
#include <limits>
#include <fstream>
#include <string>
#include <sstream>
#include <math.h>
#include <stack>
#define MAXINT 1000000000
using namespace std;
// ����վidתΪ���������
int getIndexFromId(int id, vector<int>ids){
    for(int i = 0; i < ids.size();i ++){
        if(id == ids[i])
            return i;
    }
    return -1;
}
// ��ȡ�û�������յ�
int getInputEnd(vector<int>ids){
    int id;
    for(int i = 0; i < ids.size();i++){
        cout << ids[i] << "\t";
    }
    cout << endl <<"������ϻ�վID��ѡ��һ�������յ�:";
    cin >> id;
    while(true){
        auto it = find(ids.begin(), ids.end(), id);
        if(it == ids.end()){
            cout << "���벻�Ϸ�������������"<< endl;
            cin >> id;
        }else{
            break;
        }
    }
    return getIndexFromId(id, ids); 
}
// ��ȡ�û���������
int getInputStart(vector<int>ids){
    int id;
    for(int i = 0; i < ids.size();i++){
        cout << ids[i] << "\t";
    }
    cout << endl <<"������ϻ�վID��ѡ��һ���������:" ;
    cin >> id;
        while(true){
        auto it = find(ids.begin(), ids.end(), id);
        if(it == ids.end()){
            cout << "���벻�Ϸ�������������"<< endl;
            cin >> id;
        }else{
            break;
        }
    }
    return getIndexFromId(id, ids); 
}

int getIdFromIndex(int index, vector<int>ids){
    return ids[index];
}
// ������·��
vector<int> getPath(vector<int>path, int v, int end)
{
    vector<int> p;
    p.push_back(end);
    while(end != v){
        end = path[end];
        p.push_back(end);
    }
    reverse(p.begin(), p.end());
    return p;
}

vector<int> getPrePath(vector<vector<double>> graph, int v){
    // ��ʼ�� s ���ϣ�ֻ��һ����ʼ��������
    int n = graph[0].size();
    vector<bool> s(n, false);
    vector<double> dist(n, MAXINT);
    vector<int> path(n, -1);    
    s[v] = true;
    dist[v] = 0;
    // �������·���㷨
    for(int i = 0; i < n; i++){
        // ����ԭ��v֮���������u�����ڲ�ͬ��ģsi������չ
        int temp = MAXINT;
        int u = v;
        for(int j = 0; j < n; j++){
            //ѡȡs�������Сdist�ĵ�
            if(!s[j] && dist[j] < temp){
                u = j;
                temp = dist[j];
            }
        }
        s[u] = true;
        for(int j = 0; j < n; j++){
            if(!s[j] && graph[u][j] != MAXINT 
            && dist[j] > graph[u][j]+dist[u]){
                dist[j] = graph[u][j] + dist[u];    
                path[j] = u;
            }
        }
    }
    return path;
}

vector<double> dijkstra(vector<vector<double>> graph, int v){
    // ��ʼ�� s ���ϣ�ֻ��һ����ʼ��������
    int n = graph[0].size();
    vector<bool> s(n, false);
    vector<double> dist(n, MAXINT);    
    s[v] = true;
    dist[v] = 0;
    // �������·���㷨
    for(int i = 0; i < n; i++){
        // ����ԭ��v֮���������u�����ڲ�ͬ��ģSi������չ
        int temp = MAXINT;
        int u = v;
        for(int j = 0; j < n; j++){
            //ѡȡs�������Сdist�ĵ�
            if(!s[j] && dist[j] < temp){
                u = j;
                temp = dist[j];
            }
        }
        s[u] = true;
        for(int j = 0; j < n; j++){
            if(!s[j] && graph[u][j] != MAXINT 
            && dist[j] > graph[u][j]+dist[u]){
                dist[j] = graph[u][j] + dist[u];    
            }
        }
    }
    return dist;
}

// �������پ�����Ϊ��������
double heuristic(vector<vector<double>> &graph, int u, int goal)
{
    int n = graph.size();
    int uRow = u / n;
    int uCol = u % n;
    int goalRow = goal / n;
    int goalCol = goal % n;

    return abs(uRow - goalRow) + abs(uCol - goalCol);
}

vector<int> reconstructPath(unordered_map<int, int> &cameFrom, int u)
{
    vector<int> totalPath = {u};
    while (cameFrom.find(u) != cameFrom.end())
    {
        u = cameFrom[u];
        totalPath.push_back(u);
    }
    reverse(totalPath.begin(), totalPath.end());
    return totalPath;
}

vector<int> AStar(vector<vector<double>> &graph, int start, int goal)
{
    int n = graph.size();

    set<int> openList;
    vector<bool> s(graph[0].size(), false);
    // g(n)�������ʼ�㵽��ǰ��n�Ŀ���
    unordered_map<int, double> dist;

    // h(n)����ǰ��n���յ�goal�Ĺ��㿪��
    unordered_map<int, double> h;

    // f(n) = g(n) + h(n)
    unordered_map<int, double> f;

    unordered_map<int, int> cameFrom;

    dist[start] = 0;
    h[start] = heuristic(graph, start, goal);
    f[start] = dist[start] + h[start];
    // 1. �Ƚ���ʼ����뿪���б�
    openList.insert(start);
    while (!openList.empty())
    {
        // ���ȶ��У����ȼ�����Ϊf(n)
        int u = *min_element(openList.begin(), openList.end(),
            [&](int a, int b){ return f[a] < f[b]; });

        if (u == goal)
        {
            return reconstructPath(cameFrom, goal);
        }
        openList.erase(u);
        s[u] = true;

        for (int j = 0; j < n; ++j)
        {
            // ���Ҳ��ڹرն����е�
            if (graph[u][j] != MAXINT && !s[j])
            {
                double tempDist = dist[u] + graph[u][j];
                if (openList.find(j) == openList.end() || tempDist < dist[j])
                {
                    // ��������
                    cameFrom[j] = u;
                    dist[j] = tempDist;
                    h[j] = heuristic(graph, j, goal);
                    f[j] = dist[j] + h[j];
                    openList.insert(j);
                }
            }
        }
    }

    // ���openList���˻�û�ҵ��յ㣬�ͷ��ؿ�
    return vector<int>();
}


int main(){
    vector<vector<double>> graph;
    ifstream inputFile("./1-1-2.txt");
    if(!inputFile.is_open()){
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
    while(ss >> id){
        ids.push_back(id);
    }
    // ������һ�ж�ȡ��������
    while(inputFile >> id){
        vector<double> row;
        for(int i = 0; i < ids.size(); i++){
            inputFile >> value;
            if(value+1 < abs(1e-4))
                value = MAXINT;
            row.push_back(value);
        }
        graph.push_back(row);
    }
    inputFile.close();

    // �û�������ʼλ��
    int start = getInputStart(ids); 
    vector<double>dist = dijkstra(graph, start);
    // int end = getInputEnd(ids);
    for(int i = 0 ; i < ids.size(); i++){
        int end = i;
        vector<int>prePath = getPrePath(graph, start);
        vector<int>path = getPath(prePath, start, end);
        cout << "=================��������ͨ�㷨�Ͻ�˹�����Ľ��=================="<< endl;
        cout << "dijkstra�����յ��·��Ϊ:" ;
        for(int i = 0 ; i < path.size()-1; i++){
            cout << getIdFromIndex(path[i], ids) << " --> ";
        }
        cout << getIdFromIndex(end, ids) << endl << "��̵ľ�����: " << dist[end] <<endl;

        cout << "=================�����ǸĽ��㷨A* �Ľ��=================="<< endl;
        vector<int>aPath = AStar(graph, start, end);
        double d = 0;
        // ��ȡ·��
        cout << " A*����㵽�յ��·��Ϊ: " ;
        for (int i = 1; i < aPath.size(); i++){
            d += graph[aPath[i - 1]][aPath[i]];
        }
        for (int i = 0; i < aPath.size(); i++){
            if(i != aPath.size()-1)
                cout << getIdFromIndex(aPath[i], ids) << " --> ";
            else
                cout << getIdFromIndex(aPath[i], ids) << endl;
        }
        cout << "��̾�����:" << d << endl;
    }
    
    return 0;
}