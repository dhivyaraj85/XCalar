#!/usr/bin/python
import psycopg2
from config import config
from psycopg2.extras import execute_values

from faker import Faker
fake = Faker()
fake.seed(4321)

count_str = input("Enter the number of customers: ")
count = int(count_str)

count_str2 = input("Enter the maximum number of accounts: ")
count_acc = int(count_str2)

cust_list = []

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