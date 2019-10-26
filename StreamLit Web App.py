import streamlit as st
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

sentiments = []
date_list = []
passage_list = []
passage = ""
company = st.text_input('Enter a publicly traded company')

for i in range(1, 3):
    page = urlopen('https://www.businesstimes.com.sg/search/' + company + '?page='+str(i)).read()
    soup = BeautifulSoup(page, features='html.parser')
    posts = soup.findAll('div', {'class': 'media-body'})
    for post in posts:
        url = post.a['href']
        try:
            date = post.time.text
            html_info = urlopen(url).read()
            soup = BeautifulSoup(html_info)
            sentences = soup.findAll('p')

            for sentence in sentences:
                passage += sentence.text

            passage_list.append(passage)
            date_list.append(date)
        except:
            continue

for passage in passage_list:
    sentiment = sia.polarity_scores(passage)['compound']
    sentiments.append(sentiment)

sentiments.reverse()
#range(len(sentiments))
d = datetime.today()
plt.plot(range(len(sentiments)), sentiments)
plt.title('Sentiment of Articles about ' + company.upper() + ' on "The Business Times" Over Time')
plt.ylabel('Sentiment Index')
plt.xlabel('Day')
plt.tight_layout()
st.pyplot()

st.write('Day 0 represents the least recent article written on the company, while the final day represents the most recent story on the company. '
         'A downward trend thus shows a decline in positive sentiment, although a minimum sentiment of above 0.5 is still generally acceptable, and may be considered a worthwhile investment.')
#st.write('Day 0 Represents ' + str(len(sentiments)) + ' days since today (' + str(d) + '), or ' + str((d - timedelta(days=len(sentiments)))))