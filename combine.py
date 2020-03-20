
import nltk
from scipy import spatial
import numpy as np
from featureAbstraction import abstract_feature





def get_BOW_cosine_similarity(insta_word_list, twitter_word_list, word_bag = []):
    if word_bag == []:
        word_bag = set(insta_word_list) + set(twitter_word_list)
    insta_vector = []
    twitter_vector = []
    for word in word_bag:
        insta_vector.append(insta_word_list.count(word))
        twitter_vector.append(twitter_word_list.count(word))

    result = 1 - spatial.distance.cosine(twitter_vector, insta_vector)
    return result


def combine_feature_BOW_style(insta_posts, twitter_posts):
    """
    Approach 1: Some features (like kind of stop words used & their frequency)  -->
    Consider stop words as BOW model --> Construct vocabulary and find vectors for
    twitter user and insta user --> Apply similarity metric (like jaccard, cosine)
    to find similarity b/w vectors
    """

    insta_text = ''.join(insta_posts)
    twitter_text = ''.join(twitter_posts)

    insta_word_list = nltk.word_tokenize(insta_text)
    twitter_word_list = nltk.word_tokenize(twitter_text)

    return get_BOW_cosine_similarity(insta_word_list, twitter_word_list)



def combine_feature_number_style(twitter_posts, insta_posts):
    """
    Approach 2: Some features (like number of hashes #'s used) are just numbers -->
    Consider BOW model at post level --> Construct vectors whose length is same as
    number of posts made by one user, values in that vectors are based on number of
    hashes used in each post ---> Apply similarity metric (like jaccard, cosine) to
    find similarity b/w vectors

    """

    twitter_features = abstract_feature(twitter_posts)
    insta_feature = abstract_feature(insta_posts)

    result_vector = []
    # itrating over features
    for i in range(np.shape(twitter_features)[1]):
        result = 1 - spatial.distance.cosine(twitter_features[:,i], insta_feature[:,i])
        result_vector.append(result)

    return result_vector