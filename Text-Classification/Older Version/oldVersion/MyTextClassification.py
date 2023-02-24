#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[2]:


data_path = "/Users/hannesyilmaz/Book1.csv"


# In[3]:


print(data_path)


# In[4]:


data_raw = pd.read_csv(data_path)


# In[5]:


print("Number of rows in data =",data_raw.shape[0])
print("Number of columns in data =",data_raw.shape[1])
print("\n")
print("**Sample data:**")
data_raw.head()


# In[6]:


rowSums = data_raw.iloc[:,2:].sum(axis=1)
clean_comments_count = (rowSums==0).sum(axis=0)

print("Total number of articles = ",len(data_raw))
print("Number of clean articles = ",clean_comments_count)
print("Number of articles with labels =",(len(data_raw)-clean_comments_count))


# In[7]:


missing_values_check = data_raw.isnull().sum()
print(missing_values_check)


# In[8]:


categories = list(data_raw.columns.values)
categories = categories[2:]
print(categories)


# In[9]:


counts = []
for category in categories:
    counts.append((category, data_raw[category].sum()))
df_stats = pd.DataFrame(counts, columns=['category', 'number of comments'])
df_stats


# In[10]:


sns.set(font_scale = 2)
plt.figure(figsize=(15,8))

ax= sns.barplot(categories, data_raw.iloc[:,2:].sum().values)

plt.title("Topics in each category", fontsize=24)
plt.ylabel('Number of topics', fontsize=18)
plt.xlabel('Topic Type ', fontsize=18)

#adding the text labels
rects = ax.patches
labels = data_raw.iloc[:,2:].sum().values
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom', fontsize=18)

plt.show()


# In[11]:


rowSums = data_raw.iloc[:,2:].sum(axis=1)
multiLabel_counts = rowSums.value_counts()
multiLabel_counts = multiLabel_counts.iloc[1:]

sns.set(font_scale = 2)
plt.figure(figsize=(15,8))

ax = sns.barplot(multiLabel_counts.index, multiLabel_counts.values)

plt.title("Articles having multiple labels ")
plt.ylabel('Number of articles', fontsize=18)
plt.xlabel('Number of Topics', fontsize=18)

#adding the text labels
rects = ax.patches
labels = multiLabel_counts.values
for rect, label in zip(rects, labels):
    height = rect.get_height()
    ax.text(rect.get_x() + rect.get_width()/2, height + 5, label, ha='center', va='bottom')

plt.show()


# In[12]:


from wordcloud import WordCloud,STOPWORDS

plt.figure(figsize=(40,25))

# Utbildning
subset = data_raw[data_raw.Utbildning==1]
text = subset.Heading.values
cloud_Utbildning = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 1)
plt.axis('off')
plt.title("Utbildning",fontsize=40)
plt.imshow(cloud_Utbildning)


# SamhalleKonflikter
subset = data_raw[data_raw.SamhalleKonflikter==1]
text = subset.Heading.values
cloud_SamhalleKonflikter = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 2)
plt.axis('off')
plt.title("SamhalleKonflikter",fontsize=40)
plt.imshow(cloud_SamhalleKonflikter)


# Politik
subset = data_raw[data_raw.Politik==1]
text = subset.Heading.values
cloud_Politik = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 3)
plt.axis('off')
plt.title("Politik",fontsize=40)
plt.imshow(cloud_Politik)


# Miljo
subset = data_raw[data_raw.Miljo==1]
text = subset.Heading.values
cloud_Miljo = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 4)
plt.axis('off')
plt.title("Miljo",fontsize=40)
plt.imshow(cloud_Miljo)


# Religion
subset = data_raw[data_raw.Religion==1]
text = subset.Heading.values
cloud_Religion = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 5)
plt.axis('off')
plt.title("Religion",fontsize=40)
plt.imshow(cloud_Religion)


# Ekonomi
subset = data_raw[data_raw.Ekonomi==1]
text = subset.Heading.values
cloud_Ekonomi = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 6)
plt.axis('off')
plt.title("Ekonomi",fontsize=40)
plt.imshow(cloud_Ekonomi)

# LivsstilFritt
subset = data_raw[data_raw.LivsstilFritt==1]
text = subset.Heading.values
cloud_LivsstilFritt = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 7)
plt.axis('off')
plt.title("LivsstilFritt",fontsize=40)
plt.imshow(cloud_LivsstilFritt)

