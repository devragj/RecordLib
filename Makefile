


.PHONY: build
build:
	rm frontend/bundles/*
	yarn run build
	sudo docker-compose -f deployment/docker-compose.yml build

# for local testing
.PHONY: production-up-locally
production-up-locally:
	sudo docker-compose -f deployment/docker-compose.yml up

.PHONY: push
push:
	sudo docker push ${CONTAINER_REGISTRY}/recordlibfrontend:${CONTAINER_TAG}
	sudo docker push ${CONTAINER_REGISTRY}/recordlibdjango:${CONTAINER_TAG}
	sudo docker push ${CONTAINER_REGISTRY}/recordlibdb:${CONTAINER_TAG}

# deploy is used to get the newest images running on a remote host.
# Assumes that the host is set up to receive this command. 
.PHONY: deploy
deploy:
	ssh ${HOST}; cd recordlib; ./update.sh 

build-push-deploy: build push deploy

