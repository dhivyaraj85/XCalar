sudo docker build . -t my_postgres
sudo docker container run --name=my_postgres postgres &
sleep 10s
sudo docker network create --subnet 172.20.0.0/16 --ip-range 172.20.240.0/20 my_postgres_network
sudo docker network connect --ip 172.20.128.2 my_postgres_network my_postgres
sudo docker network inspect my_postgres_network
psql -h 172.20.128.2 -d postgres -U postgres -f init.sql