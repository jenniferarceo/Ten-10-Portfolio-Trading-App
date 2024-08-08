# Ten-10 Porfolio Trading App

The Ten-10 Portfolio Trading App is a web-based application designed to help users manage and track their stock portfolios. It allows users to view their holdings, add and manage transactions, and see real-time updates of stocks prices and porfolio performance. The application is built using Flask for the backend and MySQL for data storage, with a frontend that provides interactive visualizations and data tables.

---

## Features

* **Real-Time Stock Prices**: Fetches and displays current stocks prices for selected S&P 500 tickers.
* **Transaction Management**: Add, view, and manage buy and sell transactions.
* **Portfolio Performance Visual**: Interactive line and pie charts to visualize portfolio performance and distribution.
* **User Interface**: Simple and intuitive UI Boostrap and CanvasJS for a responsive design.

---

## Project Structure

```plaintext
app/
├── static/
│   ├── script.js      # JavaScript code for front-end logic and chart rendering
│   ├── styles.css     # CSS styles for the application
│   └── db.sql         # SQL script to set up the database
├── templates/
│   └── home.html      # HTML template for the main page
└── server.py          # Flask application server code
```
---

## Requirements

* Python 3.x
* Flask
* MySQL Database
* Pandas
* Numpy
* yfinance
* mysql-connector-Python
* Boostrap (included via CDN in HTML)

---

## Installation

1. Clone the repository:

```bash
git clone https://z3iim1t62buo12q1xdeqew2g-admin@bitbucket.org/kelly-foundations-coursework/portfolio-ten-team-10-jennifer-kelly-oruru.git
cd portfolio-ten-team-10-jennifer-kelly-oruru
```

2. Set up a virtual enviroment:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

3. Set up the MySql database:

```sql
CREATE DATABASE Portfolio;
USE Portfolio;

CREATE TABLE Transactions (
    transactionid      INT AUTO_INCREMENT PRIMARY KEY,
    transactiontype    ENUM('BUY', 'SELL') NOT NULL,
    ticker             VARCHAR(10) NOT NULL,
    price              DECIMAL(10, 2) NOT NULL,
    quantity           INT NOT NULL,
    transaction_date   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

```

4. Edit database configuration:

    * Open `server.py` and update the database connection parameters (host, user, password, database) to match your MySQL configuration.

---

## Usage

1. Start the Flask server:

```bash
flask run
```
The application will start on `http://127.0.0.1:5000/`.

2. Access the application:

    * Open your web browser and navigate to `http://127.0.0.1:5000/` to view the homepage.

3. Application Interface:
    
    * **Place new order**: Enter the ticker, select the transaction type (BUY/SELL), and enter quantity. Use "CHECK PRICE" to fetch the current price, and "ORDER" to execute the transaction.
    * **Holdings table**: Displays current holdings including ticker, quantity, and price.
    * **Transactions Table**: Shows a history of buy/sell transactions with details.
    * **Portfolio Performance**: A live updating line graph displays the total unrealized PNL, and a pie chart shows the stock distribution in the portfolio.

---

## Files Overview

`server.py`

* Implements the Flask server to handle HTTP requests.
* Provides API endpoints for managing transactions and retrieving stock data.
* Integrates with Yahoo Finance to update stock prices in real-time.

`static/script.js`

* JavaScript function to manage front-end interactivity.
* Updates holdings and transaction tables, displays charts, and validates input.
* Fetches data from the backend and updates the UI every 5 seconds.

`static/styles.css`

* Custom styling for styling the application UI.
* Ensures consistency and responsive design across different devices.

`static/db.sql`

* SQL script to set up the initial database schema for transactions.
* Defines the structure of the `Transactions` table.

`templates/home/html`

* HTML structure of the application's main page.
* Includes Bootstrap for styling and layout, and integrates JS/CSS for the interactive features.

---

## Troubleshooting

* **Database Connection Issues**: Verify that the MySQL server is running and accessible. Ensure the connection details in `server.py` are correct.
* **API or Data Errors**: Check for network issues or API limits with Yahoo Finance. Ensure data is fetched correctly.
* **Dependency Problems**: Make sure all required packages are installed and acitvated in your virtual environment.

---

## License

Distributed under the MIT License. See `License.txt` for more information.

