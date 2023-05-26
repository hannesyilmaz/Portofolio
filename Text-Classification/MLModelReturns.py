# This code takes in the ML model & values from NEWMLModelMLC.py and builds a pipeline 
# Then it takes in the new data from NEWFullRSSList.py to pass into the prediction algorithm
# At the end it gives out a dictionary with all the categories matching their respective values after creating a new list that contains the only dictiories that adheres to the schema


import numpy as np
from collections import defaultdict
from FullRSSList import MyTheFinalList
from MLModelMLC import categories, train, x_train, vectorizer, best_clf_pipeline
from RssFeedNewArticle import printdepositlist 
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier
from sklearn.model_selection import GridSearchCV
import jsonschema

########################## Importing list and concanating to get rid of empty text boxes ##########################
my_text = printdepositlist

my_text_no_empty = [item for item in my_text if item != ' ']

################################# Setting up ML algorithm  ###################################################

# Transform your new texts with the same vectorizer
my_text_transformed = vectorizer.transform(my_text_no_empty)

# Create a pipeline with LogisticRegression as the base estimator
LogReg_pipeline = Pipeline([
                ('clf', OneVsRestClassifier(LogisticRegression())),
            ])

# Define the parameter values that should be searched
C_values = [0.001, 0.01, 0.1, 1, 10, 100]
penalties = ['l1', 'l2']

# Create a parameter grid
param_grid = dict(clf__estimator__C=C_values, 
                  clf__estimator__penalty=penalties)

# Wrap the pipeline in GridSearchCV
grid_clf = GridSearchCV(LogReg_pipeline, param_grid, cv=5, scoring='accuracy')

results = {}

threshold = 0.3  # adjust this value based on your needs

for category in categories:
    for idx, text in enumerate(my_text_transformed):
        prediction_proba = best_clf_pipeline.predict_proba(text)
        actual_text = my_text_no_empty[idx]
        if actual_text not in results:
            results[actual_text] = []

        for i, category_prediction_proba in enumerate(prediction_proba[0]):  # note this line
            if category_prediction_proba > threshold:
                results[actual_text].append(categories[i])

...




###############################################################################################################



################################# Reduce the duplication of keys and append labels(values) to each key ###################################################


newAlist = [item for sublist in results.items() for item in sublist]

################################# Merging nested NewAlist with category topics  ###################################################

#Function takes the NewAlist(nested list of titles and topics) and creates a news list with only category(topic) returns
def onlyCategories(newAlist):
    return newAlist[1::2]

onlyCategoryList = onlyCategories(newAlist)

#####################################################################################################################################

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

finalDict = [dict(zip(key_list, v)) for v in TotalLists]

#print("this is finalDict: ", finalDict)
##########################################################################################################################


################################# Checking dictionaries' integrity #######################################################

# Create a new list of dictionaries that adhere to the schema

# Define the JSON schema
# Define the JSON schema
schema = {
  "type": "object",
  "properties": {
    "title": {"type": "string"},
    "summary": {"type": "string"},
    "link": {"type": "string", "format": "uri"},
    "published": {"type": "string", "format": "date-time"},
    "topic": {"type": "array"}
  },
  "required": ["title", "summary", "link", "published", "topic"],
  "additionalProperties": False
}

valid_list = []
for item in finalDict:
    try:
        jsonschema.validate(instance=item, schema=schema)
        valid_list.append(item)
    except jsonschema.exceptions.ValidationError:
        print("Dictionary is invalid and will be removed.")


validDict = valid_list

print(validDict)
#print(len(finalDict))
#print(len(validDict))




##########################################################################################################################

