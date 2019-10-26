import Financials
import matplotlib.pyplot as plt

plt.plot(range(len(Financials.sentiments)), Financials.sentiments)
plt.title('Sentiment of Articles about Facebook on "The Business Times" Over Time')
plt.ylabel('Sentiment Index')
plt.xlabel('Day')
plt.show()