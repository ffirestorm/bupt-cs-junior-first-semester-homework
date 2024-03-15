import os
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.utils import Bunch
import numpy as np
import pickle
import random

# 文件夹路径
base_dir = './data/splice/'
type_list = ["auto", "business", "cul", "edu", "fz", "house", "mil", "ny", "ty", "yl"]
# document_counts = [54339,28180,58790,33954,71963,52290,61839,41798,87507,71064]
total_doc = 561890
train_out_path = "./data/trainset/train_1"
test_out_path = "./data/testset/test_1"

def divide_train_test():
    train_obj = Bunch(label=[], filenames=[], contents=[])
    test_obj = Bunch(label=[], filenames=[], contents=[])
    training_num = 8000
    # 首先将所有的数据读取到训练、测试对象中
    for t in type_list:
        dir_path = os.path.join(base_dir, t)
        file_list = []
        for _, _, files in os.walk(dir_path):
            file_list.extend(files)

        random.shuffle(file_list)
        # 选8000个出来, 剩下的用来测试
        train_files = file_list[:training_num]
        test_files = file_list[training_num:]

        for f in train_files:
            file_path = os.path.join(dir_path, f)
            with open(file_path, 'r', encoding="utf-8") as file:
                doc = file.read()
                train_obj.filenames.append(str(f))
                train_obj.label.append(t)
                train_obj.contents.append(str(doc))
        print("{} select to train over".format(t))  
        for f in test_files:
            file_path = os.path.join(dir_path, f)
            with open(file_path, 'r', encoding="utf-8") as file:
                doc = file.read()
                test_obj.filenames.append(str(f))
                test_obj.label.append(t)
                test_obj.contents.append(str(doc))

        print("{} select to test over".format(t))
    # 将二进制数据写入文件
    with open(train_out_path, 'wb') as f1:
        pickle.dump(train_obj, f1)
    with open(test_out_path, "wb") as f2:
        pickle.dump(test_obj, f2)

# 通过TF-IDF提取训练数据特征空间，生成N篇文档的TF-IDF向量空间
def tfidf_train_test(train_obj, train_out_path, test_obj, test_out_path):

    vec_train = TfidfVectorizer(max_features=2000,sublinear_tf=True, max_df=0.2, min_df=0.001)
    tfidf_space = Bunch(filenames=train_obj.filenames, 
                        weights=[], dictionary={}, labels=train_obj.label)

    tfidf_space.weights = vec_train.fit_transform(train_obj.contents)
    tfidf_space.dictionary = vec_train.vocabulary_

    # 保存特征空间，以便后续分类器使用
    with open(train_out_path, "wb") as file:
        pickle.dump(tfidf_space, file)

    # 生成测试集的TF-IDF向量空间
    vec_test = TfidfVectorizer(sublinear_tf=True, max_df=0.3, min_df=0.001, vocabulary=tfidf_space.dictionary)
    tfidf_space.weights = vec_test.fit_transform(test_obj.contents)
    tfidf_space.labels = test_obj.label
    with open(test_out_path, 'wb') as file:
        pickle.dump(tfidf_space, file)


def setup_lda():
    with open("./data/lda/train_space_1", 'rb') as file:
        tfidf_space_train = pickle.load(file)
    with open("./data/lda/test_space_1", 'rb') as file:
        tfidf_space_test = pickle.load(file)
    # 构建train的lda
    lda = LatentDirichletAllocation(n_components=10, random_state=0)
    lda_train_feature = lda.fit_transform(tfidf_space_train.weights)
    # 构建test的lda
    lda_test_feature = lda.fit_transform(tfidf_space_test.weights)
    with open("./data/lda/train_lda_1", 'wb') as file:
        pickle.dump(lda_train_feature, file)
    with open("./data/lda/test_lda_1", 'wb') as file:
        pickle.dump(lda_test_feature, file)


# 读取处理好的训练集和测试集
def get_train_test():
    with open(train_out_path, 'rb') as train:
        train_obj = pickle.load(train)
    with open(test_out_path, 'rb') as test:
        test_obj = pickle.load(test)
    return train_obj, test_obj



if __name__ == "__main__":
    divide_train_test()
    train, test = get_train_test()
    print("get data over")
    tfidf_train_test(train_obj=train, train_out_path="./data/lda/train_space_1", test_obj=test, test_out_path="./data/lda/test_space_1")
    setup_lda()


# 失败的加权模型
# 将训练集转换为TF-IDF矩阵, 为矩阵加权，喂给LDA主题模型,并保存
# def lda_fit(train_obj):
#     # 计算文档频率（DF）
#     vec_train = TfidfVectorizer(max_features=2000, max_df=0.2, token_pattern=r'\b\w+\b')
#     df_matrix = vec_train.fit_transform(train_obj.contents)
#     print(df_matrix.shape)
#     # doc_freqs = df_matrix.transform(train_obj.contents)
#     weight_array = np.array(train_obj.weights)
#     print(weight_array.shape)
#     # 将 TF-IDF 矩阵按照样本权重进行加权
#     weighted_tfidf_matrix = df_matrix.multiply(1/np.sqrt(weight_array[:, np.newaxis]))
#     # 构建 LDA 模型并在 TF-IDF 矩阵上训练
#     lda = LatentDirichletAllocation(n_components=11, random_state=42)
#     lda.fit(weighted_tfidf_matrix)
#     with open("./data/lda/lda_model", 'wb') as lda_file:
#         pickle.dump(lda, lda_file)
#     with open("./data/lda/tfidf", "wb") as tfidf_file:
#         pickle.dump(vec_train, tfidf_file)



# 本来想直接读取，然后加权得到矩阵，但是内存分配不够
# # 存放所有文档的列表
# documents = []
# weights = []
# # 添加每个已分词文件到列表中
# for t in type_list:
#     dir_path = os.path.join(base_dir, t)
#     count = 0   
#     for root, dirs, files in os.walk(dir_path):
#         for f in files:
#             path = os.path.join(root, f)
#             with open(path, 'r', encoding='utf-8') as file:
#                 # 读取文件内容
#                 documents.append(file.read())
#             weights.append(total_doc / len(files))
#             count += 1
#             if count % 10000 == 0 :
#                 print(count)
#             flag = not flag

# weights_array = np.array(weights)
# # 将文档列表转换为TF-IDF矩阵
# # max_df 表示如果一个单词在百分之max_df的文档中出现，就要省略
# vec_train = TfidfVectorizer(max_features=500, max_df=0.3, token_pattern=r'\b\w+\b')
# tfidf_matrix = vec_train.fit_transform(documents)
# print(len(weights))
# print(tfidf_matrix.shape[0])
# weighted_tfidf_matrix = tfidf_matrix.multiply(np.repeat(weights, tfidf_matrix.shape[0]))
# # 构建LDA模型
# lda = LatentDirichletAllocation(n_components=11, random_state=42)

# # 在TF-IDF矩阵上训练LDA模型
# lda.fit(weighted_tfidf_matrix)

# # 打印每个主题的前几个关键词
# feature_names = vec_train.get_feature_names_out()
# n_top_words = 10
# for topic_idx, topic in enumerate(lda.components_):
#     top_words_idx = topic.argsort()[:-n_top_words - 1:-1]
#     top_words = [feature_names[i] for i in top_words_idx]
#     print(f"Topic #{topic_idx}: {', '.join(top_words)}")