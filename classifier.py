
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.naive_bayes import GaussianNB

import numpy as np


from main import *

userLimit = 10589

def naiveBays(featureVector,Label):


    X_train, X_test, y_train, y_test = train_test_split(featureVector, Label, test_size=0.3,random_state=109) # 70% training and 30% test
    gnb = GaussianNB()
    gnb.fit(X_train, y_train)

    y_pred = gnb.predict(X_test)
    print("Accuracy:",metrics.accuracy_score(y_test, y_pred))


def normalize(featureVector,authorFeaturevalue):
    #ff
    featureVector = np.array(featureVector)
    mean_feature = np.mean(authorFeaturevalue, axis=0)
    standard_dev_feature = np.std(authorFeaturevalue,axis=0,ddof=1)

    normalizedfv = []
    i =0
    for col in featureVector.T:
        col = col - mean_feature[i]
        if standard_dev_feature[i] != 0:
            col = col / standard_dev_feature[i]
        normalizedfv.append(col.tolist())
        i += 1

    normalizedfv = np.array(normalizedfv)
    return normalizedfv.T




if __name__ == "__main__":
    '''
    This script is used to run naive bays classifier
    '''


    collection = connectDB('3pair')
    all_text = []

    for usr in collection.find().limit(userLimit):
        currentUser = [] # Two elements first list of insta text, second list of twitter
        currentUser = getInstatext(usr['igid'])

        if currentUser != None and currentUser != []:
            all_text.append(currentUser)


    Label = []
    count = 1
    featureVector = []
    authorFeaturevalue = []
    for userPost in all_text:
        userFeatureVector = abstract_feature(userPost)



        a = np.array(userFeatureVector)
        c= np.array(np.mean(a, axis=0))
        c = c.tolist()

        authorFeaturevalue.append(c)

        Label.extend([count]*len(userFeatureVector))
        featureVector.extend(userFeatureVector)
        count +=1

    authorFeaturevalue = np.array(authorFeaturevalue)
    #featureVector = normalize(featureVector,authorFeaturevalue )
    naiveBays(featureVector,Label)

