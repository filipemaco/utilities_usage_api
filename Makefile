.PHONY: up
up:
	docker-compose up --build

.PHONY: down
down:
	docker-compose down --rmi all -v
