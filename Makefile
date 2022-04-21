start: ## Start the docker containers
	@echo "Starting the docker containers"
	@docker-compose up -d
	@echo "Containers started - http://localhost:8000"

stop: ## Stop Containers
	@docker-compose down

build: ## Build Containers
	@docker-compose build

ssh: ## SSH into running web container
	docker-compose exec web bash

migrations: ## Create DB migrations in the container
	@docker-compose exec web python manage.py makemigrations

migrate: ## Run DB migrations in the container
	@docker-compose exec web python manage.py migrate

shell: ## Get a Django shell
	@docker-compose exec web python manage.py shell

dbshell: ## Get a Database shell
	@docker-compose exec db psql -U postgres bmt_sales_automation

test: ## Run Django tests
	@docker-compose exec web python manage.py test

init: start migrations migrate  ## Quickly get up and running (start containers and migrate DB)

npm-install: ## Runs npm install in the container
	@docker-compose exec web npm install

npm-build: ## Runs npm build in the container (for production assets)
	@docker-compose exec web npm run build

npm-watch: ## Runs npm watch in the container (recommended for dev)
	@docker-compose exec web npm run dev-watch

.PHONY: help
.DEFAULT_GOAL := help

help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

update-containers:
	echo ~~~puling latest code from git~~~
	git pull
	echo ~~~taking down docker containers~~~
	docker-compose down
	echo ~~~rebuilding docker containers~~~
	docker-compose build
	echo ~~~starting docker containers~~~
	docker-compose up -d
	sleep 5s
	echo ~~~removing unneeded files from ccontainers~~~