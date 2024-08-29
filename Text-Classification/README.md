How to run the Text-Classification Algorithm; 
Step_1
- Change the directory path in your MLModelML_4.py file for Book1.csv to your respective paths. 
Step_2
- Run the RssArticles_1.py file to collect all the news articles from news sites (Run the file in your terminal in the following way: >> python RssArticles.py). Step_3
- Run RssFeedNewArticle_2.py file to clean the news articles (JSON file) to collect only the titles and summaries so that we can use them in your machine learning model in the same way shown above. 
Step_4
- Run MLModelMLC_3.py to train our model with the cleaned news articles to be able to detect the topics for each text block. The accuracy will land between 30-40 percent, which is pretty low (since Book1.csv only contains a limited amount of annotated data), but for development purposes, it does not matter.  
Step_5
- Run MLModelMLCReturns_5.py to run our fetched articles that originated from RSS feeds. Each article will receive its multi-label classification (topics of the news) and be returned as a dictionary to be read and deposited into our database. 
Step_6
- Run DbTransfer_6.py to deposit all the labeled articles with the necessary additional data (such as date, link, etc.).