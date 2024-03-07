docker/build:
	poetry export -f requirements.txt --without-hashes --without dev > requirements.txt
	docker build -t rinha-backend .