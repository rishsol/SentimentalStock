import nltk
nltk.downloader.download('vader_lexicon')
import warnings
warnings.filterwarnings('ignore')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()

from urllib.request import urlopen
from bs4 import BeautifulSoup

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

for passage in passage_list:
    sentiment = sia.polarity_scores(passage)['compound']
    sentiments.append(sentiment)

sentiments.reverse()