


.PHONY: production-build
production-build:
	cd frontend && npm run build
	sudo docker-compose build


.PHONY: production-up
production-up:
	cd frontend && npm run build
	sudo docker-compose up --build