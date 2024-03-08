docker/build:
	poetry export -f requirements.txt --without-hashes --without dev > requirements.txt
	docker build -t rinha-backend .

test/setup/infra/start:
	docker container run -d -e POSTGRES_PASSWORD=123 -e POSTGRES_USER -e POSTGRES_DB=rinha -p 5400:5432 postgres:15.6-alpine3.19
	sleep 10

test/setup/infra/stop:
	docker container stop $(shell docker container ls -q --filter ancestor=postgres:15.6-alpine3.19)