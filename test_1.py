#!/usr/bin/python
import psycopg2
from psycopg2.extras import execute_values
from config import config

from faker import Faker
fake = Faker()
fake.seed(4321)

count_str = input("Enter the number of customers: ")
count = int(count_str)

cust_list = []

for i in range(1, count+1):
    first_name = fake.first_name()
    last_name = fake.last_name()
    street_address = fake.street_address()
    city = fake.city()
    state = fake.state_abbr(include_territories=True)
    zipcode = fake.zipcode()
    creation_timestamp = fake.past_datetime(start_date="-30d", tzinfo=None)
    cust_details = (first_name,last_name,street_address,city,state,zipcode,creation_timestamp)
    cust_list.append(cust_details)
	
print(cust_list)

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
        #insert_query = 'insert into customer (first_name, last_name, street_address, city, state_name, zipcode, created_on) values %s'
        #psycopg2.extras.execute_values (cur, insert_query, cust_list, template=None, page_size=100)
        print('Count of records in test1 table:')
        cur.execute('SELECT count(*) from test1')
		
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