import pandas as pd

# 获取数据
excel_file_path = "./02-1 1033个基站数据.xls"

df = pd.read_excel(excel_file_path)
selected_columns = df[['ENODEBID', 'K_DIST']]
data = selected_columns.sort_values(by='ENODEBID')
data_k = selected_columns.sort_values(by='K_DIST')
for i in range(100):
    print(f"{i+1}.{data_k.iloc[i]['ENODEBID']}: {data_k.iloc[i]['K_DIST']}")
# 线性时间选择
"""
采用线性时间选择算法，根据基站k-dist距离，挑选出
k-dist值最小的基站
k-dist第5小的基站
k-dist值第50小的基站
k-dist值最大的基站
要求
1. 在排序主程序中设置全局变量，记录选择划分过程的递归层次
2. 参照讲义PPT，将教科书上的“一分为二”的子问题划分方法，改进为“一分为三”
，比较这2种划分方式下，选择过程递归层次的差异

"""



# 1、先化成1033/5 = 207 个段
# 2、在这几个段中排序，选出每个段的中位数
# 3、这些中位数移到最前面
# 4、找出这些中位数的中位数作为划分基准
# 5、一分为三：
#       如果中间的这个不是要找的，就判断左右长度
#       如果左边的长度大于要找的长度，那么就在左段找 
#       如果左边的长度小于要找的长度，那么就在右段找第k-j找


"""
template<class Type>
Type RandomizedSelect( Type a[], int p, int r, int k)
{
      if (p==r) return a[p];//*只有1个元素
      int i=RandomizedPartition(a,p,r), //*划分为2部分, e.g. i=p+5
      j=i-p+1;     /*左端小元素个数，e.g. j=6
      if (k<=j)     /* e.g. k=4， 第4小的元素3
      return RandomizedSelect(a,p,i,k); 
                                             //*在左半部分查找
      else return RandomizedSelect(a,i+1,r,k-j); 
             //*在右半部分查找
}
"""