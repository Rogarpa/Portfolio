## Requirements:
- Docker engine
- Docker-compose
## To execute the project follow the next steps:
- Startup the database service in mysql container:
```sh
docker compose -f ./docker-compose.yml  up db
```

- Startup the CRUD command line menu inside python app container:
docker compose -f ./docker-compose.yml  run python-app

```sh
docker compose -f ./docker-compose.yml  run python-app
```