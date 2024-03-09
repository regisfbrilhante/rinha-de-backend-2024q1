docker/build:
	poetry export -f requirements.txt --without-hashes --without dev > requirements.txt
	docker build -t rinha-backend .

test/setup/infra/start:
	make test/setup/infra/stop
	docker container run -d -e POSTGRES_PASSWORD=123 -e POSTGRES_USER=admin -e POSTGRES_DB=rinha -p 5400:5432 --name postgres-teste postgres:15.6-alpine3.19 
	sleep 10

test/setup/infra/stop:

	container_id=$$(docker container ls -a -q --filter "name=postgres-teste"); \
	if [ ! -z "$$container_id" ]; then \
		docker container stop $$container_id; \
		docker container rm $$container_id -v; \
	fi
	