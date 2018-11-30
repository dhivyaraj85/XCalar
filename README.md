XCalar Takehome Assignment

Steps to run the project
1. Activate and install dependencies for VIRTUALENV (Use requirements.txt: pip freeze)
2. Run setup.sh: creates a docker image from the postgres image maintained in the docker library, using Dockerfile, which inturn invokes init.sql, which initializes the database schema
3. Run test.py (python test.py --customers=1000 --max_accounts=10): creates fake test data and runs the queries in the exercise

Notes:
* Used the psycopg2 library instead of pyodbc
* All terminal output added in terminal output.o
* Tried both ADD and COPY in Dockerfile for init.sql, but it wasn't runninng. Tried docker-compose files, but still didn't run. Ran psql on command line to init the DB instead. 

Questions
1. Spent 5 days on the entire project.
2. Yes. I took some help from a friend for parts involving docker.
3. Helpful URLs:
	https://docs.docker.com/
	https://virtualenv.pypa.io/en/latest/userguide/
	https://faker.readthedocs.io/en/master/
	https://www.postgresql.org/docs/9.5/

4. Technologies - Docker, Virtualenv.
5. Yes. I believe the reuslts are correct. The fake test data is idempotent. The queries give the expected results.
6. I do not think there are any gaps between what I have delivered and the requirements.


Thank you for considering my application.
Dhivya
