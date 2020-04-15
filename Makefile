IMAGE_NAME=come_together
CONTAINER_NAME=come_together
PORT=8080

all: build start

build:
	docker build -t $(IMAGE_NAME) .

start:
	docker run -d -p $(PORT):5000 --name $(CONTAINER_NAME) $(IMAGE_NAME) || docker start $(CONTAINER_NAME)

stop:
	docker stop $(CONTAINER_NAME)

clean: stop
	docker rm $(CONTAINER_NAME)

fclean: clean
	docker image rm $(IMAGE_NAME)

help:
	@echo "commands:"
	@echo "make 		--	build an image and start the container"
	@echo "make build	--	build an image"
	@echo "make start	--	start the container"
	@echo "make stop	--	stop the container"
	@echo "make clear	--	remove the container"
	@echo "make fclear	--	remove the container and the image"
	@echo "make re		--	remove container and image, build again and start the container"
	@echo "make help	--	show this message"

re: clean all
