from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678!",
    database="Portfolio"
)

@app.route('/', methods=['GET'])
def start_page():
    # start up our page. Maybe call our javascript to render stuff ** CHECK
    return render_template("home.html")

@app.route('/api/transactions', methods=['GET'])
# Get the json list of transactions from our database
def get_transactions():
    cursor = mydb.cursor()

    cursor.execute("Select * from Transactions")
    result = cursor.fetchall()

    cursor.close()
    #return jsonify(result)
    return jsonify(result)


@app.route('/api/add-transaction', methods=['POST'])
# add a transaction to our database given user inputs from payload
def add_transaction():
    transactiontype = request.json['transactiontype']
    ticker = request.json['ticker']
    quantity = request.json['quantity']
    type = request.json['type'] # Buy or Sell

    cursor = mydb.cursor()
    cursor.execute("Select price from Stocks WHERE ticker == %s", ticker)
    price = cursor.fetchall()

    cursor.execute("INSERT INTO Transactions (transactiontype, ticker, price, quantity) VALUES (%s, %s, %s, %s)",
                   (transactiontype, ticker, price, quantity))

    mydb.commit()
    cursor.close()
    return jsonify({'message': 'Transaction completed successfully'})

@app.route('/api/check-price', methods=['GET'])
# Checks the price of a stock given a ticker
def check_stock_price():
    cursor = mydb.cursor()
    ticker = request.json['ticker']
    cursor.execute("Select price from Stocks where ticker == %s", ticker)
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

@app.route('/api/update-stock', methods=['PUT'])
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