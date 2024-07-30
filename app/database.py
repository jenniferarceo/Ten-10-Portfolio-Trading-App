import mysql.connector
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345678!",
    database="Portfolio"
)
print(mydb)

#test to see if the connection worked
mycursor = mydb.cursor()

mycursor.execute("Select * from Stocks")
result = mycursor.fetchall()

for row in result:
    print(row)


#test to see if it can also update the tables
# mycursor.execute('''INSERT INTO Transactions(transactiontype, ticker, price, quantity)
# VALUES('BUY', 'NVDA', 110.00, 500)''')
# mydb.commit()
# print(mycursor.rowcount, "records inserted.")
