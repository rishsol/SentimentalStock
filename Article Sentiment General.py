import nltk
nltk.downloader.download('vader_lexicon')
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import matplotlib.pyplot as plt


sia = SentimentIntensityAnalyzer()

from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time

sentiments = []
news_list = []
passage_list = []
passage = ""

company = input("Enter a publicly traded company")
for i in range(1, 3):
    page = urlopen('https://www.businesstimes.com.sg/search/' + company + '?page='+str(i)).read()
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

for passage in passage_list:
    sentiment = sia.polarity_scores(passage)['compound']
    sentiments.append(sentiment)

sentiments.reverse()


plt.plot(range(len(sentiments)), sentiments)
plt.title('Sentiment of Articles about ' + company.upper() + ' on "The Business Times" Over Time')
plt.ylabel('Sentiment Index')
plt.xlabel('Day')
plt.show()