CREATE DATABASE Portfolio;
USE Portfolio;

CREATE TABLE Stocks (
Ticker		varchar(10) unique primary key,
Price_Today	 decimal(10, 2) not null ,
Available_amount int not null
);

CREATE TABLE Transactions (
transactionid 		int	auto_increment primary key,
transactiontype		enum('BUY', 'SELL') not null,
ticker				varchar(10) not null,
price				decimal(10, 2) not null,
quantity			int not null,
transaction_date	timestamp default current_timestamp,
foreign key (ticker) references Stocks(Ticker)
);

INSERT INTO Stocks (Ticker, Price_Today, Available_amount)
VALUES
('AAPL', 218.33, 1000),
('TSLA', 222.63, 1000),
('AMZN', 181.35, 1000),
('NVDA', 106.05, 1000 ),
('GOOGL', 170.15, 1000);

INSERT INTO Transactions (transactiontype, ticker, price, quantity)
VALUES
('BUY', 'TSLA', 100, 100),
('SELL', 'TSLA', 400, 100);

DELIMITER //

CREATE TRIGGER after_buy_transaction
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
	IF NEW.transactiontype = 'BUY' THEN
		UPDATE Stocks
		SET Available_amount = Available_amount - NEW.quantity
		WHERE Ticker = new.ticker;
	END IF;
END;
//

CREATE TRIGGER after_sell_transaction
AFTER INSERT ON Transactions
FOR EACH ROW
BEGIN
    IF NEW.transactiontype = 'SELL' THEN
        UPDATE Stocks
        SET Available_amount = Available_amount + NEW.quantity
        WHERE Ticker = NEW.ticker;
    END IF;
END;

//
DELIMITER ;


select * from transactions;
select * from stocks;