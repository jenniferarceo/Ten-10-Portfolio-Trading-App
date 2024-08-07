CREATE DATABASE Portfolio;
USE Portfolio;


CREATE TABLE Transactions (
transactionid 		int	auto_increment primary key,
transactiontype		enum('BUY', 'SELL') not null,
ticker				varchar(10) not null,
price				decimal(10, 2) not null,
quantity			int not null,
transaction_date	timestamp default current_timestamp
);