# This script creates a ML Model for text classification for two purposes;
# 1- Clean and Pre-process the data to be imported by the NEWMLModelReturns.py file
# 2- It measures the accuracy of the model itself (so when adding more data to Book1 dataset, this script must be run to calculate the accuracy)


import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split
from NEWRssFeedNewArticle import printdepositlist #transfer your own list of pre-processed data from another Python Script
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score



################################# Import your pre-labeled data #################################

data_path = "/Users/Hanne/Portofolio/Text-Classification/Book1.csv"

data_raw = pd.read_csv(data_path)

data = data_raw
data = data_raw.loc[np.random.choice(data_raw.index, size=len(data_raw))]

###############################################################################################

## This to suppress all warning messages that normally be printed to the console.
if not sys.warnoptions:
    warnings.simplefilter("ignore")

################################# Preprocessing the data #################################

################################# Check for the categories of Data #################################

categories = list(data_raw.columns.values)
categories = categories[2:]
#print(categories)

###############################################################################################

## Lowercasing
data['Heading'] = data['Heading'].str.lower()

## Removing punctuation
data['Heading'] = data['Heading'].str.replace('[^\w\s]','')

## Removing numerical digits
data['Heading'] = data['Heading'].str.replace('\d+', '')

## Removing HTML tags
data['Heading'] = data['Heading'].str.replace('<.*?>','')

## Removing stopwords and stemming the lexemes
nltk.download('stopwords')

stop_words = set(stopwords.words('swedish'))
stop_words.update(['noll','ett','två','tre','fyra','fem','sex','sju','åtta','nio','tio','kunna','också','över','bland','förutom','hursom','än','inom'])
re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)

def removeStopWords(sentence):
    global re_stop_words
    return re_stop_words.sub(" ", sentence)

data['Heading'] = data['Heading'].apply(removeStopWords)

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

###########################################################################################################

################################# Splitting the data into training and testing chunks #################################

train, test = train_test_split(data, random_state=42, test_size=0.30, shuffle=True)

#print(train.shape)
#print(test.shape)

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

################################# Creating a new DataFrame for my text  #################################

my_text_df = pd.DataFrame({'Heading': my_text_no_empty})
test_labels = pd.DataFrame(np.random.randint(0, 2, size=(len(my_text_no_empty), len(categories))), columns=categories)
test_df = pd.concat([my_text_df, test_labels], axis=1)

#######################################################################################################################

################################# Creating text vectors for the train and test dataset  #################################

vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(train_text)
vectorizer.fit(test_text)
vectorizer.fit(my_text_no_empty)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels = ['Id','Heading'], axis=1)

#print("Traning data shape after vectorization:", x_train.shape)

#x_test = vectorizer.transform(my_text_no_empty) #For single case (your own sample text) checking
#y_test = test.drop(labels = ['Id','Heading'], axis=1)

test_df['Heading'] = test_df['Heading'].str.lower().str.replace('[^\w\s]','').str.replace('\d+', '').str.replace('<.*?>','').apply(removeStopWords).apply(stemming)
x_test = vectorizer.transform(test_df['Heading'])
y_test = test_df.drop(labels=['Heading'], axis=1)

#######################################################################################################################


################################# Setting up ML pipeline and cross-validation ###################################################

# DecisionTreeRegressor has heighest accuracy atm
LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(DecisionTreeRegressor())),
            ])

cv_scores = cross_val_score(LogReg_pipeline, x_train, y_train, cv=5) #Perform 5-fold cross-validation

#print("Cross-validation scores:", cv_scores)
#print("Mean cross-validation score:", cv_scores.mean())

###############################################################################################################

################################# Fitting the pipeline on the training data  ###################################################

LogReg_pipeline.fit(x_train, y_train)
###############################################################################################################

################################# Predict on the test data ###################################################

y_pred = LogReg_pipeline.predict(x_test)
###############################################################################################################

################################# Calculate and print the accuracy ###################################################

accuracy = accuracy_score(y_test, y_pred)
#print("Accuracy:", accuracy)
###############################################################################################################







# The Old Script (for referance purposes)
"""
import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split

################################# Import your pre-labeled data #################################

data_path = "/Users/Hanne/Portofolio/Text-Classification/Book1.csv"

data_raw = pd.read_csv(data_path)

data = data_raw
data = data_raw.loc[np.random.choice(data_raw.index, size=len(data_raw))]
#data.shape

###############################################################################################

## This to supress all warning messages that normally be printed to the console.
if not sys.warnoptions:
    warnings.simplefilter("ignore")

################################# Check for the categories of Data #################################

categories = list(data_raw.columns.values)
categories = categories[2:]
#print(categories)


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
#print(test.shape)

train_text = train['Heading']
test_text = test['Heading']

########################################################################################################################

"""


