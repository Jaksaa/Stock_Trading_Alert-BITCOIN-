import requests
import datetime
from twilio.rest import Client


day = datetime.date.today()
yesterday = day - datetime.timedelta(days=1)
day_before_yesterday = day - datetime.timedelta(days=2)

ACCOUNT_SID = ""
AUTH_TOKEN = ""
STOCK_API_KEY = ""
NEWS_API_KEY = ""
COMPANY_SYMBOL = "BTCUSDT"

params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": COMPANY_SYMBOL,
        "apikey": STOCK_API_KEY
}

params_for_news = {
        "q": "bitcoin",
        "language": "en",
        "from": f"{day}",
        "sortBy": "popularity",
        "apiKey": NEWS_API_KEY
}

response = requests.get(url='https://www.alphavantage.co/query', params=params)
response.raise_for_status()
data = response.json()

yesterday_data_price_close = float(data['Time Series (Daily)'][f'{yesterday}']['4. close'])
day_before_yesterday_data_price_close = float(data['Time Series (Daily)'][f'{day_before_yesterday}']['4. close'])

diff = round(yesterday_data_price_close - day_before_yesterday_data_price_close, 4)
diff_percent = round(abs(diff/yesterday_data_price_close) * 100, 2)

up_or_down = None
if diff > 0:
        what_does_it_mean = "increase"
        up_or_down = '📈'
else:
        what_does_it_mean = "decrease"
        up_or_down = '📉'

article_response = requests.get(url='https://newsapi.org/v2/everything', params=params_for_news)
article_response.raise_for_status()
news_data = article_response.json()

news_to_send = []
for source in range(len(news_data['articles'])):
        news_to_send.append(f"{news_data['articles'][source]['title']} " "|" f" {news_data['articles'][source]['url']}")

client = Client(ACCOUNT_SID, AUTH_TOKEN)

message = client.messages.create(
                     body=f"The BITCOIN / TETHERUS current difference compared to yesterday and day before yesterday is: {diff}, that's a {diff_percent}% {what_does_it_mean}{up_or_down}. "
                          f"Below are top three articles with topic related to bitcoin:\n{news_to_send[0]}\n{news_to_send[1]}\n{news_to_send[2]}",
                     from_='',
                     to=''
                 )
print(message.sid)








