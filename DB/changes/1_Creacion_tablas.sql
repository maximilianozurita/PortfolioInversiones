CREATE TABLE stats.tickets (
	ticket_code varchar(50) PRIMARY KEY UNIQUE,
	name varchar(50) not null,
	ratio INT,
	date BIGINT
);

CREATE TABLE stats.equity (
	id INT AUTO_INCREMENT PRIMARY KEY UNIQUE not null,
	ticket_code varchar(50) not null UNIQUE,
	ppc FLOAT not null,
	quantity INT not null,
	weighted_date BIGINT not null,
	FOREIGN KEY (ticket_code) REFERENCES tickets(ticket_code)
);

CREATE TABLE stats.history (
	id INT AUTO_INCREMENT PRIMARY KEY UNIQUE,
	ticket_code varchar(50) not null,
	ratio INT,
	transaction_key INT,
	broker_name varchar(50),
	quantity INT not null,
	unit_price FLOAT not null,
	usd_quote INT not null,
	date BIGINT,
	FOREIGN KEY (ticket_code) REFERENCES tickets(ticket_code)
);
