import time
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf

# dt = datetime(2024, 1, 1)
# start_date = int(round(dt.timestamp()))

# dt = datetime(2024, 8, 7)
# end_date = int(round(dt.timestamp()))

# stock = 'GOOGL'

# df = pd.read_csv(f"https://query1.finance.yahoo.com/v7/finance/download/{stock}?period1={start_date}&period2={end_date}&interval=1d&events=history&includeAdjustedClose=true",
#     parse_dates = ['Date'], index_col='Date')

# print(df)

#test with 5 tickers
#tickers = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']
#test with 100 tickers hard coded
# tickers = [
#     "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "V",
#     "UNH", "LLY", "XOM", "JNJ", "JPM", "WMT", "MA", "PG", "ORCL", "MRK",
#     "AVGO", "HD", "CVX", "PEP", "KO", "COST", "MCD", "ABBV", "ADBE", "CRM",
#     "TMO", "NKE", "PFE", "ASML", "BMY", "MDT", "LIN", "DHR", "TXN", "CMCSA",
#     "DIS", "VZ", "HON", "ABT", "SCHW", "PM", "IBM", "QCOM", "ACN", "LMT",
#     "AMD", "AMT", "CHTR", "CAT", "ELV", "BLK", "DE", "NE", "INTU", "MU",
#     "NEE", "PYPL", "UPS", "AXP", "RTX", "SPGI", "AMGN", "AMAT", "GILD", "MO",
#     "MS", "BA", "T", "NOW", "ISRG", "BKNG", "MDLZ", "MMM", "ADP", "LOW",
#     "SLB", "ZTS", "C", "AON", "COP", "CL", "MMM", "SBUX", "TJX", "TGT",
#     "MCO", "CI", "GS", "CB", "MMC", "GE", "FIS", "USB", "PLD"
# ]
#take only part of it to see how fast it runs 
# tickers = [
#     "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "V",
#     "UNH", "LLY", "XOM", "JNJ", "JPM", "WMT", "MA", "PG", "ORCL", "MRK",
#     "AVGO", "HD", "CVX", "PEP", "KO", "COST", "MCD", "ABBV", "ADBE", "CRM",
#     "TMO", "NKE", "PFE", "ASML", "BMY", "MDT", "LIN", "DHR", "TXN", "CMCSA",
#     "DIS", "VZ", "HON", "ABT", "SCHW", "PM", "IBM", "QCOM", "ACN", "LMT",
#     "AMD", "AMT", "CHTR", "CAT", "ELV", "BLK", "DE", "NE", "INTU", "MU"]


# data = yf.download(tickers, period="1d", group_by='ticker')
# current_data = pd.DataFrame()

# for ticker in tickers:
#     try:
#         current_data.loc[ticker, 'Current Price'] = data[ticker].iloc[-1]['Close']
#         current_data.loc[ticker, 'Volume'] = data[ticker].iloc[-1]['Volume']
#     except Exception as e:
#         print(f"Failed to fetch data for {ticker}: {str(e)}")
# print(current_data)
       
# print(len(tickers))



# update the current price every five seconds
def get_current_data(tickers):
    data = {}
    for ticker in tickers:
        stock = yf.Ticker(ticker)
        info = stock.history(period="1d", interval="1m")
        if not info.empty:
            current_price = info.iloc[-1]['Close']
            #volume = info.iloc[-1]['Volume']
            data[ticker] = {
                'Current Price': current_price,
                #'Volume': volume
            }
            print(f"Ticker: {ticker}, Current Price: {current_price}") #, Volume: {volume}
    return data

#list of tickers to track
tickers = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "V",
    "UNH", "LLY", "XOM", "JNJ", "JPM", "WMT", "MA", "PG", "ORCL", "MRK",
    "AVGO", "HD", "CVX", "PEP", "KO", "COST", "MCD", "ABBV", "ADBE", "CRM",
    "TMO", "NKE", "PFE", "ASML", "BMY", "MDT", "LIN", "DHR", "TXN", "CMCSA",
    "DIS", "VZ", "HON", "ABT", "SCHW", "PM", "IBM", "QCOM", "ACN", "LMT",
    "AMD", "AMT", "CHTR", "CAT", "ELV", "BLK", "DE", "NE", "INTU", "MU"
    ]
try: 
    while True:
        #fetch and display the data every 5 seconds
        current_data = get_current_data(tickers)
        time.sleep(5)
except KeyboardInterrupt:
    print("Data retrieval stopped by user.")

            