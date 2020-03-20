import pymongo
from pprint import pprint
import matplotlib.pyplot as plt
import pprint

from statistics import mean




from featureAbstraction import abstract_feature

# label = user
# feture = post




#10590
userLimit = 3 # No of users to iterate


client = pymongo.MongoClient("mongodb://192.168.1.26:27017/?serverSelectionTimeoutMS=10000&connectTimeoutMS=10000")
db = client["psosm"]

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


def do_analysis(option, goodUsers):
    '''
    Used to do analysis and make graphs


    option: 1 for insta
            2 for twitter

    '''
    global userLimit
    collection = connectDB('3pair')
    #all_text = []
    MaxMin = []         # To store the diff between length of posts made by users
    all_post_length = []
    avg_post_length = []

    noOfPoster_perUSer = []

    cursor = collection.find({}, no_cursor_timeout=True).limit(userLimit)
    for uid in cursor:
        print(uid)
        currentUser = [] # Two elements first list of insta text, second list of twitter
        if option == 2:
                #if str(uid['twid']) in goodUsers:
                print(str(uid['twid']))
                currentUser = getTwittertext(uid['twid'])
                print(currentUser)
                exit()
        else:
            if str(uid['igid']) in goodUsers:
                currentUser = getInstatext(uid['igid'])
                #print(currentUser)



        if currentUser == None:
            continue
        post_length = []  # To store length of each and every post of the current user
        for i in currentUser:
            post_length.append(len(i))

        if post_length != []:
            noOfPoster_perUSer.append(len(post_length))
            MaxMin.append(max(post_length) - min(post_length))
            avg_post_length.append(mean(post_length))
        all_post_length.extend(post_length)

        #all_text.append(currentUser)

    #cursor.close()

    print("Mean length of all the posts: ",mean(all_post_length))

    userLimit = len(avg_post_length)

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


#do_analysis(1)






def nooftwitterPost(twitteruserID):
    collection = connectDB('twcontent2')
    no_Post = 0
    # Find all post of a particular user
    no_Post =  collection.find({"user.id":twitteruserID}).count()
    return no_Post

def getTwitterpostno(twid):
    collection = connectDB('twprofile')
    tw_post_num = 0
    for userData in collection.find({"_id":twid}):
        userID = userData['id']
        tw_post_num = nooftwitterPost(userID)

    return tw_post_num


def find_elegible_users(twitterLimit, instaLimit):
    """
        Find the users who have twitter and insta post beyond a certain limit
    """
    collection = connectDB('3pair')
    cursor = collection.find({}, no_cursor_timeout=True).limit(userLimit)

    count = 0
    goodUsers = []
    cursor = collection.find({}, no_cursor_timeout=True).limit(userLimit)
    for usr in cursor:
        currentUser = [] # Two elements first list of insta text, second list of twitter
        TwitterPosts = getTwitterpostno(usr['twid'])
        currentUserInsta = getInstatext(usr['igid'])

        if TwitterPosts == None or currentUserInsta == None:
            continue

        insta_pots = len(currentUserInsta)

        if insta_pots >= instaLimit and TwitterPosts >= twitterLimit:
            count +=1
            goodUsers.append((usr['twid'],usr['igid']))

    cursor.close()

    f = open("goodUsers.txt", "a")
    for i in goodUsers:
        f.write(str(i[0])+" "+ str(i[1])+"\n")
    f.close()

    print(count)



if __name__ == "__main__":
    f = open("goodUsers.txt","r")

    twit = []
    while True:

        f1 = f.readline()
        if not f1:
            break
        twitter, insta = f1.split()
        twit.append(twitter)
        #print(insta)

    f.close()

    do_analysis(2, twit[:1])

    '''
    jj = list(f1)
    print(jj)
    for row in jj:
        print(row)
        twitter, insta = row.split()
        print(twitter)
        print(insta)
    '''

#find_elegible_users(2500,10)




























########### Useless stuff

"""
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



"""
