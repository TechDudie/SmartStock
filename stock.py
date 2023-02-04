from polygon import RESTClient

get_key = lambda: open(".env").read().strip().split("=")[1]

client = RESTClient(api_key=get_key())

ticker = "MSFT"

bars = client.get_aggs(ticker=ticker, multiplier=1, timespan="day", from_="2023-02-02", to="2023-02-03")
for bar in bars:
    print(bar)