# VetenskapTeknik
subset = data_raw[data_raw.VetenskapTeknik==1]
text = subset.Heading.values
cloud_VetenskapTeknik = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 8)
plt.axis('off')
plt.title("VetenskapTeknik",fontsize=40)
plt.imshow(cloud_VetenskapTeknik)

# Halsa
subset = data_raw[data_raw.Halsa==1]
text = subset.Heading.values
cloud_Halsa = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 9)
plt.axis('off')
plt.title("Halsa",fontsize=40)
plt.imshow(cloud_Halsa)


# Idrott
subset = data_raw[data_raw.Idrott==1]
text = subset.Heading.values
cloud_Idrott = WordCloud(
                          stopwords=STOPWORDS,
                          background_color='black',
                          collocations=False,
                          width=2500,
                          height=1800
                         ).generate(" ".join(text))

plt.subplot(2, 5, 10)
plt.axis('off')
plt.title("Idrott",fontsize=40)
plt.imshow(cloud_Idrott)


plt.show()


# In[14]:


data = data_raw
data = data_raw.loc[np.random.choice(data_raw.index, size=638)]
data.shape


# In[15]:


import nltk
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
import re

import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")


# In[16]:



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
        alpha_word = re.sub('[^a-z A-Z]+', ' ', word)
        alpha_sent += alpha_word
        alpha_sent += " "
    alpha_sent = alpha_sent.strip()
    return alpha_sent


# In[17]:


data['Heading'] = data['Heading'].str.lower()
data['Heading'] = data['Heading'].apply(cleanHtml)
data['Heading'] = data['Heading'].apply(cleanPunc)
data['Heading'] = data['Heading'].apply(keepAlpha)
data.head()


# In[18]:


nltk.download('stopwords')

stop_words = set(stopwords.words('swedish'))
stop_words.update(['noll','ett','två','tre','fyra','fem','sex','sju','åtta','nio','tio','kunna','också','över','bland','förutom','hursom','än','inom'])
re_stop_words = re.compile(r"\b(" + "|".join(stop_words) + ")\\W", re.I)
def removeStopWords(sentence):
    global re_stop_words
    return re_stop_words.sub(" ", sentence)

data['Heading'] = data['Heading'].apply(removeStopWords)
data.head()


# In[19]:


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


# In[20]:


from sklearn.model_selection import train_test_split

train, test = train_test_split(data, random_state=42, test_size=0.30, shuffle=True)

print(train.shape)
print(test.shape)


# In[21]:


train_text = train['Heading']
test_text = test['Heading']


# In[22]:


from sklearn.feature_extraction.text import TfidfVectorizer
vectorizer = TfidfVectorizer(strip_accents='unicode', analyzer='word', ngram_range=(1,3), norm='l2')
vectorizer.fit(train_text)
vectorizer.fit(test_text)


# In[23]:


x_train = vectorizer.transform(train_text)
y_train = train.drop(labels = ['Id','Heading'], axis=1)

x_test = vectorizer.transform(test_text)
y_test = test.drop(labels = ['Id','Heading'], axis=1)


# In[24]:


from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.multiclass import OneVsRestClassifier


# In[25]:


get_ipython().run_cell_magic('time', '', '\n# Using pipeline for applying logistic regression and one vs rest classifier\nLogReg_pipeline = Pipeline([\n                (\'clf\', OneVsRestClassifier(LogisticRegression(solver=\'sag\'), n_jobs=-1)),\n            ])\n\nfor category in categories:\n    print(\'**Processing {} articles...**\'.format(category))\n    \n    # Training logistic regression model on train data\n    LogReg_pipeline.fit(x_train, train[category])\n    \n    # calculating test accuracy\n    prediction = LogReg_pipeline.predict(x_test)\n    print(\'Test accuracy is {}\'.format(accuracy_score(test[category], prediction)))\n    print("\\n")')


# In[26]:


get_ipython().run_cell_magic('time', '', '\n# using binary relevance\nfrom skmultilearn.problem_transform import BinaryRelevance\nfrom sklearn.naive_bayes import GaussianNB')


# In[ ]:



# initialize classifier chains multi-label classifier
classifier = ClassifierChain(LogisticRegression())

# Training logistic regression model on train data
classifier.fit(x_train, y_train)

# predict
predictions = classifier.predict(x_test)

# accuracy
print("Accuracy = ",accuracy_score(y_test,predictions))
print("\n")
