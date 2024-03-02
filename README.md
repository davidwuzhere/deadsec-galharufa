# Galharufa API

Swagger URL: http://localhost:8000/api/v1/swagger/

## Requirements

- Docker
- Docker compose

## Getting started

### Initialize API

`sudo make clean && make build`

### Stop containers

`make down`

### Run containers

`make up`

### Restart containers

`make restart`

### Rebuild containers (recommended after new commits)

`make rebuild`

### Delete all containers and images

`make clean`

## TODOs

- Unit tests
- e2e tests
