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

sentiments = []
date_list = []
passage_list = []
passage = ""
company = st.text_input('Enter a publicly traded company')
company = company.strip().upper()

#below algorithm made with reference to jasonyip184 GitHub repo StockSentimentTrading
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
#end of algo reference

def sentimentStatement():
    tOld = date_list[0]
    tRecent = date_list[len(date_list) - 1]
    if(sentiments[0] > sentiments[len(sentiments) - 1]):
        return 'Sentiment has decreased by ' + str(round(sentiments[0] - sentiments[len(sentiments) - 1], 5)) + ' points from ' + tOld + ' to ' + tRecent + ' for ' + company + '.'
    elif(sentiments[0] < sentiments[len(sentiments) - 1]):
        return 'Sentiment has increased by ' + str(round(sentiments[len(sentiments) - 1] - sentiments[0], 5)) + ' points from ' + tOld + ' to ' + tRecent + ' for ' + company + '.'
    else:
        return 'Sentiment has not changed from ' + tOld + ' to ' + tRecent + ' for ' + company + '. It remains at ' + str(sentiments[0]) + '.'

if(len(date_list) == 0):
    st.write('Sorry, either that company does not exist or The Business Times has no articles on it')
else:
    for passage in passage_list:
        sentiment = sia.polarity_scores(passage)['compound']
        sentiments.append(sentiment)

    sentiments.reverse()
    date_list.reverse()
    plt.plot(range(len(sentiments)), sentiments)
    plt.title('Sentiment of Articles about ' + company.upper() + ' in "The Business Times" Over Time')
    plt.ylabel('Sentiment Index')
    plt.xlabel('Time Period')
    plt.xticks(range(len(sentiments)))
    plt.tight_layout()
    st.pyplot()

    st.write('Each time period represents a date when "The Business Times" wrote an article about ' + company +
         '. The first time period, time period 0, represents the oldest  article about ' + company + ' I was able to scrape. Here, time period 0 represents ' + date_list[0] +
        '. The final time period (time period ' + str(len(sentiments) - 1) + ') represents the latest article on ' + company + ' and here, it represents ' + date_list[len(date_list) - 1] + '. I could not just'
        ' add theses dates since the labels would not be able to fit within the graph otherwise. A downward trend shows a decline in positive sentiment, while an upwards trend represents a rise in positive sentiment.')
    st.write()

    st.write(sentimentStatement())
    st.write()

    difference = sentiments[0] - sentiments[len(sentiments) - 1]
    if(difference > 1 ):
        st.write('Thus, company public opinion has declined rather significantly over the time period.')
    elif(difference < -1):
        st.write('Thus, company public opinion has appreciated significantly over the time period.')
    elif(difference > 0.5):
        st.write('Thus, there has been a decent decline in public opinion of the company over the time period.')
    elif(difference < -0.5):
        st.write('Thus, there has been a decent rise in public opinion of the company over the time period.')
    else:
        st.write('Thus, there has not been an appreciable change in public opinion of the company over the time period.')