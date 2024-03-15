#define _UNIT_TEST_

#include <stdio.h>
#include <string.h>
#include <stdlib.h> 

#define bool int
#define true 1
#define false 0

#ifdef _UNIT_TEST_
// 自己定义的，同学不一定要链表来写
// 定义黑名单节点结构
struct BlackListNode {
    char number[20]; 
    struct BlackListNode* next;
};

// 黑名单链表的头节点
struct BlackListNode* blacklist = NULL;

// 添加号码到黑名单
void addToBlackList(const char* number) {
    struct BlackListNode* newNode = (struct BlackListNode*)malloc(sizeof(struct BlackListNode));
    if (newNode) {
        strcpy(newNode->number, number);
        newNode->next = blacklist;
        blacklist = newNode;
    }
}

// 真正的接口函数
bool inBlackList(const char* number) {
    struct BlackListNode* current = blacklist;
    while (current) {
        if (strcmp(current->number, number) == 0) {
            return true; // 号码在黑名单中
        }
        current = current->next;
    }
    return false; // 号码不在黑名单中
}


// 用于单元测试
int main() {
    addToBlackList("1234567890");
    addToBlackList("9876543210");
    addToBlackList("55555555554");
    addToBlackList("55555555554");
    // 测试1：号码在黑名单中，测试桩返回1
    const char* testNumber1 = "1234567890";
    int result1 = inBlackList(testNumber1);
    printf("Is %s in the blacklist? %s\n", testNumber1, (result1 ? "Yes" : "No"));

    // 测试2：号码不在黑名单中，测试桩返回0
    const char* testNumber2 = "5555555555";
    int result2 = inBlackList(testNumber2);
    printf("Is %s in the blacklist? %s\n", testNumber2, (result2 ? "Yes" : "No"));

    // 测试主逻辑
    char number[20];
    printf("请输入想要查看的黑名单号码：");
    scanf("%s", &number);
    int result = inBlackList(number);
    printf("The number %s is%sin the blacklist.\n", number, (result ? " " : " not "));
    return 0;
}

#else


// 主逻辑
int main()  {
    // 主逻辑代码


    return 0;
}

#endif