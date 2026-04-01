import yfinance as yf

data = yf.download("AAPL", period="1mo", threads=False)
print(data.head())