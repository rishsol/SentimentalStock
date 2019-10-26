import nltk
nltk.downloader.download('vader_lexicon')
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests

sia = SentimentIntensityAnalyzer()

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

sentiments = []
news_list = []
passage_list = []
passage = ""

for i in range(1, 3):
    page = urlopen('https://www.businesstimes.com.sg/search/facebook?page='+str(i)).read()
    soup = BeautifulSoup(page, features="html.parser")
    posts = soup.findAll("div", {"class": "media-body"})
    for post in posts:
        url = post.a['href']
        try:
            html_info = urlopen(url).read()
            soup = BeautifulSoup(html_info)
            sentences = soup.findAll("p")

            for sentence in sentences:
                passage += sentence.text

            passage_list.append(passage)
        except:
            continue

#print(passage_list)

for passage in passage_list:
    sentiment = sia.polarity_scores(passage)['compound']
    sentiments.append(sentiment)

print(sentiments)

#html_info = urlopen(news_list[0].read())
#print(html_info)
#soup = BeautifulSoup(html_info)
#sentences = soup.find_all("p")
#stuff = urlopen(news_list[0]).read()
#soup = BeautifulSoup(stuff)
#words = soup.find_all('p')
#print(words)

#for url in news_list:
#    html_information = urlopen(url).read()
#    soup = BeautifulSoup(html_information)
#    sentences = soup.find_all('p')
#
#    for sentence in sentences:
#       passage += sentence.text

#    passage_list.append(passage)


#print(passage_list)





        #date = post.time.text
        #print(date, url)
        #try:
         #   link_page = urlopen(url).read()
        #except:
         #   url = url[:-2]
          #  link_page = urlopen(url).read()
        #link_soup = BeautifulSoup(link_page)
        #sentences = link_soup.findAll("p")
        #passage = ""
        #for sentence in sentences:
         #   passage += sentence.text
        #sentiment = sia.polarity_scores(passage)['compound']
        #date_sentiments.setdefault(date, []).append(sentiment)

#date_sentiment = {}

#for k,v in date_sentiments.items():
 #   date_sentiment[datetime.strptime(k, '%d %b %Y').date() + timedelta(days=1)] = round(sum(v)/float(len(v)),3)

#earliest_date = min(date_sentiment.keys())

#print(date_sentiment)