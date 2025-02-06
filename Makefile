DEPLOY_HOST := 93.123.95.160
DOCKER_TAG := latest
DOCKER_IMAGE := plates-tg
DOCKER_NAME := car-plates-tg
USERNAME := dmitriy

.PHONY: install
install:
	pip install -r requirements.txt

.PHONY: run_app
run_app:
	PYTHONPATH=. python main.py

.PHONY: lint
lint:
	PYTHONPATH=. tox

.PHONY: build
build:
	docker build -f Dockerfile . -t $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: docker_run
docker_run:
	docker run --name=$(DOCKER_NAME) -d $(DOCKER_IMAGE):$(DOCKER_TAG)

.PHONY: deploy
deploy:
	ansible-playbook -i deploy/ansible/inventory.ini  deploy/ansible/deploy.yml \
		-e host=$(DEPLOY_HOST) \
		-e docker_image=$(DOCKER_IMAGE) \
		-e docker_tag=$(DOCKER_TAG) \
		-e docker_registry_user=$(CI_REGISTRY_USER) \
		-e docker_registry_password=$(CI_REGISTRY_PASSWORD) \
		-e docker_registry=$(CI_REGISTRY) \

.PHONY: destroy
destroy:
	ansible-playbook -i deploy/ansible/inventory.ini deploy/ansible/destroy.yml \
		-e host=$(DEPLOY_HOST)
