# For accessing mysql into container
sudo mysql --host=127.0.0.1 --port=3307  --user=my_user --password=my_password
# For building dockerfile
docker build --tag python -f ./Dockerfile.python .
# For running with interactive termina
docker run --name python -it python /bin/sh
# For running with interactive termina
docker start -i python /bin/sh

docker run --name python python
docker compose up --force-recreate --build -f ./docker-compose-db.yml
docker compose up --force-recreate --build -f ./docker-compose-python.yml
# ?
docker compose -f ./docker-compose.yml  up --force-recreate --build 
docker compose -f ./docker-compose.yml  down
docker compose -f ./docker-compose-db.yml  up --force-recreate --build 
docker compose -f ./docker-compose-db.yml  down

sudo docker start -i proyectofinal-python-app-1
sudo docker exec -it proyectofinal-db-1 /bin/sh
sudo docker exec -it proyectofinal-python-app-1 /bin/sh

sudo service mysql stop



docker compose -f ./docker-compose.yml  up --force-recreate --build db
docker compose -f ./docker-compose.yml  run