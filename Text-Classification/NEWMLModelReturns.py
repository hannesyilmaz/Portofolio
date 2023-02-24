import numpy as np
from collections import defaultdict
from NEWFullRSSList import MyTheFinalList
from NEWMLModelMLC import categories, x_test, train, x_train, my_text #transfer your own list of pre-processed data from another Python Script
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline
from sklearn.multiclass import OneVsRestClassifier


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

print(dicts)


###############################################################################################################



################################# Reduce the duplication of keys and append labels(values) to each key ###################################################


new_dicts = defaultdict(list)

for d in dicts:
    for k, v in d.items():
        new_dicts[k].append(v)


newAlist = []
for i in my_text:
    for k, v in new_dicts.items():
        if i == k:
            newAlist.append(i)
            newAlist.append(v)


################################# Merging nested NewAlist with category topics  ###################################################

#Function takes the NewAlist(nested list of titles and topics) and creates a news list with only category(topic) returns
def onlyCategories(newAlist):
    second_values = []

    for index in range(1, len(newAlist), 2):
        second_values.append(newAlist[index])

    return second_values 

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

finalDict = [dict( zip(key_list, v)) for v in TotalLists]

print(finalDict)
##########################################################################################################################