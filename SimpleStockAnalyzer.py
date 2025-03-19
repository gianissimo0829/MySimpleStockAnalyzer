import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

stockInput = "JBFCY"

# Download historical data for the company
stock = yf.download(stockInput, start="2020-01-01", end="2024-01-01")

# Download PHP/USD exchange rate (USD to PHP)
exchange_rate = yf.download("PHP=X", start="2020-01-01", end="2024-01-01")

# Ensure exchange_rate is a Series (extract 'Close' column properly)
if isinstance(exchange_rate, pd.DataFrame):  
    exchange_rate = exchange_rate["Close"]

# Align exchange rate data with stock data
exchange_rate = exchange_rate.reindex(stock.index).ffill()

# Multiply only if both are Series
stock["Close_PHP"] = stock["Close"].squeeze() * exchange_rate.squeeze()
# Display first few rows
print(stock[["Close_PHP"]].head())

# Visualize Stock Prices
plt.figure(figsize=(12,6))
plt.plot(stock.index, stock["Close_PHP"], label=stockInput+" in PHP", color="blue")
plt.title(stockInput+" Stock Price in PHP")
plt.xlabel("Date")
plt.ylabel("Price (PHP)")
plt.legend()
plt.grid()
plt.show()

# Get a SMA 
stock['SMA_50'] = stock['Close'].rolling(window=50).mean()
stock['SMA_200'] = stock['Close'].rolling(window=200).mean()

plt.figure(figsize=(12,6))
plt.plot(stock['Close'], label=stockInput+' Closing Price', alpha=0.6)
plt.plot(stock['SMA_50'], label='50-Day SMA', linestyle='dashed')
plt.plot(stock['SMA_200'], label='200-Day SMA', linestyle='dashed')
plt.legend()
plt.show()

