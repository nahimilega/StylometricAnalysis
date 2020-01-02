
import pymongo
from pprint import pprint
import matplotlib.pyplot as plt
import pprint
import numpy as np
from statistics import mean




from featureAbstraction import abstract_feature
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

from sklearn import metrics
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.naive_bayes import GaussianNB
# label = user
# feture = post




#10590
userLimit = 10589 # No of users to iterate


client = pymongo.MongoClient("mongodb://192.168.1.26:27017/?serverSelectionTimeoutMS=10000&connectTimeoutMS=10000")
#client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["psosm"]
#igProfile = db['igprofile']

def connectDB(collectionname):
    '''
    Returns:
        Collection
    '''
    collection = db[collectionname]
    return collection

########### Get all post

def textfromInstaPost(postsList):
    textList = []
    for post in postsList:
        textNode = post['node']['edge_media_to_caption']['edges']
        for node in textNode:
            textList.append(node['node']['text'])

    return textList


def getInstatext(igid):
    collection = connectDB('igprofile')
    userText = []
    for userData in collection.find({"_id":igid}):
        postsList = userData['graphql']['user']['edge_owner_to_timeline_media']['edges']
        return textfromInstaPost(postsList)




def textfromtwitterPost(twitteruserID):
    collection = connectDB('twcontent2')
    userText = []
    # Find all post of a particular user
    for userData in collection.find({"user.id":twitteruserID}):
        #pprint.pprint(userData)
        #break ##################

        userText.append(userData['full_text'])

    return userText


def getTwittertext(twid):
    collection = connectDB('twprofile')
    userText = []
    for userData in collection.find({"_id":twid}):
        userID = userData['id']
        userText = textfromtwitterPost(userID)

    return userText

########### End of Get all post


########### For Analysis
def getFrequencyForall(allUser, textTofind):
    '''
    Args:
        list: first element insta data second twitter
    '''
    all_count = []
    for user in allUser:
        count = []
        for i in user:
            count.append(getFrequency(i,textTofind))
        all_count.append(count)
    return all_count


def getFrequency(text, tofind):
    count = 0
    for i in text:
        count += i.count(tofind)
    return count

########### End of Analysis

def getlengthForall(allUser):
    '''
    Args:
        list: first element insta data second twitter
    '''
    all_count = []
    for user in allUser:
        count = []
        for i in user:
            count.append(len(i))
        all_count.append(count)
    return all_count






def drawPlot(data,ylabel,xlabel):
    '''
        Input:
        [[a1,b1],[a2,b2]]

        a1 and a2 be y axis points
        b1 and b2 be x axis points

    '''

    yaxis = []
    xaxis = []

    for i in data:
        yaxis.append(i[0])
        xaxis.append(i[1])

    plt.scatter(yaxis, xaxis, color='r')
    plt.xlabel(ylabel)
    plt.ylabel(xlabel)
    plt.show()









def do_insta_analysis():
    collection = connectDB('3pair')
    #all_text = []
    MaxMin = []
    all_post_length = []
    avg_post_length = []

    noOfPoster_perUSer = []

    cursor = collection.find({}, no_cursor_timeout=True).limit(userLimit)
    for usr in cursor:
        currentUser = [] # Two elements first list of insta text, second list of twitter
        currentUser = getTwittertext(usr['twid'])
        if currentUser == None:
            continue
        post_length = []
        for i in currentUser:
            post_length.append(len(i))


        if post_length != []:
            noOfPoster_perUSer.append(len(post_length))
            MaxMin.append(max(post_length) - min(post_length))
            avg_post_length.append(mean(post_length))


        all_post_length.extend(post_length)

        #all_text.append(currentUser)

    cursor.close()

    print("Mean length of all the posts: ",mean(all_post_length))


    ######## Plot 1
    plt.hist(MaxMin, bins=10)
    plt.ylabel("No. of users")
    plt.title("Difference between the min and max length of text of users ("+str(userLimit)+" Users)")
    plt.savefig("Difference between the min and max length of text of users ("+str(userLimit)+" Users).png")
    plt.clf()

    ######### Plot 2
    plt.hist(all_post_length, bins=10)
    plt.ylabel("Frequency")
    plt.xlabel(" Post length")
    plt.title("Post length histogram of users ("+str(userLimit)+" Users)")
    plt.savefig("Post length histogram of users ("+str(userLimit)+" Users).png")
    plt.clf()

    ######### Plot 3
    plt.hist(avg_post_length, bins=10)
    plt.ylabel("Frequency")
    plt.xlabel(" Post length")
    plt.title("Avg post length of users histogram ("+str(userLimit)+" Users)")
    plt.savefig("Avg post length of users histogram  ("+str(userLimit)+" Users).png")
    plt.clf()

    ######### Plot 4
    plt.hist(noOfPoster_perUSer, bins=10)
    plt.ylabel("No of users")
    plt.xlabel("No of posts")
    plt.title("No. of posts per users ("+str(userLimit)+" Users)")
    plt.savefig("No. of posts per users ("+str(userLimit)+" Users).png")
    plt.clf()
    client.close()





'''
if __name__ == "__main__":
    collection = connectDB('3pair')
    all_text = []

    for usr in collection.find().limit(userLimit):
        currentUser = [] # Two elements first list of insta text, second list of twitter
        #currentUser.append(getInstatext(usr['igid']))
        currentUser.append(getTwittertext(usr['twid']))
        #if len(currentUser[0]) != 0 and len(currentUser[1]) != 0:
        #    all_text.append(currentUser)



    print(getFrequencyForall(all_text,'#'))
    allLength = getlengthForall(all_text)


    client.close()

    # TO ploth the length feature
    #drawPlot(allLength,'Insta Length','Twitter Length')




    #print(allLength)

    ##drawPlot()
    #print(all_text)



'''




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



'''
if __name__ == "__main__":
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
'''



do_insta_analysis()
