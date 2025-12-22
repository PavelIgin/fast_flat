DOCKER_COMPOSE_FILE="`pwd`/docker-compose.yaml"
DOCKER_COMPOSE_TEST_FILE="`pwd`/docker-compose.test.yaml"
DOCKER_COMPOSE_PROJECT=fast_flat

DOCKER_COMPOSE_CMD=docker-compose -p $(DOCKER_COMPOSE_PROJECT) -f $(DOCKER_COMPOSE_FILE)
DOCKER_COMPOSE_TEST_CMD=docker-compose -p $(DOCKER_COMPOSE_PROJECT)pytest -f $(DOCKER_COMPOSE_TEST_FILE)
FASTAPI_CONTAINER=web

run:
	$(DOCKER_COMPOSE_CMD) --env-file .env up --build

down:
	$(DOCKER_COMPOSE_CMD) down

build:
	$(DOCKER_COMPOSE_CMD) build


pytest_init:
	$(DOCKER_COMPOSE_TEST_CMD) up

pytest_build:
	$(DOCKER_COMPOSE_TEST_CMD) build

pytest_down:
	$(DOCKER_COMPOSE_TEST_CMD) down


pytest_cmd:
	@echo "Ensure that 'make pytest_init' is called if it fails"
# 	find tests -type d -name "__pycache__" -exec rm -rf {} \;
# 	find tests -type f -name "*.pyc" -delete
	$(DOCKER_COMPOSE_TEST_CMD) exec $(FASTAPI_CONTAINER) $(cmd)





