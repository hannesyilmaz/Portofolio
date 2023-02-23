# This scripts extracts RSS-feed from the online News-sites
# it is then cleans and structures them to be imported by another script

# Import packages/files

from RssArticles import posts


##################### Extracting the titles and summeries from the dataset ##################

def OnlyTitlesandSumaries():
    only_titles_and_summaries = []
    for x in posts:
        try:
            tempdict = {}
            tempdict["title"] = x["title"]
            tempdict["summary"] = x["summary"]
            only_titles_and_summaries.append(tempdict)
        except KeyError as ke:
            only_titles_and_summaries.append("") #replace the missing keys with empty space
    return only_titles_and_summaries

Only_the_titles_Summaries = OnlyTitlesandSumaries()


def TitleAndSummaryList():
    title_and_summary_list = []
    temp_and_summary_title_list = []
    for x in Only_the_titles_Summaries:
        for key in x:
            if 'title' == key:
                firstkey = x[key]
            if 'summary' == key:
                secondkey = x[key]
                temp_and_summary_title_list.append(firstkey + ' ' + secondkey)
        title_and_summary_list.append(temp_and_summary_title_list)
        temp_and_summary_title_list = []
    return title_and_summary_list

The_Title_Summary_List = TitleAndSummaryList()


print(The_Title_Summary_List)
######################################################################################



##################### Concatenating the list of Titles into a single list  ##################

def PrintDeposit():
    newList= []
    for item in The_Title_Summary_List:
        for value in item:
            newList.append(value)
    return newList

printdepositlist = PrintDeposit()

#print(len(printdepositlist))

######################################################################################