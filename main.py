import requests

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "interval": "60min",
    "apikey": "1HXOOYLL36WV3YZL"
}

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

response = requests.get(url=STOCK_ENDPOINT, params=parameters)
response.raise_for_status()
data = response.json()
print(data["Time Series (Daily)"])

stock_list = [value["4. close"] for key, value in data["Time Series (Daily)"].items()]
print(stock_list)
yesterday_stock = float(stock_list[1])
before_yesterday_stock = float(stock_list[2])
print(yesterday_stock, before_yesterday_stock)
differences_between_stock = abs(yesterday_stock - before_yesterday_stock)
min_value = min(yesterday_stock, before_yesterday_stock)
difference_in_percentage = differences_between_stock * 100 / min_value
print(min_value)
print(differences_between_stock)
print(difference_in_percentage)

if difference_in_percentage > 5:
    print("Get News")


def get_news():
    pass


