from flask import Flask, jsonify, request, render_template
import mysql.connector
import time
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf

from unicodedata import decimal

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="c0nygre",
    database="Portfolio"
)

def calculate_holdings():
    cursor2 = mydb.cursor()
    cursor2.execute("Select * from Transactions")
    transactions = cursor2.fetchall()
    cursor2.execute("Select * from Stocks")
    stocks = cursor2.fetchall()
    cursor2.close()
    stock_prices = {}
    # Convert stocks from list to dictionary
    for stock in stocks:
        stock_prices[stock[0]] = stock[1]

    holding_amounts = {}
    print(stocks)
    print(stock_prices)
    # Calculates the holding amount for each ticker
    for transaction in transactions:
        # From database: int_key, type, ticker, price, volume, date
        transaction_type = transaction[1]
        ticker = transaction[2]
        volume = transaction[4]
        if transaction_type == "SELL":
            volume = volume * -1

        if ticker in holding_amounts.keys():
            holding_amounts[ticker] += volume
        else:
            holding_amounts[ticker] = volume
    return holding_amounts, stock_prices

@app.route('/', methods=['GET'])
def start_page():
    # start up our page. Maybe call our javascript to render stuff ** CHECK
    return render_template("home.html")

# update the current price every five seconds
#@app.route('/api/currentdata', methods=['GET'])
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

@app.route('/api/holdings', methods=['GET'])
# Get the json list of transactions from our database
def get_holdings():
    holdings = []
    holding_amounts, stock_prices = calculate_holdings()
    for ticker in holding_amounts.keys():
        holding = {"ticker": ticker, "volume": holding_amounts[ticker], "curr_price": stock_prices[ticker]}
        holdings.append(holding)
    return jsonify(holdings)

@app.route('/api/transactions', methods=['GET'])
# Get the json list of transactions from our database
def get_transactions():
    cursor1 = mydb.cursor()

    cursor1.execute("Select * from Transactions")
    result = cursor1.fetchall()

    cursor1.close()
    #return jsonify(result)
    return jsonify(result)

@app.route('/api/addTransaction', methods=['POST'])
# add a transaction to our database given user inputs from payload
def add_transaction():
    transactiontype = request.json['transactiontype']
    ticker = request.json['ticker']
    quantity = request.json['quantity']

    cursor = mydb.cursor(buffered=True)
    holdings, stock_prices = calculate_holdings()
    # cursor.execute("SELECT price_today FROM stocks WHERE ticker = \'" + ticker + "\'")
    # price = cursor.fetchone()

    if ticker in stock_prices.keys():
        price = stock_prices[ticker]
    else:
        cursor.close()
        return {'error': "Ticker not available"}, 404

    if transactiontype == "SELL" and holdings[ticker] < quantity:
        cursor.close()
        return {'error': "Not enough holdings to sell"}, 404

    cursor.execute("INSERT INTO Transactions (transactiontype, ticker, price, quantity) VALUES (%s, %s, %s, %s)",
                   (transactiontype, ticker, price, quantity))

    mydb.commit()
    cursor.close()
    return jsonify({'message': 'Transaction completed successfully'})

@app.route('/api/checkPrice', methods=['GET'])
# Checks the price of a stock given a ticker
def check_stock_price():
    cursor = mydb.cursor()
    ticker = request.json['ticker']
    cursor.execute("SELECT price_today FROM stocks WHERE ticker = \'" + ticker + "\'")
    result = cursor.fetchall()

    cursor.close()
    return jsonify(result)

@app.route('/api/stocks', methods=['GET'])
# Gets the list of stocks from our database
def get_stocks():
    cursor = mydb.cursor()

    cursor.execute("Select * from Stocks")
    result = cursor.fetchall()

    cursor.close()
    return jsonify(result)

@app.route('/api/updateStock', methods=['PUT'])
# Updates the price of (one) stock given ticker
def update_stocks():
    ticker = request.json['ticker']
    price = request.json['price']
    cursor = mydb.cursor()
    cursor.execute("UPDATE Stocks SET price = %s WHERE ticker = %s", (price, ticker))
    mydb.commit()
    cursor.close()
    return jsonify({'message': 'Stocks updated successfully'})

# PORTFOLIO TABLE
# - get all items
# - add entries
#
# STOCKS TABLE
# - get all items
# - update items (current price from api)

#test to see if it can also update the tables
# mycursor.execute('''INSERT INTO Transactions(transactiontype, ticker, price, quantity)
# VALUES('BUY', 'NVDA', 110.00, 500)''')
# mydb.commit()
# print(mycursor.rowcount, "records inserted.")

if __name__ == '__main__':
    app.run()