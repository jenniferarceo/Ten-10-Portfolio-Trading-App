from flask import Flask, jsonify, request, render_template
import mysql.connector

app = Flask(__name__)
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="c0nygre",
    database="Portfolio"
)
@app.route('/', methods=['GET'])
def start_page():
    # return "Hello World"
    return render_template("home.html")

@app.route('/transactions', methods=['GET'])
def get_transactions():
    cursor = mydb.cursor()

    cursor.execute("Select * from Transactions")
    result = cursor.fetchall()

    cursor.close()
    return jsonify(result)


@app.route('/transactions', methods=['POST'])
def add_transaction():
    transactiontype = request.json['transactiontype']
    ticker = request.json['ticker']
    price = request.json['price']
    quantity = request.json['quantity']

    cursor = mydb.cursor()
    cursor.execute("INSERT INTO Transactions (transactiontype, ticker, price, quantity) VALUES (%s, %s, %s, %s)",
                   (transactiontype, ticker, price, quantity))

    mydb.commit()
    cursor.close()
    return jsonify({'message': 'Transaction completed successfully'})


@app.route('/stocks', methods=['GET'])
def get_stocks():
    cursor = mydb.cursor()

    cursor.execute("Select * from Stocks")
    result = cursor.fetchall()

    cursor.close()
    return jsonify(result)


@app.route('/stocks', methods=['PUT'])
def update_stocks():
    ticker = request.json['ticker']
    price = request.json['price']
    cursor = mydb.cursor()

    for t in ticker:
        cursor.execute("UPDATE Stocks SET price = %s WHERE ticker = %s", (price, ticker))

    mydb.commit()
    cursor.close()
    return jsonify({'message': 'Stock updated successfully'})

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

@app.route('/form', methods=['PUT'])
def test_form():
    return None

if __name__ == '__main__':
    app.run()