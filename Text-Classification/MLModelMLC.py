# This script import 'title' and 'summar' to be used in the training process from NEWRssFeedNewArticle
# This script creates a ML Model for text classification for two purposes;
# 1- Clean and Pre-process the data to be imported by the NEWMLModelReturns.py file
# 2- It measures the accuracy of the model itself (so when adding more data to Book1 dataset, this script must be run to calculate the accuracy)




# Import necessary libraries
import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split, GridSearchCV
from RssFeedNewArticle import printdepositlist 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression

# Suppress all warning messages
if not sys.warnoptions:
    warnings.simplefilter("ignore")

# Load the data
data_path = "/Users/Hanne/Portofolio/Text-Classification/Book1.csv"
data_raw = pd.read_csv(data_path)

# Shuffle the data
data_raw = data_raw.sample(frac=1)

# Preprocessing the data
categories = list(data_raw.columns.values)
categories = categories[2:]

data_raw['Heading'] = data_raw['Heading'].str.lower().str.replace('[^\w\s]','').str.replace('\d+', '').str.replace('<.*?>','')

nltk.download('stopwords')
stop_words = set(stopwords.words('swedish'))

def removeStopWords(sentence):
    return " ".join([word for word in nltk.word_tokenize(sentence) if word not in stop_words])

data_raw['Heading'] = data_raw['Heading'].apply(removeStopWords)

stemmer = SnowballStemmer("swedish")

def stemming(sentence):
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence

# Splitting the data into training and testing chunks
train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)

train_text = train['Heading']
test_text = test['Heading']

# Creating text vectors for the train and test dataset
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(train_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels = ['Id','Heading'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels = ['Id','Heading'], axis=1)

# Setting up ML pipeline and cross-validation
LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(LogisticRegression())),
            ])

# Hyperparameter Tuning
# Define the parameter values that should be searched
C_values = [0.1, 1, 10]
penalty_values = ['l1', 'l2']

# Create a parameter grid: map the parameter names to the values that should be searched
param_grid = dict(clf__estimator__C=C_values, 
                  clf__estimator__penalty=penalty_values)

# Instantiate the grid
grid = GridSearchCV(LogReg_pipeline, param_grid, cv=5, scoring='accuracy')

# Fit the grid with data
grid.fit(x_train, y_train)

# View the complete results (list of named tuples)
grid_results = grid.cv_results_

# Examine the best model
print("Best score: ", grid.best_score_)
print("Best params: ", grid.best_params_)
print("Best estimator: ", grid.best_estimator_)

# Fitting the pipeline on the training data with best parameters
best_clf_pipeline = grid.best_estimator_
best_clf_pipeline.fit(x_train, y_train)

# Predict on the test data
y_pred_proba = best_clf_pipeline.predict_proba(x_test)
threshold = 0.3 # Define your threshold here
y_pred = (y_pred_proba >= threshold).astype(int)

# Calculate and print the accuracy
accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)


"""
import re
import sys
import warnings
import nltk
import pandas as pd
import numpy as np
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.model_selection import train_test_split, GridSearchCV
from RssFeedNewArticle import printdepositlist 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression




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

###############################################################################################

data_raw['Heading'] = data_raw['Heading'].str.lower().str.replace('[^\w\s]','').str.replace('\d+', '').str.replace('<.*?>','')

nltk.download('stopwords')
stop_words = set(stopwords.words('swedish'))

def removeStopWords(sentence):
    return " ".join([word for word in nltk.word_tokenize(sentence) if word not in stop_words])

data_raw['Heading'] = data_raw['Heading'].apply(removeStopWords)

stemmer = SnowballStemmer("swedish")

def stemming(sentence):
    stemSentence = ""
    for word in sentence.split():
        stem = stemmer.stem(word)
        stemSentence += stem
        stemSentence += " "
    stemSentence = stemSentence.strip()
    return stemSentence
###########################################################################################################

################################# Splitting the data into training and testing chunks #################################

train, test = train_test_split(data_raw, random_state=42, test_size=0.30, shuffle=True)

train_text = train['Heading']
test_text = test['Heading']

########################################################################################################################


################################# Creating text vectors for the train and test dataset  #################################

vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(train_text)

x_train = vectorizer.transform(train_text)
y_train = train.drop(labels = ['Id','Heading'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels = ['Id','Heading'], axis=1)

#######################################################################################################################


################################# Setting up ML pipeline and cross-validation ###################################################

LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(LogisticRegression())),
            ])

cv_scores = cross_val_score(LogReg_pipeline, x_train, y_train, cv=5)

###############################################################################################################

################################# Hyperparameter Tuning ###################################################

# Define the parameter values that should be searched
max_depth_values = [None, 5, 10]
min_samples_split_values = [2, 5, 10]
min_samples_leaf_values = [1, 5, 10]

# Create a parameter grid: map the parameter names to the values that should be searched
param_grid = dict(clf__estimator__max_depth=max_depth_values, 
                  clf__estimator__min_samples_split=min_samples_split_values, 
                  clf__estimator__min_samples_leaf=min_samples_leaf_values)


# Instantiate the grid
grid = GridSearchCV(LogReg_pipeline, param_grid, cv=5, scoring='accuracy')

# Fit the grid with data
grid.fit(x_train, y_train)

# View the complete results (list of named tuples)
grid_results = grid.cv_results_

# Examine the best model
print("Best score: ", grid.best_score_)
print("Best params: ", grid.best_params_)
print("Best estimator: ", grid.best_estimator_)

###############################################################################################################

################################# Fitting the pipeline on the training data with best parameters ###################################################

best_clf_pipeline = grid.best_estimator_
best_clf_pipeline.fit(x_train, y_train)

###############################################################################################################

################################# Predict on the test data ###################################################

y_pred = best_clf_pipeline.predict(x_test)

###############################################################################################################

################################# Calculate and print the accuracy ###################################################

accuracy = accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

###############################################################################################################
"""

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


