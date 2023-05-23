# This scripts extracts RSS-feed from the online News-sites
# it is then cleans and structures them to be imported by another script

# Import packages
import feedparser


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