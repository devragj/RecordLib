


.PHONY: production-build
production-build:
	sudo docker-compose build


.PHONY: production-up
production-up:
	sudo docker-compose up --build