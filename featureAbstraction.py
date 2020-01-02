#from nltk.corpus import stopwords

import emoji


#stops = stopwords.words('english')
x = [i.split("'")for i in stops]
stops = [i[0] for i in x]
#stops = list(set(stops))
stops = []

slang_stops = ['gonna', 'coulda', 'shoulda',
               'lotta', 'lots', 'oughta', 'gotta', 'ain', 'sorta', 'kinda', 'yeah', 'whatever', 'cuz', 'ya', 'haha', 'lol', 'eh']
puncts = ['!', ':', '...', '.', '%', '$', "'", '"', ';','(',')']
formattings = ['#', '__', '_', '  ', '*', '@','&',' ']
alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
numbers = ['0','1','2','3','4','5','6','7','8','9']



ascii_string = set("""!"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~""")




stops.extend(slang_stops)
stops.extend(puncts)
#stops.extend(numbers)
stops.extend(alphabet)
stops.extend(formattings)

def char_is_emoji(character):
    return character in emoji.UNICODE_EMOJI


def abstract_feature(userText):
    '''
    Args:
        userText: a list of all the post from a user for a specific platform

    Returns:
        Featue Vector for each fow for one post
    '''
    featureVector = []
    for post in userText:

        normalizingValue = len(post)

        local_feature_vector = [0]*len(stops)

        # No of stop words and special character
        # no of words also cnasidered here because counting the spaces
        post_in_lower = post.lower()
        for i in range(len(stops)):
            local_feature_vector[i] += post_in_lower.count(stops[i])/normalizingValue


        # No of character
        local_feature_vector.append(len(post))


        # No of non ascii character
        total_count = len(post)
        ascii_count = sum(c in ascii_string for c in post)
        local_feature_vector.append((total_count-ascii_count)/normalizingValue)



        # No of upper case
        u = sum(1 for i in post if i.isupper())
        local_feature_vector.append(u/normalizingValue)


        # Count the no of emoji
        u = sum(1 for i in post if char_is_emoji(i))
        local_feature_vector.append(u/normalizingValue)


        '''
        u = sum(1 for i in post if i.isdigit())
        local_feature_vector.append(u)
        '''


        featureVector.append(local_feature_vector)


    return featureVector









#185