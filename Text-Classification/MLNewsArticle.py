# This is a Machine Learning script that uses pre-labeled and pre-processed 
# data to train a ML algorithm to run a multi-label classification task

# Import all the neccecary packages for the program
import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from collections import defaultdict
from sklearn.pipeline import Pipeline
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.multiclass import OneVsRestClassifier
from RssScraper.FullRSSList import MyTheFinalList # RssScraper is the folder and FullRSSList is the file inside it
from RssScraper.RssFeedNewArticle import printdepositlist #transfer your own list of pre-processed data from another Python Script





################################# Import your pre-label data #################################

data_path = "/Users/Hanne/Portofolio/Text-Classification/Book1.csv"

data_raw = pd.read_csv(data_path)

data = data_raw
data = data_raw.loc[np.random.choice(data_raw.index, size=len(data_raw))]
#data.shape

###############################################################################################



if not sys.warnoptions:
    warnings.simplefilter("ignore")



################################# Check for the categories of Data #################################

categories = list(data_raw.columns.values)
categories = categories[2:]
#print(categories)

###############################################################################################



################################# Clean the Data of non-numero-alphabetic symbols #################################

def cleanHtml(sentence):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, ' ', str(sentence))
    return cleantext


def cleanPunc(sentence): #function to clean the word of any punctuation or special characters
    cleaned = re.sub(r'[?|!|\'|"|#]',r'',sentence)
    cleaned = re.sub(r'[.|,|)|(|\|/]',r' ',cleaned)
    cleaned = cleaned.strip()
    cleaned = cleaned.replace("\n"," ")
    return cleaned


def keepAlpha(sentence):
    alpha_sent = ""
    for word in sentence.split():
        alpha_word = re.sub('[^a-z A-Z wåäöÅÄÖ]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent

#####################################################################################################################



################################# Getting rid of stopwords and stemming the lexemes #################################

nltk.download('stopwords')

stop_words = set(stopwords.words('swedish'))
stop_words.update(['noll','ett','två','tre','fyra','fem','sex','sju','åtta','nio','tio','kunna','också','över','bland','förutom','hursom','än','inom'])
re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)
def removeStopWords(sentence):
    global re_stop_words
    return re_stop_words.sub(" ", sentence)

data['Heading'] = data['Heading'].apply(removeStopWords)
data.head()

stemmer = SnowballStemmer("swedish")
def stemming(sentence):
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

data['Heading'] = data['Heading'].apply(stemming)
data.head()

#####################################################################################################################



################################# Splitting the data into training and testing chunks #################################

train, test = train_test_split(data, random_state=42, test_size=0.30, shuffle=True)

#print(train.shape)
#kprint(test.shape)

train_text = train['Heading']
test_text = test['Heading']

########################################################################################################################



################################# Defining my imported pre-labeled data set variable  #################################

my_text = printdepositlist

my_text_no_empty = []


for item in my_text:
    if item != ' ':
        my_text_no_empty.append(item)

#print("my_text:", len(my_text))
#print("my_text type:", type(my_text))
#print("my_text_no_empty len:", len(my_text))

#######################################################################################################################



################################# Creating text vectors for the train and test dataset  #################################

vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(train_text)
vectorizer.fit(test_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels = ['Id','Heading'], axis=1)

x_test = vectorizer.transform(my_text) #For single case (your own sample text) checking
y_test = test.drop(labels = ['Id','Heading'], axis=1)

#######################################################################################################################



################################# Setting up ML algorithm  ###################################################

# DecisionTreeRegressor has heighest accuracy atm
LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(DecisionTreeRegressor())),
            ])


dicts = []
for category in categories:
    #print('**Processing {} articles...**'.format(category))
    # Training logistic regression model on train data
    LogReg_pipeline.fit(x_train, train[category])
    
    counter = 0
    n_counter = []
    for text in x_test:
        prediction = LogReg_pipeline.predict(text)
            #print(type(prediction))
        for pred in np.nditer(prediction):
            #print('Predicted as {}'.format(pred)) #Your own sample data test
            #print("\n")
            actual_text = my_text[counter]
            counter +=1
            
            tempDict = {}
            if pred == 1:
                #for i in range((len(my_text) - 1)):
                tempDict[actual_text] = category # Move them into a temporary dictionary (dict)
                dicts.append(tempDict) # Then append them to the main list of dictionary
            else:
                tempDict[actual_text] = "empty"
                dicts.append(tempDict)

#print(dicts)


###############################################################################################################



################################# Reduce the duplication of keys and append labels(values) to each key ###################################################


new_dicts = defaultdict(list)

for d in dicts:
    for k, v in d.items():
        new_dicts[k].append(v)



#print("new_dicts text: ", list(new_dicts.keys())[0])
#print("my_text text: ", my_text[0])

#print("dicts: ", (len(dicts)))
#print("new_dicts len: ", len(new_dicts))

#print("dicts type: ", type(dicts))
#print("new_dicts type: ", type(new_dicts))
#print("new_dicts len: ", len(new_dicts))


newAlist = []
for i in my_text:
    for k, v in new_dicts.items():
        if i == k:
            newAlist.append(i)
            newAlist.append(v)


'''
# This segment takes NewAlist(nested list of titles and topics) and converts it into a single dictionary
# This is NOT used
item = iter(newAlist)

ds = dict(zip(item, item))
'''

'''
# This is NOT used
test = [
    ["{} {}".format(key, v) for v in values] if values else [key]
    for key, values in zip(newAlist, Allvalues)
    ]
'''


################################# Merging nested NewAlist with category topics  ###################################################

#Function takes the NewAlist(nested list of titles and topics) and creates a news list with only category(topic) returns
def onlyCategories(newAlist):
    second_values = []

    for index in range(1, len(newAlist), 2):
        second_values.append(newAlist[index])

    return second_values 

onlyCategoryList = onlyCategories(newAlist)

#####################################################################################################################################


#print("newAlist: ", newAlist)
#print("test: ", test)
#print("test len: ", len(test))



################################# Merging imported TheFinalList with onlyCategoryList ###################################################

# Merging the OnlyCategoryList with the list(TheFinalList) from FullRSSList script
TotalLists = [a+[x] for a,x in zip(MyTheFinalList, onlyCategoryList)]

#print("TotalLists:", (TotalLists))
#print("TotalLists len:", len(TotalLists))

#print("newAdict len:", len(newAdict))
#print("newAdict type:", type(newAdict))

##########################################################################################################################################



################################# Converting TotalLists to Dictionary ###################################################

key_list = ['title', 'summary', 'link', 'published', 'topic']

finalDict = [dict( zip(key_list, v)) for v in TotalLists]

print(finalDict)
##########################################################################################################################