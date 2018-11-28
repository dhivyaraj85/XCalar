#!/usr/bin/python
import psycopg2
from config import config
from psycopg2.extras import execute_values

import random
import numpy as np
import argparse

from faker import Faker

parser = argparse.ArgumentParser()
parser.add_argument("--customers", type=int,help="enter the number of customers; default is 1000",default=1000)
parser.add_argument("--max_accounts", type=int,help="enter the maximum number of accounts per customer; default is 10",default=10)

args = parser.parse_args()
count = args.customers 
max_acc = args.max_accounts

fake = Faker()
fake.seed(4321)

# count_str = input("Enter the number of customers: ")
# count_str2 = input("Enter the maximum number of accounts: ")


cust_list = []
acc_list = []
acc_nos_list = []
cust_acc_list  = []

for i in range(1, count+1):
    print("user no: " + repr(i))
    cust_id = i
    first_name = fake.first_name()
    last_name = fake.last_name()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr(include_territories=True)
    zipcode = fake.zipcode()
    creation_timestamp = fake.past_datetime(start_date="-30d", tzinfo=None)
    cust_details = (cust_id,first_name,last_name,street_address,city,state,zipcode,creation_timestamp)
    cust_list.append(cust_details)	
    user_total_acc = random.randint(1, max_acc)
    print("no of accounts for this user = " + repr(user_total_acc))
    total_acc = len(acc_list)
    print("total existing accounts = " + repr(total_acc))
    if(user_total_acc <= total_acc):
        print("user_total_acc <= total_acc")
        user_new_acc = random.randint(1, user_total_acc)
        print("no of new acc for this user = " + repr(user_new_acc))
        user_existing_acc = user_total_acc - user_new_acc
        print("no of existing acc for this user = " + repr(user_existing_acc))
        existing_arr = random.sample(acc_nos_list, user_existing_acc)
        print("existing_arr LIST: " + repr(existing_arr))
        #existing_arr = np.random.choice(acc_nos_list, user_existing_acc, replace=False)
    else:
        print("user accounts is greater than total existing acc")
        if(total_acc == 0):
            user_new_acc = user_total_acc
            user_existing_acc = 0
        else:
            user_existing_acc = random.randint(1, total_acc)
            print("random no of existing accounts = " + repr(user_existing_acc))
            #existing_arr = np.random.choice(acc_nos_list, user_existing_acc, replace=False)
            existing_arr = random.sample(acc_nos_list, user_existing_acc)
            user_new_acc = user_total_acc - user_existing_acc
    for j in range(1, user_existing_acc+1):
        acc_no = existing_arr[j-1]
        cust_acc_details = (cust_id,acc_no)
        cust_acc_list.append(cust_acc_details)
    for k in range(1, user_new_acc+1):
        acc_no = fake.bban()
        balance = random.randint(1,10000)
        acc_details = (acc_no,balance,creation_timestamp)
        acc_list.append(acc_details)
        cust_acc = (cust_id,acc_no)
        cust_acc_list.append(cust_acc)
        acc_nos_list.append(acc_no)
	
			
def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)
 
        # create a cursor
        cur = conn.cursor()
        
 # execute a statement
        psycopg2.extras.execute_values(cur, "INSERT INTO customer (cust_id, first_name, last_name, street_address, city, state_name, zipcode, created_on) VALUES %s", cust_list)

        psycopg2.extras.execute_values(cur, "INSERT INTO ACCOUNTS_INFO (ACCOUNT_NUMBER, BALANCE, created_on) VALUES %s", acc_list)
		
        psycopg2.extras.execute_values(cur, "INSERT INTO customer_ACCOUNTS_INFO (cust_id, ACCOUNT_NUMBER) VALUES %s", cust_acc_list)
		
        conn.commit()
		
     # close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
 
 
if __name__ == '__main__':
    connect()