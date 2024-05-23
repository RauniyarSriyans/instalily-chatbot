.PHONY: build instal venv scrape-models podman-start podman-stop minikube partselect-db forward-partselect-db migrateup migratedown server-dev server-prod

SHELL:=/bin/bash
VIRTUAL_ENV=.venv
PYTHON=${VIRTUAL_ENV}/bin/python3

# DB_NAME=partselect
# DB_USER=partselect
# DB_PASSWORD=partselect

# Colors for echos 
ccend = $(shell tput sgr0)
ccbold = $(shell tput bold)
ccgreen = $(shell tput setaf 2)
ccso = $(shell tput smso)

build:
	@echo ""
	@echo "$(ccso)--> Build $(ccend)"
	$(MAKE) clean
	$(MAKE) install

install: venv requirements.txt
	@echo "$(ccso)--> Updating packages $(ccend)"
	$(PYTHON) -m pip install -r requirements.txt

venv: $(VIRTUAL_ENV)

$(VIRTUAL_ENV):
	@echo "$(ccso)--> Install and setup virtualenv $(ccend)"
	python3 -m pip install --upgrade pip
	python3 -m pip install virtualenv
	virtualenv $(VIRTUAL_ENV)

# partselect-db:
# 	kubectl run $(DB_NAME) --image postgres:alpine --restart=Never --env="POSTGRES_USER=$(DB_USER)" --env="POSTGRES_PASSWORD=$(DB_PASSWORD)" --env="POSTGRES_DB=$(DB_NAME)"

# forward-partselect-db:
# 	kubectl port-forward partselect 5432:5432

# migrateup:
# 	@migrate -path db/migrations -database "postgres://$(DB_USER):$(DB_PASSWORD)@localhost:5432/$(DB_NAME)?sslmode=disable" -verbose up

# migratedown:
# 	@migrate -path db/migrations -database "postgres://$(DB_USER):$(DB_PASSWORD)@localhost:5432/$(DB_NAME)?sslmode=disable" -verbose down

server-dev:
	fastapi dev main.py

server-prod:
	fastapi run main.py