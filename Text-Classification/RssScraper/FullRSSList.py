import feedparser
import datetime


################################ RSS FEED Parser #####################################
RSS_URLS = ['http://www.dn.se/nyheter/m/rss/',
            'https://rss.aftonbladet.se/rss2/small/pages/sections/senastenytt/', 'https://feeds.expressen.se/nyheter/',
            'http://www.svd.se/?service=rss', 'http://api.sr.se/api/rss/program/83?format=145',
            'http://www.svt.se/nyheter/rss.xml'
              ]

posts = []

for url in RSS_URLS:
    posts.extend(feedparser.parse(url).entries)
######################################################################################


#print(posts)
##################### Extracting the necessary items from RSS FEED ##################

def gettingNecessaryList():

    allitems = []


    for x in posts:
        try:
            tempdict = {}
            tempdict["title"] = x["title"]
            tempdict["summary"] = x["summary"]
            tempdict["link"] = x["link"]
            tempdict["published"] = x["published"]
            allitems.append(tempdict)
        except:
            allitems.append("")
    
    return allitems

#########################################################################################

AllItemsX = gettingNecessaryList()

####################### Put the above items into a final list ###########################



#print(AllItemsX)

def ThefinalList():

    finalList = []
    tempList = []
    key1 = "title"
    key2 = "summary"
    key3 = "link"
    key4 = "published"

    for x in AllItemsX:
        for key in x:
            if key1 == key:
                tempList.append(x[key])
            if key2 == key:
                tempList.append(x[key])
            if key3 == key:
                tempList.append(x[key])
            if key4 == key:
                # datetime conversion code
                date_str = x[key]
                date_obj = None
                try:
                    date_obj = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
                except ValueError:
                    try:
                        date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S%z')
                    except ValueError:
                        try:
                            date_obj = datetime.datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
                        except ValueError:
                            print(f'Error: unrecognized date format {date_str}')
                if date_obj is not None:
                    tempList.append(date_obj.strftime('%Y-%m-%d %H:%M:%S'))
        finalList.append(tempList)
        tempList = []

    return finalList


MyTheFinalList = ThefinalList()

#print(MyTheFinalList)
#print(len(MyTheFinalList))
############################################################################################################


################################# This Code is not used ####################################################
'''
for item in finalList:
    if item == ' ':
        print("this is the empty item: ", item)


# To find out how many keys(articles) are in the list
# And also compare to rest of the scripts to concatanate them
new_list = []
for value in finalList:
    new_list.append(value[0])
    
print(len(new_list))
'''
############################################################################################################

