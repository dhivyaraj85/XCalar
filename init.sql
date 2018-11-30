CREATE TABLE customer(
 cust_id int  PRIMARY KEY,
 first_name VARCHAR (50) NOT NULL,
 last_name VARCHAR (50) NOT NULL,
 street_address VARCHAR (100) NOT NULL,
 city VARCHAR (30) NOT NULL,
 state_name VARCHAR (2) NOT NULL,
 zipcode int NOT NULL,
 created_on TIMESTAMP NOT NULL
);

CREATE TABLE accounts_info(
 account_number varchar(20)  PRIMARY KEY,
 balance NUMERIC(20,2) NOT NULL,
 created_on TIMESTAMP NOT NULL
);

CREATE TABLE customer_accounts_info(
 cust_id int,
 account_number varchar(20)
);
