import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_API_KEY = "1HXOOYLL36WV3YZL"
NEWS_KEY = "466a26e6701e4983a0db27e48cb21ae8"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "60min",
    "apikey": STOCK_API_KEY
}

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()

stock_list = [value["4. close"] for key, value in stock_data["Time Series (Daily)"].items()]
yesterday_stock = float(stock_list[0])
before_yesterday_stock = float(stock_list[1])
differences_between_stock = yesterday_stock - before_yesterday_stock
difference_in_percentage = abs(differences_between_stock) / yesterday_stock * 100

rate = ""
if difference_in_percentage > 0:
    rate = "🔺"
else:
    rate = "🔻"

if abs(difference_in_percentage) > 5:
    news_parameters = {
        "q": COMPANY_NAME,
        "apiKey": NEWS_KEY
    }

    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()
    title = news_data["articles"][0]["title"]
    content = news_data["articles"][0]["content"]

    article = f"{COMPANY_NAME}: {rate}{round(difference_in_percentage, 2)}%\n" \
              f"Headline: {title}\n" \
              f"Brief: {content}"

    # --------SEND SMS----------------

    account_sid = "ACCOUNT SID"
    auth_token = "AUTH_TOKEN"

    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=article,
        from_="YOUR TWILIO VIRTUAL NUMBER",
        to="YOUR TWILIO VERIFIED REAL  NUMBER"
    )

# ---------------SENDING EMAIL----------------------

import smtplib

MY_EMAIL = "sarunas@gmail.com"
MY_PASSWORD = "12345"

with smtplib.SMTP("smtp.gmail.com") as connection:
    connection.starttls()
    connection.login(user=MY_EMAIL, password=MY_PASSWORD)
    connection.sendmail(from_addr=MY_EMAIL, to_addrs="jonas@gmail.com", msg=article)
