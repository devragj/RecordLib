


.PHONY: production-build
production-build:
	yarn run build
	sudo docker-compose -f deployment/docker-compose.yml build

.PHONY: production-up
production-up:
	sudo docker-compose -f deployment/docker-compose.yml up

.PHONY: push
push:
	docker push ${CONTAINER_REGISTRY}/recordlibfrontend:${CONTAINER_TAG}
	docker push ${CONTAINER_REGISTRY}/recordlibdjango:${CONTAINER_TAG}
	docker push ${CONTAINER_REGISTRY}/recordlibdb:${CONTAINER_TAG}