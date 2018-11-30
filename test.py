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

cust_list = []
acc_list = []
acc_nos_list = []
cust_acc_list  = []

# generating fake customer data
for i in range(1, count+1):
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
    user_total_acc = fake.pyint()%(max_acc+1) # randomly generate the number of accounts for a user
    total_acc = len(acc_list) # list containg all existing account numbers
    # case 1: no of acc for this user <= total existing accounts
    if(user_total_acc <= total_acc):
        user_new_acc = fake.pyint()%(user_total_acc+1) # randomly generate no of new accounts for this user
        user_existing_acc = user_total_acc - user_new_acc
        # case: no of acc for this user = total existing accounts
        if(len(acc_nos_list) == user_existing_acc):
            random_index = 0 # use the entire list
        else:
            # case: no of acc for this user < total existing accounts
            random_index = fake.pyint()%(len(acc_nos_list)-user_existing_acc)
        existing_arr = acc_nos_list[random_index:random_index+user_existing_acc]		
    else:
        # case 2: total existing accounts = 0
        if(total_acc == 0):
            user_new_acc = user_total_acc
            user_existing_acc = 0
        else:
            # case 3: no of acc for this user > total existing accounts
            user_existing_acc = fake.pyint()%(total_acc+1)
            random_index = fake.pyint()%(len(acc_nos_list))
            existing_arr = acc_nos_list[random_index:random_index+user_existing_acc]
            user_new_acc = user_total_acc - user_existing_acc
    # customer-accounts relation added for all existing accounts for this user
    for j in range(1, user_existing_acc+1):
        acc_no = existing_arr[j-1]
        cust_acc_details = (cust_id,acc_no)
        cust_acc_list.append(cust_acc_details)
    # new accounts created for this user
    for k in range(1, user_new_acc+1):
        acc_no = fake.bban()
        balance = fake.pyfloat(left_digits=5, right_digits=2, positive=True)
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
		
        cursor = conn.cursor('cursor_1', cursor_factory=psycopg2.extras.DictCursor)
        
        cursor.execute('select t4.state_name, trunc(temp2.avgbal,2) from (select temp.cust as cust, avg(temp.bal) as avgbal from (select t1.cust_id as cust, t3.account_number as acc, t2.balance as bal from customer t1, accounts_info t2, customer_accounts_info t3 where t1.cust_id = t3.cust_id and t2.account_number = t3.account_number) temp group by temp.cust order by avgbal desc) temp2, customer t4 where t4.cust_id = temp2.cust LIMIT 10')
		
        print ("\nQuery 1: States with ten highest average customer balances\n")
        for row in cursor:
            print ("State Name: %s Average Balance: %s" % (row[0],row[1]))
		
        cursor = conn.cursor('cursor_2', cursor_factory=psycopg2.extras.DictCursor)
		
        cursor.execute('select temp1.cust, temp1.sumbal from (select temp.cust as cust, sum(temp.bal) as sumbal from (select t1.cust_id as cust, t3.account_number as acc, t2.balance as bal from customer t1, accounts_info t2, customer_accounts_info t3 where t1.cust_id = t3.cust_id and t2.account_number = t3.account_number) temp group by temp.cust order by sumbal desc) temp1 LIMIT 10')
		
        print ("\nQuery 2: Ten customers with highest total balances\n")
        for row in cursor:
            print ("Customer ID: %s Total Balance: %s" % (row[0],row[1]))
		
        cursor = conn.cursor('cursor_3', cursor_factory=psycopg2.extras.DictCursor)
		
        cursor.execute('select temp1.cust, temp1.sumbal from (select temp.cust as cust, sum(temp.bal) as sumbal from (select t1.cust_id as cust, t3.account_number as acc, t2.balance as bal from customer t1, accounts_info t2, customer_accounts_info t3 where t1.cust_id = t3.cust_id and t2.account_number = t3.account_number) temp group by temp.cust order by sumbal) temp1 LIMIT 10')
		
        print ("\nQuery 3: Ten customers with lowest total balances\n")
        for row in cursor:
            print ("Customer ID: %s Total Balance: %s" % (row[0],row[1]))
		
        cursor = conn.cursor('cursor_4', cursor_factory=psycopg2.extras.DictCursor)
		
        cursor.execute('select temp2.cust,t4.account_number, trunc((0.1 * t4.balance),2), trunc((0.9 * t4.balance),2),t4.balance from (select temp1.cust from (select temp.cust as cust, sum(temp.bal) as avgbal from (select t1.cust_id as cust, t3.account_number as acc, t2.balance as bal from customer t1, accounts_info t2, customer_accounts_info t3 where t1.cust_id = t3.cust_id and t2.account_number = t3.account_number) temp group by temp.cust order by avgbal desc) temp1 LIMIT 10) temp2, accounts_info t4 where t4.balance = (select max(t5.balance) from accounts_info t5, customer_accounts_info t6 where t6.cust_id = temp2.cust and t5.account_number = t6.account_number)')
		
        top_accounts = []
        bottom_accounts = []
        top_new_balances = []
        bottom_add_balances = []
		
        print ("\nQuery 4: Ten customers with highest total balances\n")
        for row in cursor:
            print ("Customer ID: %s Account Number %s Balance: %s New Balance: %s" % (row[0],row[1],row[4],row[3]))
            top_accounts.append(row[1])
            top_new_balances.append(float(row[3]))
            bottom_add_balances.append(float(row[2]))

        top_new_balances_str = " ".join(str(x)+',' for x in top_new_balances)[0:-1]
        top_accounts_str = " ".join("'"+str(x)+"'," for x in top_accounts)[0:-1]
        bottom_add_balances_str = " ".join(str(x)+',' for x in bottom_add_balances)[0:-1]
	
       # update balances for accounts (highest balance) of customers with highest total balances
	
        query = 'update accounts_info set balance = data_table.balance from (select unnest(array['+top_accounts_str+']) as accounts, unnest(array['+top_new_balances_str+']) as balance) as data_table where accounts_info.account_number = data_table.accounts'
		
        cur.execute(query)
		
        cursor = conn.cursor('cursor_6', cursor_factory=psycopg2.extras.DictCursor)
		
        cursor.execute('select temp2.cust,  t4.account_number, t4.balance from (select temp1.cust from (select temp.cust as cust, sum(temp.bal) as avgbal from (select t1.cust_id as cust, t3.account_number as acc, t2.balance as bal from customer t1, accounts_info t2, customer_accounts_info t3 where t1.cust_id = t3.cust_id and t2.account_number = t3.account_number) temp group by temp.cust order by avgbal) temp1 LIMIT 10) temp2, accounts_info t4 where t4.balance = (select min(t5.balance)from accounts_info t5, customer_accounts_info t6 where t6.cust_id = temp2.cust and t5.account_number = t6.account_number)')
		
        print ("\nQuery 4: Ten customers with lowest total balances\n")
        idx = 0
        for row in cursor:
            print ("Customer ID: %s Account Number: %s Existing Balance: %s New balance: %s" % (row[0],row[1],row[2],float(row[2])+bottom_add_balances[idx]))
            bottom_accounts.append(row[1])
            idx = idx+1
        
        bottom_accounts_str = " ".join("'"+str(x)+"'," for x in bottom_accounts)[0:-1]	
	
        # update balances for accounts (lowest balance) of customers with lowest total balances
	
        query = 'update accounts_info set balance = accounts_info.balance + data_table.balance from (select unnest(array['+bottom_accounts_str+']) as accounts, unnest(array['+bottom_add_balances_str+']) as balance) as data_table where accounts_info.account_number = data_table.accounts'
			
        cur.execute(query)
        
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
