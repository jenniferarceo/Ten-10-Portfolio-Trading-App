from flask import Flask, jsonify, request, render_template
import mysql.connector
import time
from datetime import datetime
import numpy as np
import pandas as pd
import yfinance as yf
import threading
from decimal import Decimal

from unicodedata import decimal

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678!",
    database="Portfolio"
)

# list of tickers to track
tickers = [
    "AAPL", "MSFT", "AMZN", "NVDA", "GOOGL", "GOOG", "META", "TSLA", "V",
    "UNH", "LLY", "XOM", "JNJ", "JPM", "WMT", "MA", "PG", "ORCL", "MRK",
    "AVGO", "HD", "CVX", "PEP", "KO", "COST", "MCD", "ABBV", "ADBE", "CRM",
    "TMO", "NKE", "PFE", "ASML", "BMY", "MDT", "LIN", "DHR", "TXN", "CMCSA",
    "DIS", "VZ", "HON", "ABT", "SCHW", "PM", "IBM", "QCOM", "ACN", "LMT",
    "AMD", "AMT", "CHTR", "CAT", "ELV", "BLK", "DE", "NE", "INTU", "MU"
]


# get current data for tickers
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
                'Current Price': round(Decimal(current_price), 2),
                #'Volume': volume
            }
            #print(f"Ticker: {ticker}, Current Price: {current_price}") #, Volume: {volume}
    return data


current_data = get_current_data(tickers)


#continously update the data in the background
def update_data(ticker_list):
    while True:
        try:
            #fetch and display the data every 5 seconds
            global current_data
            current_data = get_current_data(ticker_list)
            time.sleep(5)
        except Exception as e:
            print(f"Data retrieval error: {str(e)}")


#run in the background
threading.Thread(target=update_data, args=(tickers,), daemon=True).start()


def calculate_holdings():
    cursor2 = mydb.cursor()
    cursor2.execute("Select * from Transactions")
    transactions = cursor2.fetchall()
    cursor2.close()

    holding_amounts = {}
    holding_realized_pnls = {}
    holding_unrealized_pnls = {}
    # Calculates the holding amount for each ticker
    for transaction in transactions:
        # From database: int_key, type, ticker, price, volume, date
        transaction_type = transaction[1]
        ticker = transaction[2]
        purchase_price = transaction[3]
        volume = transaction[4]

        if transaction_type == "SELL":
            volume = volume * -1

        if ticker in holding_amounts.keys():
            holding_amounts[ticker] += volume
            holding_realized_pnls[ticker] += volume * -1 * purchase_price
        else:
            holding_amounts[ticker] = volume
            holding_realized_pnls[ticker] = volume * -1 * purchase_price

        #transaction[4] is volume as positive number always
    print("Current Data contains: " + str(current_data))
    print("Type of price: " + str(type(current_data["TSLA"]['Current Price'])))
    for ticker in holding_amounts.keys():
        holding_unrealized_pnls[ticker] = holding_amounts[ticker] * current_data[ticker]['Current Price'] + \
                                          holding_realized_pnls[ticker]

    return holding_amounts, current_data, holding_realized_pnls, holding_unrealized_pnls


@app.route('/', methods=['GET'])
def start_page():
    # start up our page. Maybe call our javascript to render stuff ** CHECK
    return render_template("home.html")


@app.route('/api/holdings', methods=['GET'])
# Get the json list of transactions from our database
def get_holdings():
    holdings = []
    holding_amounts, stock_prices, holding_realized_pnls, holding_unrealized_pnls = calculate_holdings()
    for ticker in holding_amounts.keys():
        holding = {"ticker": ticker, "volume": holding_amounts[ticker],
                   "curr_price": stock_prices[ticker]['Current Price'], \
                   "realized_pnl": holding_realized_pnls[ticker], "unrealized_pnl": holding_unrealized_pnls[ticker]}
        holdings.append(holding)
    return jsonify(holdings)


@app.route('/api/transactions', methods=['GET'])
# Get the json list of transactions from our database
def get_transactions():
    cursor1 = mydb.cursor()

    cursor1.execute("Select * from Transactions")
    result = cursor1.fetchall()

    cursor1.close()
    return jsonify(result)


@app.route('/api/addTransaction', methods=['POST'])
# add a transaction to our database given user inputs from payload
def add_transaction():
    transactiontype = request.json['transactiontype']
    ticker = request.json['ticker']
    quantity = request.json['quantity']

    cursor = mydb.cursor(buffered=True)
    holdings, stock_prices, holding_realized_pnls, holding_unrealized_pnls = calculate_holdings()

    if ticker in current_data.keys():
        price = current_data[ticker]['Current Price']
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


@app.route('/api/checkPrice/<string:ticker>', methods=['GET'])
# Checks the price of a stock given a ticker
def check_stock_price(ticker):
    price = current_data[ticker]['Current Price']
    print(price)
    if price:
        return jsonify(price)
    else:
        return jsonify({'error': 'Price not found'}), 404


@app.route('/api/stocks', methods=['GET'])
# Gets the list of stocks from our database
def get_stocks():
    return jsonify(current_data)


# @app.route('/api/updateStock', methods=['PUT'])
# # Updates the price of (one) stock given ticker
# def update_stocks():
#     ticker = request.json['ticker']
#     price = request.json['price']
#     cursor = mydb.cursor()
#     cursor.execute("UPDATE Stocks SET price = %s WHERE ticker = %s", (price, ticker))
#     mydb.commit()
#     cursor.close()
#     return jsonify({'message': 'Stocks updated successfully'})


if __name__ == '__main__':
    app.run()
