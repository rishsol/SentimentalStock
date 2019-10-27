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
date_list.reverse()
plt.plot(range(len(sentiments)), sentiments)
plt.title('Sentiment of Articles about ' + company.upper() + ' on "The Business Times" Over Time')
plt.ylabel('Sentiment Index')
plt.xlabel('Time Period')
plt.tight_layout()
st.pyplot()

def sentimentStatement():
    tOld = date_list[0]
    tRecent = date_list[len(date_list) - 1]
    if(sentiments[0] > sentiments[len(sentiments) - 1]):
        return 'Sentiment has decreased by ' + str(round(sentiments[0] - sentiments[len(sentiments) - 1], 5)) + ' from ' + tOld + ' to ' + tRecent
    elif(sentiments[0] < sentiments[len(sentiments) - 1]):
        return 'Sentiment has increased by ' + str(round(sentiments[len(sentiments) - 1]) - sentiments[0], 5) + ' from ' + tOld+ ' to ' + tRecent
    else:
        return 'Sentiment has not changed from ' + tOld + ' to ' + tRecent

st.write('Time Period 0 represents ' + date_list[0] + ' while the final time period (time period ' + str(len(sentiments)) + ') represents ' + date_list[len(date_list) - 1] + '. '
         'A downward trend shows a decline in positive sentiment, while an upwards trend represents a rise in positive sentiment.')
st.write()
st.write(sentimentStatement())