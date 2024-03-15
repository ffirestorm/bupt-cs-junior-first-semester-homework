from sklearn.svm import LinearSVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import pickle
import time
from sklearn import metrics
import pandas as pd


type_list = ["auto", "business", "cul", "edu", "fz", "house", "mil", "ny", "ty", "yl"]
# 从文件中加载lda模型
def get_lda_model():
    with open("./data/lda/train_lda", 'rb') as file:
        lda_train = pickle.load(file)
    with open("./data/lda/test_lda", 'rb') as file:
        lda_test = pickle.load(file)

    return lda_train, lda_test

def get_train_test_tfidf():
    with open("./data/lda/train_space", 'rb') as file:
        tfidf_train = pickle.load(file)
        print(tfidf_train.weights)
        print("The dictionary size is : {}".format(len(tfidf_train.dictionary)))
    with open("./data/lda/test_space", 'rb') as file:
        tfidf_test = pickle.load(file)
    return tfidf_train, tfidf_test


# 读取处理好的训练集和测试集
def get_train_test():
    with open("./data/trainset/train_data", 'rb') as train:
        train_obj = pickle.load(train)
    with open("./data/testset/test_data", 'rb') as test:
        test_obj = pickle.load(test)
    return train_obj, test_obj

# 使用LDA主题模型训练并预测
def lda_classify(lda_train, train_space, lda_test, test_space):
    start_train = time.time()
    svm_linear = LinearSVC(C=1, tol=1e-5, loss='hinge', max_iter=2000)
    svm_linear.fit(lda_train, train_space.labels)
    end_train = time.time()
    print("training time is:{}".format(end_train-start_train))
    
    start_test = time.time()
    prediction = svm_linear.predict(lda_test)
    end_test = time.time()
    print("predicting time: {}".format(end_test-start_test))
    accuracy = accuracy_score(test_space.labels, prediction)
    print(f"Accuracy: {accuracy}")
    print ('精度:{0:.3f}'.format(metrics.precision_score(test_space.labels, prediction,average='weighted')))
    print ('召回:{0:0.3f}'.format(metrics.recall_score(test_space.labels, prediction,average='weighted')))
    print ('f1-score:{0:.3f}'.format(metrics.f1_score(test_space.labels, prediction,average='weighted')))

    report = classification_report(test_space.labels, prediction)
    print(report)
    pd.set_option('display.max_columns', None)
    pd.set_option("display.max_rows", None)
    confuse_matrix = pd.DataFrame(confusion_matrix(test_space.labels, prediction), columns=type_list, index=type_list)
    print(confuse_matrix)


# 使用TF-IDF矩阵空间训练并预测
def tfidf_classify(train, test, class_weight=None):
    x_train = train.labels
    y_train = train.weights
    svc_linear = LinearSVC(C=1, tol=1e-4, loss='hinge', max_iter=750, class_weight=class_weight)
    start_train = time.time()
    svc_linear.fit(y_train,x_train)
    end_train = time.time()
    print("training time is:{}".format(end_train-start_train))

    start_test = time.time()
    predict = svc_linear.predict(test.weights)
    end_test = time.time()
    print("predicting time: {}".format(end_test-start_test))
    accuracy = accuracy_score(test_space.labels, predict)
    print(f"Accuracy: {accuracy}")
    print ('精度:{0:.3f}'.format(metrics.precision_score(test.labels, predict, average='weighted')))
    print ('召回:{0:0.3f}'.format(metrics.recall_score(test.labels, predict, average='weighted')))
    print ('f1-score:{0:.3f}'.format(metrics.f1_score(test.labels, predict, average='weighted')))

    report = classification_report(test.labels, predict)
    print(report)
    pd.set_option('display.max_columns', None)
    pd.set_option("display.max_rows", None)
    confuse_matrix = pd.DataFrame(confusion_matrix(test.labels, predict), columns=type_list, index=type_list)
    print(confuse_matrix)


if __name__ == "__main__":
    lda_train, lda_test = get_lda_model()
    train_space, test_space = get_train_test_tfidf()
    # train_obj, test_obj = get_train_test()
    # svm_classify(lda, tfidf, train_obj, test_obj)
    class_weight = {'auto':1.0, 'business':0.5, "cul":0.8, "edu":0.5, "fz":1.0, "house":1.0, "mil":1.0, "ny":1.0, "ty":1.0, "yl":1.0}
    lda_classify(lda_train, train_space=train_space, lda_test=lda_test, test_space=test_space)
    tfidf_classify(train=train_space, test=test_space,class_weight=class_weight)



# def svm_classify(lda, tfidf, train, test, loss="hinge", weigh_param=None):
#     start_transform = time.time()
#     lda_train_feature = lda.transform(train.weights)
#     lda_test_feature = lda.transform(test.weights)
#     end_transform = time.time()
#     print(f"Time for transformation: {end_transform - start_transform} seconds")

#     # 构造分类器
#     svm_linear = LinearSVC(class_weight=weigh_param, loss=loss)

#     # 训练SVM
#     start_training = time.time()
#     # dense_train = lda_train_feature.toarray()
#     svm_linear.fit(lda_train_feature, train.labels)
#     end_training = time.time()
#     print(f"Time for training: {end_training - start_training} seconds")

#     # 预测
#     start_prediction = time.time()
#     predictions = svm_linear.predict(lda_test_feature)
#     end_prediction = time.time()
#     print(f"Time for prediction: {end_prediction - start_prediction} seconds")

#     # 评估
#     accuracy = accuracy_score(test.labels, predictions)
#     report = classification_report(test.labels, predictions)

#     print(f"Accuracy: {accuracy}")
#     print("Classification Report:")
#     print(report)
# def svm_classify(lda, tfidf, train_obj, test_obj):
#     start_transform = time.time()
#     lda_train_feature = lda.transform(tfidf.transform(train_obj.contents))
#     lda_test_feature = lda.transform(tfidf.transform(test_obj.contents))
#     end_transform = time.time()
#     print("transform time is : {}".format(end_transform-start_transform))
#     # 构建SVM分类器
#     linear_svm = SVC(kernel='linear')
#     start_train = time.time()
#     linear_svm.fit(lda_train_feature, train_obj.labels)
#     end_train = time.time()
#     print("train time is : {}".format(end_train-start_train))
#     # 预测
#     predict_linear = linear_svm.predict(lda_test_feature)
#     # 评估
#     accuracy_linear = accuracy_score(test_obj.labels, predict_linear)
#     report_linear = classification_report(test_obj.labels, predict_linear)
#     print(f"Accuracy: {accuracy_linear}")
#     print("Classification Report:")
#     print(report_linear)
#     print("predict time is {}".format(time.time() - end_train))


    # poly_svm = SVC(kernel="poly")
    # poly_svm.fit(lda_test_feature, test_obj.labels)
    # # 预测
    # predict_poly = poly_svm.predict(lda_test_feature)
    # # 评估
    # accuracy_poly = accuracy_score(test_obj.labels, predict_poly)
    # report_poly = classification_report(test_obj.labels, predict_poly)
    # print(f"Accuracy: {accuracy_poly}")
    # print("Classification Report:")
    # print(report_poly)