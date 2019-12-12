import pandas as pd
from sklearn.neural_network import MLPClassifier
from datetime import datetime
import numpy as np
from postgre_conn import executeQuery


def main():
    features = pd.read_csv("feature.csv")
    test_set = pd.read_csv("feature_test.csv")
    labels = features['Label']
    #print(labels)
    datetime_arr = test_set['Datetime']

    #rename first column of testing and training dataset to index this is done for compatability only
    features = features.rename(columns={'Unnamed: 0': 'index'})
    test_set = test_set.rename(columns={'Unnamed: 0': 'index'})

    print(test_set)
    features = features.drop(columns=['Window Length', 'Label', 'index'])
    #print(features)
    test_set = test_set.drop(columns=['Window Length', 'index'])
    test = MLPClassifier()

    #this cluster is just make the feature set of the testing data equal to the training data I removed a few features
    #there are 170 instead of 226. the missing features didnt work well with our dataset.
    test_col = list(test_set.columns)
    feature_col = list(features.columns)
    both_list = list(set(test_col).intersection(feature_col))
    del_list_train = set(feature_col) - set(both_list)
    del_list_test = set(test_col) - set(both_list)
    #print(both_list, len(both_list))
    #print(del_list_train, len(del_list_train))
    #print(del_list_test, len(del_list_test))
    features = features.drop(columns=del_list_train)
    test_set = test_set.drop(columns=del_list_test)

    test.fit(X=features, y=labels)

    predict = test.predict(X=test_set)
    test_predict = pd.DataFrame({'DateTime': datetime_arr, 'label': predict})
    print(test_predict)
    test_predict.to_csv("test_prediction.csv")


main()
