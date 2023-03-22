build:
	docker compose up --build -d --remove-orphans
up:
	docker compose up -d
down:
	docker compose down
show_logs:
	docker compose logs
db:
	docker compose -p openecoe-persistence -f .docker/docker-compose.persistence.yml up --build -d --remove-orphans 
db_down:
	docker compose -p openecoe-persistence -f .docker/docker-compose.persistence.yml down 
prod:
	docker compose -p openecoe-prod -f .docker/docker-compose.prod.yml up --build -d --remove-orphans 
prod_down:
	docker compose -p openecoe-prod -f .docker/docker-compose.prod.yml down 