build:
	mkdir static
	docker compose up

up:
	docker compose up

up-desenv:
	docker build -t galharufa-desenv .
	docker run -p 8000:8000 --name galharufa-desenv galharufa-desenv:latest

down:
	docker compose down

restart:
	docker compose restart

rebuild:
	docker compose up --build

clean:
	docker stop galharufa-api-backend-1
	docker stop galharufa-api-db-1
	docker rm galharufa-api-backend-1
	docker rm galharufa-api-db-1
	docker image rm galharufa-api-backend
	rm -rf static
	rm -rf .dbdata
	rm -rf galharufa/migrations