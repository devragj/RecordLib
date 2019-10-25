


.PHONY: production-build
production-build:
	sudo docker-compose -f deployment/docker-compose.yml build

.PHONY: production-up
production-up:
	sudo docker-compose -f deployment/docker-compose.yml up